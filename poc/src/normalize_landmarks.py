"""Create traceable body-relative motion data from immutable raw landmarks."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from statistics import median

import numpy as np
import pandas as pd


POSE_LANDMARK_COUNT = 33
HAND_LANDMARK_COUNT = 21
LEFT_SHOULDER_ID = 11
RIGHT_SHOULDER_ID = 12
COORDINATES = ("x", "y", "z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contiguous_runs(frames: list[int]) -> list[tuple[int, int]]:
    if not frames:
        return []
    runs: list[tuple[int, int]] = []
    start = previous = frames[0]
    for frame in frames[1:]:
        if frame != previous + 1:
            runs.append((start, previous))
            start = frame
        previous = frame
    runs.append((start, previous))
    return runs


def classify_gap(start: int, end: int, total_frames: int) -> str:
    if start == 0:
        return "leading"
    if end == total_frames - 1:
        return "trailing"
    return "internal"


def build_missing_diagnostic(
    video_name: str,
    total_frames: int,
    fps: float,
    frame_timestamps: dict[int, float],
    detected_frames: set[int],
    hand: str,
    max_gap_frames: int,
) -> dict:
    missing_frames = [frame for frame in range(total_frames) if frame not in detected_frames]
    gaps = []
    for start, end in contiguous_runs(missing_frames):
        length = end - start + 1
        gap_type = classify_gap(start, end, total_frames)
        eligible = gap_type == "internal" and length <= max_gap_frames
        frame_numbers = list(range(start, end + 1))
        timestamps = [round(frame_timestamps[frame], 2) for frame in frame_numbers]
        gaps.append(
            {
                "start_frame": start,
                "end_frame": end,
                "length_frames": length,
                "approximate_duration_ms": round(1000 * length / fps, 2),
                "gap_type": gap_type,
                "frame_numbers": frame_numbers,
                "timestamps_ms": timestamps,
                "interpolation_eligible": eligible,
                "decision": "interpolate" if eligible else "leave_unresolved",
            }
        )

    return {
        "video": video_name,
        "analysis_stage": "raw_before_interpolation",
        "detection_basis": f"presence of all expected landmarks for dominant {hand} hand",
        "total_frames": total_frames,
        "fps": fps,
        "dominant_hand": hand,
        "max_internal_gap_frames": max_gap_frames,
        "missing_frames": [
            {"frame": frame, "timestamp_ms": round(frame_timestamps[frame], 2)}
            for frame in missing_frames
        ],
        "gaps": gaps,
        "summary": {
            "total_missing_frames": len(missing_frames),
            "longest_missing_run_frames": max(
                (gap["length_frames"] for gap in gaps), default=0
            ),
            "median_gap_length_frames": float(
                median([gap["length_frames"] for gap in gaps]) if gaps else 0
            ),
            "gap_count": len(gaps),
        },
    }


def validate_raw_grain(
    hand_df: pd.DataFrame, pose_df: pd.DataFrame, total_frames: int
) -> None:
    required_hand = {"frame", "timestamp_ms", "hand", "landmark_id", "x", "y", "z"}
    required_pose = {"frame", "timestamp_ms", "landmark_id", "x", "y", "z"}
    if missing := required_hand.difference(hand_df.columns):
        raise ValueError(f"Hand CSV is missing required columns: {sorted(missing)}")
    if missing := required_pose.difference(pose_df.columns):
        raise ValueError(f"Pose CSV is missing required columns: {sorted(missing)}")
    if hand_df.duplicated(["frame", "hand", "landmark_id"]).any():
        raise ValueError("Hand CSV contains duplicate frame/hand/landmark rows")
    if pose_df.duplicated(["frame", "landmark_id"]).any():
        raise ValueError("Pose CSV contains duplicate frame/landmark rows")
    if not hand_df["frame"].between(0, total_frames - 1).all():
        raise ValueError("Hand CSV contains a frame outside the metadata frame range")
    if not pose_df["frame"].between(0, total_frames - 1).all():
        raise ValueError("Pose CSV contains a frame outside the metadata frame range")


def shoulder_reference(pose_df: pd.DataFrame) -> pd.DataFrame:
    shoulders = pose_df.loc[
        pose_df["landmark_id"].isin([LEFT_SHOULDER_ID, RIGHT_SHOULDER_ID]),
        ["frame", "landmark_id", "x", "y", "z"],
    ].pivot(index="frame", columns="landmark_id", values=["x", "y", "z"])
    required = [(axis, landmark) for axis in COORDINATES for landmark in (11, 12)]
    missing_columns = [column for column in required if column not in shoulders.columns]
    if missing_columns:
        raise ValueError(f"Pose CSV lacks shoulder coordinates: {missing_columns}")

    reference = pd.DataFrame(index=shoulders.index)
    for axis in COORDINATES:
        reference[f"shoulder_mid_{axis}"] = (
            shoulders[(axis, LEFT_SHOULDER_ID)]
            + shoulders[(axis, RIGHT_SHOULDER_ID)]
        ) / 2
    deltas = np.column_stack(
        [
            shoulders[(axis, LEFT_SHOULDER_ID)]
            - shoulders[(axis, RIGHT_SHOULDER_ID)]
            for axis in COORDINATES
        ]
    )
    reference["shoulder_width"] = np.linalg.norm(deltas, axis=1)
    reference.loc[reference["shoulder_width"] <= 0, "shoulder_width"] = np.nan
    return reference.reset_index()


def add_body_relative_coordinates(
    data: pd.DataFrame, reference: pd.DataFrame
) -> pd.DataFrame:
    result = data.rename(
        columns={
            "x": "raw_x",
            "y": "raw_y",
            "z": "raw_z",
            "visibility": "raw_visibility",
        }
    ).merge(reference, on="frame", how="left", validate="many_to_one")
    for axis in COORDINATES:
        result[f"norm_{axis}"] = (
            result[f"raw_{axis}"] - result[f"shoulder_mid_{axis}"]
        ) / result["shoulder_width"]
    return result


def smooth_resolved_segments(
    data: pd.DataFrame, group_columns: list[str], window_size: int
) -> pd.DataFrame:
    result = data.copy()
    for axis in COORDINATES:
        result[f"smooth_{axis}"] = np.nan

    grouping = group_columns[0] if len(group_columns) == 1 else group_columns
    for _, index in result.groupby(grouping, sort=False).groups.items():
        group = result.loc[index].sort_values("frame")
        resolved = group["norm_x"].notna() & ~group["is_unresolved"]
        segment = (~resolved).cumsum()
        for axis in COORDINATES:
            smoothed = group[f"norm_{axis}"].where(resolved).groupby(segment).transform(
                lambda values: values.rolling(
                    window=window_size, center=True, min_periods=1
                ).mean()
            ).where(resolved)
            result.loc[group.index, f"smooth_{axis}"] = smoothed.to_numpy()
    return result


def normalize_and_smooth(
    video_name: str, max_gap_frames: int = 3, window_size: int = 3, hand: str | None = None
) -> dict:
    if max_gap_frames < 0:
        raise ValueError("max_gap_frames must be non-negative")
    if window_size < 1 or window_size % 2 == 0:
        raise ValueError("window_size must be a positive odd integer")

    raw_dir = Path("poc/output/landmarks")
    normalized_dir = Path("poc/output/normalized")
    diagnostics_dir = Path("poc/output/diagnostics")
    normalized_dir.mkdir(parents=True, exist_ok=True)
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    pose_path = raw_dir / f"{video_name}_pose_landmarks.csv"
    hand_path = raw_dir / f"{video_name}_hand_landmarks.csv"
    source_metadata_path = raw_dir / f"{video_name}_metadata.json"
    for path in (pose_path, hand_path, source_metadata_path):
        if not path.exists():
            raise FileNotFoundError(f"Required raw evidence not found: {path}")

    source_metadata = json.loads(source_metadata_path.read_text(encoding="utf-8"))
    total_frames = int(source_metadata["total_frames_metadata"])
    fps = float(source_metadata["fps"])
    if fps <= 0:
        raise ValueError("Metadata fps must be positive")
    hand_df = pd.read_csv(hand_path)
    pose_df = pd.read_csv(pose_path)
    validate_raw_grain(hand_df, pose_df, total_frames)

    hand_counts = hand_df.groupby("hand")["frame"].nunique().sort_values(ascending=False)
    if hand_counts.empty:
        raise ValueError("No hand landmarks are available for normalization")
    dominant_hand = hand or str(hand_counts.index[0])
    if dominant_hand not in hand_counts.index:
        raise ValueError(f"Requested hand {dominant_hand!r} is absent from the raw hand CSV")
    selected_hand = hand_df.loc[hand_df["hand"] == dominant_hand].copy()

    pose_timestamps = pose_df.groupby("frame")["timestamp_ms"].first().to_dict()
    frame_timestamps = {
        frame: float(pose_timestamps.get(frame, 1000 * frame / fps))
        for frame in range(total_frames)
    }
    detected_counts = selected_hand.groupby("frame")["landmark_id"].nunique()
    detected_frames = set(
        detected_counts.loc[detected_counts == HAND_LANDMARK_COUNT].index.astype(int)
    )
    missing_diagnostic = build_missing_diagnostic(
        video_name,
        total_frames,
        fps,
        frame_timestamps,
        detected_frames,
        dominant_hand,
        max_gap_frames,
    )
    missing_path = diagnostics_dir / f"{video_name}_missing_frames.json"
    missing_path.write_text(
        json.dumps(missing_diagnostic, indent=2) + "\n", encoding="utf-8"
    )

    reference = shoulder_reference(pose_df)

    pose_index = pd.MultiIndex.from_product(
        [range(total_frames), range(POSE_LANDMARK_COUNT)],
        names=["frame", "landmark_id"],
    )
    pose_complete = pose_df.set_index(["frame", "landmark_id"]).reindex(pose_index).reset_index()
    pose_complete["timestamp_ms"] = pose_complete["frame"].map(frame_timestamps)
    pose_normalized = add_body_relative_coordinates(pose_complete, reference)
    pose_normalized["is_detected"] = pose_normalized["raw_x"].notna()
    pose_normalized["is_interpolated"] = False
    pose_normalized["is_unresolved"] = pose_normalized["norm_x"].isna()
    pose_normalized = smooth_resolved_segments(
        pose_normalized, ["landmark_id"], window_size
    )

    hand_index = pd.MultiIndex.from_product(
        [range(total_frames), [dominant_hand], range(HAND_LANDMARK_COUNT)],
        names=["frame", "hand", "landmark_id"],
    )
    hand_complete = (
        selected_hand.set_index(["frame", "hand", "landmark_id"])
        .reindex(hand_index)
        .reset_index()
    )
    hand_complete["timestamp_ms"] = hand_complete["frame"].map(frame_timestamps)
    hand_normalized = add_body_relative_coordinates(hand_complete, reference)
    hand_normalized["is_detected"] = hand_normalized["raw_x"].notna()
    hand_normalized["is_interpolated"] = False

    eligible_frames = {
        frame
        for gap in missing_diagnostic["gaps"]
        if gap["interpolation_eligible"]
        for frame in gap["frame_numbers"]
    }
    for _, index in hand_normalized.groupby(["hand", "landmark_id"]).groups.items():
        group = hand_normalized.loc[index].sort_values("frame")
        for axis in COORDINATES:
            interpolated = group[f"norm_{axis}"].interpolate(
                method="linear", limit_area="inside"
            )
            eligible_mask = group["frame"].isin(eligible_frames) & group[f"norm_{axis}"].isna()
            hand_normalized.loc[group.index[eligible_mask], f"norm_{axis}"] = interpolated.loc[
                eligible_mask
            ].to_numpy()

    interpolated_rows = (
        ~hand_normalized["is_detected"]
        & hand_normalized["frame"].isin(eligible_frames)
        & hand_normalized[["norm_x", "norm_y", "norm_z"]].notna().all(axis=1)
    )
    hand_normalized.loc[interpolated_rows, "is_interpolated"] = True
    hand_normalized["is_unresolved"] = hand_normalized[
        ["norm_x", "norm_y", "norm_z"]
    ].isna().any(axis=1)
    hand_normalized = smooth_resolved_segments(
        hand_normalized, ["hand", "landmark_id"], window_size
    )

    column_order = [
        "frame", "timestamp_ms", "hand", "landmark_id",
        "raw_x", "raw_y", "raw_z", "raw_visibility",
        "norm_x", "norm_y", "norm_z",
        "smooth_x", "smooth_y", "smooth_z",
        "shoulder_mid_x", "shoulder_mid_y", "shoulder_mid_z", "shoulder_width",
        "is_detected", "is_interpolated", "is_unresolved",
    ]
    pose_column_order = [column for column in column_order if column != "hand"]
    hand_output = normalized_dir / f"{video_name}_hand_normalized.csv"
    pose_output = normalized_dir / f"{video_name}_pose_normalized.csv"
    hand_normalized[column_order].to_csv(hand_output, index=False)
    pose_normalized[pose_column_order].to_csv(pose_output, index=False)

    interpolated_frames = sorted(
        map(
            int,
            hand_normalized.loc[
                hand_normalized["is_interpolated"], "frame"
            ].unique(),
        )
    )
    unresolved_frames = sorted(
        map(
            int,
            hand_normalized.loc[
                hand_normalized["is_unresolved"], "frame"
            ].unique(),
        )
    )
    normalization_metadata = {
        "video": video_name,
        "lineage": {
            "stages": ["raw", "normalized", "interpolated", "smoothed", "diagnostics"],
            "raw_inputs": {
                str(hand_path): {"sha256": sha256_file(hand_path)},
                str(pose_path): {"sha256": sha256_file(pose_path)},
                str(source_metadata_path): {"sha256": sha256_file(source_metadata_path)},
            },
            "derived_outputs": [str(hand_output), str(pose_output), str(missing_path)],
        },
        "dominant_hand": dominant_hand,
        "expected_index": {
            "frames": total_frames,
            "hands": [dominant_hand],
            "landmarks_per_hand": HAND_LANDMARK_COUNT,
            "hand_rows": total_frames * HAND_LANDMARK_COUNT,
        },
        "normalization": {
            "origin": "shoulder_midpoint",
            "origin_formula": "(left_shoulder_xyz + right_shoulder_xyz) / 2",
            "scale": "shoulder_width",
            "scale_formula": "euclidean_distance(left_shoulder_xyz, right_shoulder_xyz)",
            "coordinate_formula": "norm_axis = (raw_axis - shoulder_mid_axis) / shoulder_width",
            "interpretation": "Body-relative normalization reduces sensitivity to performer position and apparent scale.",
            "limitation": "This transformation does not provide full viewpoint invariance.",
        },
        "interpolation": {
            "method": "linear",
            "maximum_internal_gap_frames": max_gap_frames,
            "leading_extrapolation": False,
            "trailing_extrapolation": False,
            "interpolated_frames": interpolated_frames,
            "interpolated_frame_count": len(interpolated_frames),
            "unresolved_frames": unresolved_frames,
            "unresolved_frame_count": len(unresolved_frames),
            "interpolated_gaps": [
                gap for gap in missing_diagnostic["gaps"] if gap["interpolation_eligible"]
            ],
            "unresolved_gaps": [
                gap for gap in missing_diagnostic["gaps"] if not gap["interpolation_eligible"]
            ],
        },
        "smoothing": {
            "method": "centered_rolling_mean",
            "window_frames": window_size,
            "causal_lag": False,
            "trade_off": "Minimal smoothing reduces frame-level detector jitter while preserving temporal structure.",
            "normalized_coordinates_overwritten": False,
        },
    }
    metadata_output = normalized_dir / f"{video_name}_normalization_metadata.json"
    metadata_output.write_text(
        json.dumps(normalization_metadata, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Missing-frame diagnostic saved: {missing_path}")
    print(f"Normalized hand landmarks saved: {hand_output}")
    print(f"Normalized pose landmarks saved: {pose_output}")
    print(f"Normalization metadata saved: {metadata_output}")
    print(
        f"Interpolated frames: {len(interpolated_frames)}; "
        f"unresolved frames: {len(unresolved_frames)}"
    )
    return normalization_metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Normalize raw landmarks and conservatively handle short hand gaps."
    )
    parser.add_argument("--video-name", default="sign_reference")
    parser.add_argument("--max-gap-frames", type=int, default=3)
    parser.add_argument("--smoothing-window", type=int, default=3)
    parser.add_argument("--hand", choices=["Left", "Right"], default=None)
    arguments = parser.parse_args()
    normalize_and_smooth(
        arguments.video_name,
        max_gap_frames=arguments.max_gap_frames,
        window_size=arguments.smoothing_window,
        hand=arguments.hand,
    )
