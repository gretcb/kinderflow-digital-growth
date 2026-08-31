"""Validate raw MediaPipe extraction coverage without inferring motion fidelity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


POSE_PASS_PERCENT = 95.0
HAND_PASS_PERCENT = 90.0
HAND_PARTIAL_PERCENT = 70.0


def evaluate_extraction_status(
    hand_detection_rate: float, pose_detection_rate: float
) -> tuple[str, list[str]]:
    """Return a coverage-only status and evidence-led notes."""
    if (
        pose_detection_rate >= POSE_PASS_PERCENT
        and hand_detection_rate >= HAND_PASS_PERCENT
    ):
        return (
            "EXTRACTION_PASS",
            [
                "Landmark extraction coverage is sufficient for downstream motion analysis.",
                "Coverage alone does not establish motion fidelity or sign correctness.",
            ],
        )
    if hand_detection_rate >= HAND_PARTIAL_PERCENT:
        return (
            "EXTRACTION_PARTIAL",
            [
                "Hand landmark coverage supports limited downstream analysis, with missing-data constraints.",
                "Coverage alone does not establish motion fidelity or sign correctness.",
            ],
        )
    return (
        "EXTRACTION_FAIL",
        [
            "Hand landmark coverage is insufficient for the planned downstream motion analysis.",
            "Coverage alone does not establish motion fidelity or sign correctness.",
        ],
    )


def generate_validation_summary(
    video_name: str,
    total_frames: int,
    hand_data: list[dict] | pd.DataFrame,
    pose_data: list[dict] | pd.DataFrame,
    output_path: str | Path = "poc/output/validation_summary.json",
) -> dict:
    hand_df = hand_data.copy() if isinstance(hand_data, pd.DataFrame) else pd.DataFrame(hand_data)
    pose_df = pose_data.copy() if isinstance(pose_data, pd.DataFrame) else pd.DataFrame(pose_data)

    frames_with_pose = pose_df["frame"].nunique() if not pose_df.empty else 0
    frames_with_hands = hand_df["frame"].nunique() if not hand_df.empty else 0
    pose_detection_rate = 100 * frames_with_pose / total_frames if total_frames else 0.0
    hand_detection_rate = 100 * frames_with_hands / total_frames if total_frames else 0.0
    frames_with_left = (
        hand_df.loc[hand_df["hand"] == "Left", "frame"].nunique()
        if not hand_df.empty
        else 0
    )
    frames_with_right = (
        hand_df.loc[hand_df["hand"] == "Right", "frame"].nunique()
        if not hand_df.empty
        else 0
    )
    status, notes = evaluate_extraction_status(
        hand_detection_rate, pose_detection_rate
    )

    summary = {
        "video": video_name,
        "assessment_scope": "raw_landmark_extraction_coverage",
        "metrics": {
            "frames_total": int(total_frames),
            "frames_with_hands": int(frames_with_hands),
            "hand_detection_rate_percent": round(hand_detection_rate, 2),
            "frames_with_pose": int(frames_with_pose),
            "pose_detection_rate_percent": round(pose_detection_rate, 2),
            "frames_with_left_hand": int(frames_with_left),
            "frames_with_right_hand": int(frames_with_right),
            "missing_frames": int(total_frames - frames_with_hands),
        },
        "criteria": {
            "EXTRACTION_PASS": {
                "pose_coverage_percent_min": POSE_PASS_PERCENT,
                "hand_coverage_percent_min": HAND_PASS_PERCENT,
            },
            "EXTRACTION_PARTIAL": {
                "hand_coverage_percent_min": HAND_PARTIAL_PERCENT
            },
            "EXTRACTION_FAIL": "hand coverage below the partial threshold",
        },
        "status": status,
        "notes": notes,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Validation summary generated at {output_path}")
    print(f"Status: {status}")
    return summary


def validate_existing_output(video_name: str) -> dict:
    landmarks_dir = Path("poc/output/landmarks")
    metadata = json.loads(
        (landmarks_dir / f"{video_name}_metadata.json").read_text(encoding="utf-8")
    )
    hand_df = pd.read_csv(landmarks_dir / f"{video_name}_hand_landmarks.csv")
    pose_df = pd.read_csv(landmarks_dir / f"{video_name}_pose_landmarks.csv")
    total_frames = int(metadata["total_frames_metadata"])
    return generate_validation_summary(video_name, total_frames, hand_df, pose_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Assess raw MediaPipe extraction coverage."
    )
    parser.add_argument("--video-name", default="sign_reference")
    args = parser.parse_args()
    validate_existing_output(args.video_name)
