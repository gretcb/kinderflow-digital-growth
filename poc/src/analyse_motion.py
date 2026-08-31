"""Generate auditable motion diagnostics from normalized landmark data."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

_matplotlib_cache = Path(tempfile.gettempdir()) / "kinder-signs-matplotlib"
_matplotlib_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_matplotlib_cache))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


LANDMARKS = {
    0: "wrist",
    4: "thumb_tip",
    8: "index_tip",
    12: "middle_tip",
    16: "ring_tip",
    20: "pinky_tip",
}
COORD_COLUMNS = ["smooth_x", "smooth_y", "smooth_z"]


def rounded(value: float | int, digits: int = 6) -> float:
    return round(float(value), digits)


def transition_diagnostics(
    landmark_data: pd.DataFrame, landmark_name: str, mad_multiplier: float
) -> tuple[dict, list[dict]]:
    data = landmark_data.sort_values("frame").reset_index(drop=True)
    coordinates = data[COORD_COLUMNS]
    frame_delta = data["frame"].diff()
    resolved = ~data["is_unresolved"].astype(bool) & coordinates.notna().all(axis=1)
    valid_transition = resolved & resolved.shift(1, fill_value=False) & frame_delta.eq(1)
    displacement = np.sqrt(coordinates.diff().pow(2).sum(axis=1)).where(valid_transition)
    valid_values = displacement.dropna()

    if valid_values.empty:
        median_displacement = maximum_displacement = trajectory_length = 0.0
        mad = abrupt_threshold = 0.0
    else:
        median_displacement = float(valid_values.median())
        maximum_displacement = float(valid_values.max())
        trajectory_length = float(valid_values.sum())
        mad = float((valid_values - median_displacement).abs().median())
        abrupt_threshold = median_displacement + mad_multiplier * mad

    abrupt = displacement.gt(abrupt_threshold) & valid_transition
    transition_rows = []
    for row_index in range(1, len(data)):
        is_valid = bool(valid_transition.iloc[row_index])
        value = displacement.iloc[row_index]
        transition_rows.append(
            {
                "landmark": landmark_name,
                "from_frame": int(data.loc[row_index - 1, "frame"]),
                "to_frame": int(data.loc[row_index, "frame"]),
                "status": "valid" if is_valid else "missing_transition",
                "displacement": rounded(value) if is_valid else None,
                "is_abrupt_jump": bool(abrupt.iloc[row_index]) if is_valid else False,
            }
        )

    valid_transition_count = int(valid_transition.sum())
    abrupt_count = int(abrupt.sum())
    metrics = {
        "landmark_id": int(data["landmark_id"].iloc[0]),
        "coordinate_basis": "smoothed_body_relative_xyz",
        "valid_transitions": valid_transition_count,
        "missing_transitions": int(max(len(data) - 1 - valid_transition_count, 0)),
        "median_frame_displacement": rounded(median_displacement),
        "max_frame_displacement": rounded(maximum_displacement),
        "normalized_trajectory_length": rounded(trajectory_length),
        "displacement_mad": rounded(mad),
        "abrupt_jump_threshold": rounded(abrupt_threshold),
        "abrupt_jump_rule": f"displacement > median + {mad_multiplier:g} x MAD",
        "abrupt_jump_count": abrupt_count,
        "abrupt_jump_rate_percent": rounded(
            100 * abrupt_count / valid_transition_count if valid_transition_count else 0.0,
            2,
        ),
        "abrupt_jump_frames": data.loc[abrupt, "frame"].astype(int).tolist(),
    }
    return metrics, transition_rows


def save_detection_timeline(
    video_name: str,
    hand_frames: pd.DataFrame,
    pose_frames: pd.DataFrame,
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(11, 3.1))
    frame = hand_frames["frame"].to_numpy()
    detected = hand_frames["is_detected"].astype(bool).to_numpy()
    interpolated = hand_frames["is_interpolated"].astype(bool).to_numpy()
    unresolved = hand_frames["is_unresolved"].astype(bool).to_numpy()
    pose_detected = pose_frames["is_detected"].astype(bool).to_numpy()

    ax.scatter(frame[pose_detected], np.full(pose_detected.sum(), 1.0), s=10,
               color="#355c7d", marker="s", label="Pose detected")
    ax.scatter(frame[detected], np.full(detected.sum(), 0.55), s=10,
               color="#2f6b5f", marker="s", label="Hand detected")
    ax.scatter(frame[interpolated], np.full(interpolated.sum(), 0.55), s=34,
               facecolors="none", edgecolors="#d9822b", marker="o",
               linewidths=1.4, label="Hand interpolated")
    ax.scatter(frame[unresolved], np.full(unresolved.sum(), 0.55), s=18,
               color="#8b3a3a", marker="x", label="Hand unresolved")
    ax.set_title(f"{video_name}: landmark detection and gap handling")
    ax.set_xlabel("Frame")
    ax.set_yticks([0.55, 1.0], labels=["Dominant hand", "Pose"])
    ax.set_xlim(-2, int(frame.max()) + 2)
    ax.grid(axis="x", color="#d9dde2", linewidth=0.6)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=4, frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_trajectory(ax: plt.Axes, data: pd.DataFrame, title: str) -> None:
    ordered = data.sort_values("frame")
    ax.plot(ordered["smooth_x"], ordered["smooth_y"], color="#355c7d", linewidth=1.4)
    detected = ordered["is_detected"].astype(bool)
    interpolated = ordered["is_interpolated"].astype(bool)
    ax.scatter(
        ordered.loc[detected, "smooth_x"],
        ordered.loc[detected, "smooth_y"],
        s=8, color="#2f6b5f", alpha=0.55, label="Detected",
    )
    ax.scatter(
        ordered.loc[interpolated, "smooth_x"],
        ordered.loc[interpolated, "smooth_y"],
        s=34, facecolors="none", edgecolors="#d9822b", linewidths=1.3,
        label="Interpolated",
    )
    ax.set_title(title)
    ax.set_xlabel("Normalized x (shoulder widths)")
    ax.set_ylabel("Normalized y (shoulder widths)")
    ax.invert_yaxis()
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(color="#e1e4e8", linewidth=0.6)


def save_wrist_trajectory(data: pd.DataFrame, video_name: str, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    plot_trajectory(ax, data.loc[data["landmark_id"] == 0], "Dominant-hand wrist trajectory")
    ax.legend(frameon=False)
    fig.suptitle(f"{video_name}: body-relative motion", y=1.01, fontsize=13)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_fingertip_trajectories(
    data: pd.DataFrame, video_name: str, output_path: Path
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(12, 7.5))
    fingertip_ids = [4, 8, 12, 16, 20]
    for ax, landmark_id in zip(axes.flat, fingertip_ids):
        plot_trajectory(
            ax,
            data.loc[data["landmark_id"] == landmark_id],
            LANDMARKS[landmark_id].replace("_", " ").title(),
        )
    axes.flat[-1].axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.suptitle(f"{video_name}: body-relative fingertip trajectories", fontsize=13)
    fig.tight_layout(rect=[0, 0.05, 1, 0.96])
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def assess_quality(
    extraction_status: str,
    total_frames: int,
    missing: dict,
    normalization_metadata: dict,
    shoulder_width: pd.Series,
    landmark_metrics: dict,
) -> tuple[list[dict], str, list[str]]:
    unresolved_count = normalization_metadata["interpolation"]["unresolved_frame_count"]
    unresolved_rate = 100 * unresolved_count / total_frames
    unresolved_internal = [
        gap
        for gap in normalization_metadata["interpolation"]["unresolved_gaps"]
        if gap["gap_type"] == "internal"
    ]
    scale_valid_rate = 100 * shoulder_width.notna().sum() / total_frames
    max_abrupt_rate = max(
        metric["abrupt_jump_rate_percent"] for metric in landmark_metrics.values()
    )

    detection_status = (
        "PASS" if extraction_status == "EXTRACTION_PASS"
        else "PARTIAL" if extraction_status == "EXTRACTION_PARTIAL"
        else "FAIL"
    )
    continuity_status = (
        "PASS" if unresolved_count == 0
        else "PARTIAL" if unresolved_rate <= 10
        else "FAIL"
    )
    recoverability_status = (
        "PASS" if not unresolved_internal
        else "PARTIAL" if sum(gap["length_frames"] for gap in unresolved_internal) / total_frames <= 0.1
        else "FAIL"
    )
    normalization_status = (
        "PASS" if scale_valid_rate >= 95
        else "PARTIAL" if scale_valid_rate >= 80
        else "FAIL"
    )
    smoothness_status = (
        "PASS" if max_abrupt_rate <= 5
        else "PARTIAL" if max_abrupt_rate <= 10
        else "FAIL"
    )

    dimensions = [
        {
            "dimension": "A. Detection coverage",
            "status": detection_status,
            "criterion": "PASS requires EXTRACTION_PASS: pose coverage >=95% and hand coverage >=90%.",
            "reason": f"Raw extraction status is {extraction_status}.",
        },
        {
            "dimension": "B. Missing-data continuity",
            "status": continuity_status,
            "criterion": "PASS requires no unresolved frames; PARTIAL permits unresolved frames up to 10% of the sequence.",
            "reason": f"{unresolved_count} frames ({unresolved_rate:.2f}%) remain unresolved.",
        },
        {
            "dimension": "C. Short-gap recoverability",
            "status": recoverability_status,
            "criterion": "PASS requires every internal gap to be reconstructed under the configured maximum; edge gaps are never extrapolated.",
            "reason": (
                "All internal gaps met the conservative interpolation rule."
                if not unresolved_internal
                else f"{len(unresolved_internal)} internal gaps remain unresolved."
            ),
        },
        {
            "dimension": "D. Body-relative stability",
            "status": normalization_status,
            "criterion": "PASS requires a finite, positive shoulder-width reference for at least 95% of frames.",
            "reason": f"A valid shoulder reference was available for {scale_valid_rate:.2f}% of frames.",
        },
        {
            "dimension": "E. Temporal smoothness",
            "status": smoothness_status,
            "criterion": "PASS requires <=5% robustly flagged transitions for every tracked wrist/fingertip; PARTIAL permits <=10%; flags require human inspection and are not accuracy errors.",
            "reason": f"The highest landmark abrupt-transition rate was {max_abrupt_rate:.2f}%.",
        },
        {
            "dimension": "F. Human-inspectable correspondence",
            "status": "PENDING_EXPERT_REVIEW",
            "criterion": "A qualified human reviewer must compare the structured trajectories with the validated reference.",
            "reason": "Diagnostic plots were generated, but professional sign validation is outside the CV layer.",
        },
    ]

    automated_statuses = [item["status"] for item in dimensions[:5]]
    reasons = [
        item["reason"]
        for item in dimensions
        if item["status"] in {"PARTIAL", "FAIL", "PENDING_EXPERT_REVIEW"}
    ]
    if "FAIL" in automated_statuses:
        overall = "MOTION_REPRESENTATION_FAIL"
    else:
        overall = "MOTION_REPRESENTATION_PARTIAL"
    return dimensions, overall, reasons


def analyse_motion(video_name: str, mad_multiplier: float = 6.0) -> dict:
    if mad_multiplier <= 0:
        raise ValueError("mad_multiplier must be positive")

    normalized_dir = Path("poc/output/normalized")
    diagnostics_dir = Path("poc/output/diagnostics")
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    hand_path = normalized_dir / f"{video_name}_hand_normalized.csv"
    pose_path = normalized_dir / f"{video_name}_pose_normalized.csv"
    normalization_path = normalized_dir / f"{video_name}_normalization_metadata.json"
    missing_path = diagnostics_dir / f"{video_name}_missing_frames.json"
    validation_path = Path("poc/output/validation_summary.json")
    for path in (hand_path, pose_path, normalization_path, missing_path, validation_path):
        if not path.exists():
            raise FileNotFoundError(f"Required pipeline input not found: {path}")

    hand_df = pd.read_csv(hand_path)
    pose_df = pd.read_csv(pose_path)
    normalization_metadata = json.loads(normalization_path.read_text(encoding="utf-8"))
    missing = json.loads(missing_path.read_text(encoding="utf-8"))
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    total_frames = int(validation["metrics"]["frames_total"])

    hand_frames = (
        hand_df.groupby("frame", as_index=False)
        .agg(
            is_detected=("is_detected", "all"),
            is_interpolated=("is_interpolated", "all"),
            is_unresolved=("is_unresolved", "any"),
        )
        .sort_values("frame")
    )
    pose_frames = (
        pose_df.groupby("frame", as_index=False)
        .agg(is_detected=("is_detected", "all"))
        .sort_values("frame")
    )

    landmark_metrics = {}
    displacement_rows = []
    for landmark_id, landmark_name in LANDMARKS.items():
        metrics, rows = transition_diagnostics(
            hand_df.loc[hand_df["landmark_id"] == landmark_id],
            landmark_name,
            mad_multiplier,
        )
        landmark_metrics[landmark_name] = metrics
        displacement_rows.extend(rows)

    dimensions, status, status_reasons = assess_quality(
        validation["status"],
        total_frames,
        missing,
        normalization_metadata,
        pose_df.loc[pose_df["landmark_id"] == 11, "shoulder_width"],
        landmark_metrics,
    )

    detection_plot = diagnostics_dir / f"{video_name}_detection_timeline.png"
    wrist_plot = diagnostics_dir / f"{video_name}_wrist_trajectory.png"
    fingertips_plot = diagnostics_dir / f"{video_name}_fingertip_trajectories.png"
    save_detection_timeline(video_name, hand_frames, pose_frames, detection_plot)
    save_wrist_trajectory(hand_df, video_name, wrist_plot)
    save_fingertip_trajectories(hand_df, video_name, fingertips_plot)

    displacement_path = diagnostics_dir / f"{video_name}_motion_displacements.json"
    displacement_payload = {
        "video": video_name,
        "coordinate_basis": "smoothed body-relative xyz",
        "abrupt_jump_rule": f"displacement > median + {mad_multiplier:g} x MAD, calculated per landmark",
        "transitions": displacement_rows,
    }
    displacement_path.write_text(
        json.dumps(displacement_payload, indent=2) + "\n", encoding="utf-8"
    )

    wrist = landmark_metrics["wrist"]
    shoulder_width = pose_df.loc[pose_df["landmark_id"] == 11, "shoulder_width"]
    summary = {
        "video": video_name,
        "extraction": {
            "frames_total": total_frames,
            "hand_detected_frames": int(validation["metrics"]["frames_with_hands"]),
            "hand_detection_rate_percent": validation["metrics"]["hand_detection_rate_percent"],
            "pose_detected_frames": int(validation["metrics"]["frames_with_pose"]),
            "pose_detection_rate_percent": validation["metrics"]["pose_detection_rate_percent"],
            "status": validation["status"],
        },
        "missing_data": {
            "missing_frames_total": missing["summary"]["total_missing_frames"],
            "gap_count": missing["summary"]["gap_count"],
            "longest_gap_frames": missing["summary"]["longest_missing_run_frames"],
            "median_gap_length_frames": missing["summary"]["median_gap_length_frames"],
            "interpolated_frames": normalization_metadata["interpolation"]["interpolated_frame_count"],
            "unresolved_frames": normalization_metadata["interpolation"]["unresolved_frame_count"],
            "interpolated_frame_numbers": normalization_metadata["interpolation"]["interpolated_frames"],
            "unresolved_frame_numbers": normalization_metadata["interpolation"]["unresolved_frames"],
        },
        "normalization": {
            "origin": "shoulder_midpoint",
            "scale": "shoulder_width",
            "valid_shoulder_reference_frames": int(shoulder_width.notna().sum()),
            "median_shoulder_width": rounded(shoulder_width.median()),
            "shoulder_width_mad": rounded(
                (shoulder_width - shoulder_width.median()).abs().median()
            ),
            "statement": "Body-relative normalization reduces sensitivity to performer position and apparent scale.",
            "viewpoint_limitation": "The representation is not fully viewpoint invariant.",
            "smoothing_window_frames": normalization_metadata["smoothing"]["window_frames"],
        },
        "motion": {
            "coordinate_basis": wrist["coordinate_basis"],
            "wrist_trajectory_length": wrist["normalized_trajectory_length"],
            "median_frame_displacement": wrist["median_frame_displacement"],
            "max_frame_displacement": wrist["max_frame_displacement"],
            "missing_transitions": wrist["missing_transitions"],
            "abrupt_jump_count": wrist["abrupt_jump_count"],
            "abrupt_jump_threshold": wrist["abrupt_jump_threshold"],
            "abrupt_jump_rule": wrist["abrupt_jump_rule"],
            "landmarks": landmark_metrics,
        },
        "quality_assessment": dimensions,
        "status": status,
        "status_reasons": status_reasons,
        "technical_feasibility": {
            "decision": "Proceed with conditions" if status != "MOTION_REPRESENTATION_FAIL" else "Stop",
            "conditions": [
                "Professional sign validation remains mandatory.",
                "Leading, trailing, and long internal gaps must remain unresolved rather than extrapolated.",
                "The representation must be tested across multiple signs, performers, capture conditions, and viewpoints.",
                "Future rendering and motion-preservation fidelity remain untested.",
            ],
        },
        "interpretation": (
            "The observed dominant-hand motion can be represented as body-relative, "
            "temporally ordered landmarks for further controlled experimentation. "
            "The current single-video evidence remains partial because edge gaps are "
            "unresolved and human correspondence has not been professionally reviewed."
        ),
        "human_validation_checkpoint": (
            "Computer Vision can quantify and structure observed movement. It cannot "
            "determine whether the sign is professionally correct without expert review."
        ),
        "limitations": [
            "Single adult reference video; no cross-video or cross-performer generalization test.",
            "No proof of linguistic, Baby Sign, ASL, LSE, clinical, or developmental correctness.",
            "No semantic sign recognition.",
            "No full viewpoint invariance.",
            "No avatar generation, motion retargeting, or synthetic-video fidelity test.",
            "Unresolved edge gaps are retained as missing data.",
            "Abrupt-jump flags are detector diagnostics, not an accuracy measure.",
        ],
        "artifacts": {
            "missing_frames": str(missing_path),
            "transition_evidence": str(displacement_path),
            "detection_timeline": str(detection_plot),
            "wrist_trajectory": str(wrist_plot),
            "fingertip_trajectories": str(fingertips_plot),
        },
    }
    summary_path = diagnostics_dir / f"{video_name}_motion_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Motion summary saved: {summary_path}")
    print(f"Status: {status}")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse normalized dominant-hand motion and generate diagnostics."
    )
    parser.add_argument("--video-name", default="sign_reference")
    parser.add_argument("--abrupt-jump-mad-multiplier", type=float, default=6.0)
    arguments = parser.parse_args()
    analyse_motion(arguments.video_name, arguments.abrupt_jump_mad_multiplier)
