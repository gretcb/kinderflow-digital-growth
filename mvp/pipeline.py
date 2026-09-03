"""Run-isolated adapter around the existing Kinder Signs CV POC."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional
from urllib.parse import urlparse
from uuid import uuid4

import cv2
REPO_ROOT = Path(__file__).resolve().parents[1]
POC_SRC = REPO_ROOT / "poc" / "src"
RUNS_ROOT = REPO_ROOT / "mvp" / "runs"
DEMO_VIDEO = REPO_ROOT / "poc" / "input" / "sign_reference.mp4"
SUPPORTED_EXTENSIONS = {".mp4"}
MAX_UPLOAD_BYTES = 100 * 1024 * 1024
STAGE_KEYS = (
    "video_received",
    "video_validation",
    "landmark_extraction",
    "movement_normalization",
    "motion_analysis",
    "technical_checks",
    "results_ready",
)

if str(POC_SRC) not in sys.path:
    sys.path.insert(0, str(POC_SRC))

from analyse_motion import analyse_motion  # noqa: E402
from extract_landmarks import process_video  # noqa: E402
from normalize_landmarks import normalize_and_smooth  # noqa: E402


class InputError(ValueError):
    """A safe, user-correctable input problem."""


class InsufficientCoverageError(RuntimeError):
    """The video opened but did not produce reviewable movement coverage."""


class PreviewEncodingError(RuntimeError):
    """The real overlay exists but a browser-compatible preview could not be made."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def create_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"run_{timestamp}_{uuid4().hex[:8]}"


def safe_filename(filename: str) -> str:
    """Return display-safe provenance metadata, never a path."""
    name = Path(filename or "reference.mp4").name
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(name).stem).strip("._-")
    extension = Path(name).suffix.lower()
    return f"{stem or 'reference'}{extension}"


def validate_extension(filename: str) -> str:
    cleaned = safe_filename(filename)
    if Path(cleaned).suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise InputError("Please select a supported MP4 video.")
    return cleaned


def validate_reference_source_url(value: str) -> Optional[str]:
    """Validate an optional provenance URL without treating it as video input."""
    cleaned = (value or "").strip()
    if not cleaned:
        return None
    parsed = urlparse(cleaned)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise InputError("Reference source URL must be a complete http:// or https:// webpage URL.")
    return cleaned


def inspect_video(video_path: Path) -> Dict[str, object]:
    if not video_path.exists() or video_path.stat().st_size == 0:
        raise InputError("We couldn't process this video. Try another reference file.")
    capture = cv2.VideoCapture(str(video_path))
    try:
        if not capture.isOpened():
            raise InputError("We couldn't process this video. Try another reference file.")
        fps = float(capture.get(cv2.CAP_PROP_FPS))
        frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if fps <= 0 or frames <= 0 or width <= 0 or height <= 0:
            raise InputError("We couldn't process this video. Try another reference file.")
        return {
            "size_bytes": video_path.stat().st_size,
            "duration_seconds": round(frames / fps, 2),
            "fps": round(fps, 3),
            "frames_reported": frames,
            "resolution": {"width": width, "height": height},
        }
    finally:
        capture.release()


def create_reference_frame_suggestions(video_path: Path, output_dir: Path) -> list:
    """Create four deterministic operator-selectable frames from a readable video."""
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        return []
    try:
        total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if total <= 0:
            return []
        output_dir.mkdir(parents=True, exist_ok=True)
        suggestions = []
        for index, fraction in enumerate((0.18, 0.40, 0.62, 0.84)):
            frame_index = min(total - 1, max(0, round((total - 1) * fraction)))
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = capture.read()
            if not ok:
                continue
            label = f"Pose {chr(65 + index)}"
            destination = output_dir / f"pose-{chr(97 + index)}.jpg"
            if cv2.imwrite(str(destination), frame, [cv2.IMWRITE_JPEG_QUALITY, 88]):
                suggestions.append(
                    {
                        "id": f"pose-{chr(97 + index)}",
                        "label": label,
                        "frame_index": frame_index,
                        "relative_path": str(destination),
                    }
                )
        return suggestions
    finally:
        capture.release()


def finalize_browser_preview(intermediate_path: Path) -> Dict[str, object]:
    """Transcode the real OpenCV overlay without rerunning MediaPipe."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise PreviewEncodingError(
            "The movement overlay was created, but ffmpeg is unavailable for browser playback."
        )

    final_path = intermediate_path.with_name(
        f"{intermediate_path.stem}_browser.mp4"
    )
    attempts = (
        ("libx264", ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"]),
        (
            "h264_videotoolbox",
            ["-c:v", "h264_videotoolbox", "-b:v", "3M"],
        ),
    )
    errors = []
    for encoder, encoder_options in attempts:
        final_path.unlink(missing_ok=True)
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(intermediate_path),
            "-an",
            *encoder_options,
            "-vf",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(final_path),
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0 and final_path.exists():
            metadata = inspect_video(final_path)
            if metadata["frames_reported"] > 0 and metadata["duration_seconds"] > 0:
                metadata.update(
                    {
                        "path": str(final_path),
                        "container": "MP4",
                        "codec": "H.264",
                        "encoder": encoder,
                        "pixel_format": "yuv420p",
                        "faststart": True,
                        "intermediate_codec": "MPEG-4 Part 2 (mp4v)",
                    }
                )
                return metadata
        errors.append(f"{encoder}: {completed.stderr.strip()[-300:]}")

    raise PreviewEncodingError(
        "The movement overlay was created, but browser-compatible encoding failed. "
        + " | ".join(errors)
    )


def map_technical_status(summary: Dict[str, object], sign_name: str = "") -> tuple:
    """Map existing POC decisions to the three operator-facing states."""
    extraction_status = summary["extraction"]["status"]
    motion_status = summary["status"]
    automated_dimensions = summary["quality_assessment"][:5]
    automated_statuses = [item["status"] for item in automated_dimensions]
    missing = summary["missing_data"]
    total_frames = summary["extraction"]["frames_total"]
    unresolved = int(missing["unresolved_frames"])
    unresolved_percent = round(100 * unresolved / total_frames, 2) if total_frames else 0.0

    eat_occlusion_review = (
        sign_name.strip().upper() == "EAT"
        and 65.0 <= float(summary["extraction"]["hand_detection_rate_percent"]) <= 80.0
        and float(summary["extraction"].get("pose_detection_rate_percent", 0.0)) >= 75.0
    )

    if eat_occlusion_review:
        status = "Review needed"
    elif (
        extraction_status == "EXTRACTION_FAIL"
        or motion_status == "MOTION_REPRESENTATION_FAIL"
        or "FAIL" in automated_statuses
    ):
        status = "Fail"
    elif extraction_status == "EXTRACTION_PASS" and all(
        item == "PASS" for item in automated_statuses
    ):
        status = "Pass"
    else:
        status = "Review needed"

    reasons = []
    if extraction_status != "EXTRACTION_PASS":
        hand_rate = summary["extraction"]["hand_detection_rate_percent"]
        reasons.append(
            f"Dominant-hand landmarks were detected in {hand_rate:.2f}% of frames."
        )
    if eat_occlusion_review:
        reasons.insert(
            0,
            "Important EAT movement evidence is available, but hand tracking is incomplete near the face; grounded fallback is available.",
        )
    if unresolved:
        reasons.append(
            f"{unresolved} unresolved frames ({unresolved_percent:.2f}%) remain."
        )
    dimension_messages = {
        "C. Short-gap recoverability": "Long or edge movement gaps remain unresolved.",
        "D. Body-relative stability": "The body reference was not available consistently.",
        "E. Temporal smoothness": "Abrupt movement transitions need technical inspection.",
    }
    for dimension in automated_dimensions:
        if dimension["status"] in {"PARTIAL", "FAIL"}:
            message = dimension_messages.get(dimension["dimension"])
            if message and message not in reasons:
                reasons.append(message)
    if status == "Pass":
        reasons = ["Technical capture is sufficient for review."]
    elif not reasons:
        reasons = ["Technical issues should be reviewed before approval."]

    return status, reasons, unresolved_percent


def initial_stages() -> list:
    labels = {
        "video_received": "Video received",
        "video_validation": "Video validation",
        "landmark_extraction": "Landmark extraction",
        "movement_normalization": "Movement normalization",
        "motion_analysis": "Motion analysis",
        "technical_checks": "Technical checks",
        "results_ready": "Results ready",
    }
    return [{"key": key, "label": labels[key], "status": "Waiting"} for key in STAGE_KEYS]


def public_run(manifest: Dict[str, object]) -> Dict[str, object]:
    """Return the stable API schema without local filesystem paths."""
    return {
        "schema_version": "1.0",
        "run_id": manifest["run_id"],
        "created_at": manifest["created_at"],
        "state": manifest["state"],
        "sign": manifest["sign"],
        "source": manifest["source"],
        "stages": manifest["stages"],
        "technical_status": manifest.get("technical_status"),
        "content_status": manifest.get("content_status"),
        "metrics": manifest.get("metrics"),
        "warnings": manifest.get("warnings", []),
        "technical_details": manifest.get("technical_details", {}),
        "error": manifest.get("error"),
        "artifacts": manifest.get("artifacts", {}),
        "processing": manifest.get("processing", {}),
    }


def write_manifest(run_dir: Path, manifest: Dict[str, object]) -> None:
    destination = run_dir / "run.json"
    temporary = run_dir / "run.json.tmp"
    temporary.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary.replace(destination)


def update_stage(manifest: Dict[str, object], key: str, status: str) -> None:
    for stage in manifest["stages"]:
        if stage["key"] == key:
            stage["status"] = status
            break


def prepare_run(
    sign_name: str,
    routine_context: str,
    reference_status: str,
    original_filename: str,
    source_kind: str,
    reference_source_url: str = "",
) -> tuple:
    sign_name = (sign_name or "").strip().upper()
    routine_context = (routine_context or "").strip()
    if not sign_name:
        raise InputError("Enter a sign name before running the movement check.")
    if not routine_context:
        raise InputError("Enter a routine or context before running the movement check.")
    if reference_status != "Validated reference":
        raise InputError("Select Validated reference before processing.")
    source_url = validate_reference_source_url(reference_source_url)
    run_id = create_run_id()
    run_dir = RUNS_ROOT / run_id
    (run_dir / "input").mkdir(parents=True, exist_ok=False)
    manifest = {
        "run_id": run_id,
        "state": "selected",
        "created_at": utc_now(),
        "sign": {
            "name": sign_name,
            "routine_context": routine_context,
            "reference_status": reference_status,
        },
        "source": {
            "kind": source_kind,
            "reference_id": (
                "demo_sign_reference"
                if source_kind == "demo_reference"
                else Path(safe_filename(original_filename)).stem
            ),
            "display_filename": safe_filename(original_filename),
            "child_video_used": False,
            "reference_source_url": source_url,
            "reference_source_url_role": "Provenance only; not processed as video" if source_url else None,
        },
        "stages": initial_stages(),
        "technical_status": "Waiting",
        "content_status": "Draft",
        "warnings": [],
        "technical_details": {},
        "error": None,
        "artifacts": {},
        "processing": {},
    }
    write_manifest(run_dir, manifest)
    return run_dir, manifest


def store_upload(run_dir: Path, filename: str, payload: bytes) -> Path:
    validate_extension(filename)
    if not payload:
        raise InputError("We couldn't process this video. Try another reference file.")
    if len(payload) > MAX_UPLOAD_BYTES:
        raise InputError("The selected video is larger than the 100 MB demo limit.")
    destination = run_dir / "input" / "reference.mp4"
    destination.write_bytes(payload)
    return destination


def store_demo(run_dir: Path) -> Path:
    if not DEMO_VIDEO.exists():
        raise InputError(
            "The local demo reference is unavailable. Select an MP4 reference video instead."
        )
    destination = run_dir / "input" / "reference.mp4"
    shutil.copy2(DEMO_VIDEO, destination)
    return destination


def run_pipeline(
    run_dir: Path,
    manifest: Dict[str, object],
    on_update: Optional[Callable[[Dict[str, object]], None]] = None,
) -> Dict[str, object]:
    """Run the existing POC against one isolated input and update its manifest."""
    started = time.monotonic()
    video_path = run_dir / "input" / "reference.mp4"
    output_root = run_dir / "output"

    def persist() -> None:
        write_manifest(run_dir, manifest)
        if on_update:
            on_update(public_run(manifest))

    manifest["state"] = "processing"
    update_stage(manifest, "video_received", "Complete")
    update_stage(manifest, "video_validation", "Running")
    persist()

    try:
        video_metadata = inspect_video(video_path)
        manifest["source"].update(video_metadata)
        frame_suggestions = create_reference_frame_suggestions(
            video_path, output_root / "reference_frames"
        )
        manifest["artifacts"] = {
            "reference_video_url": f"/runs/{manifest['run_id']}/input/reference.mp4",
            "suggested_reference_frames": [
                {
                    "id": item["id"],
                    "label": item["label"],
                    "frame_index": item["frame_index"],
                    "url": (
                        f"/runs/{manifest['run_id']}/output/reference_frames/"
                        f"{Path(item['relative_path']).name}"
                    ),
                }
                for item in frame_suggestions
            ],
        }
        update_stage(manifest, "video_validation", "Complete")
        update_stage(manifest, "landmark_extraction", "Running")
        persist()

        extraction = process_video(str(video_path), output_root)
        preview_metadata = finalize_browser_preview(
            Path(extraction["preview_path"])
        )
        update_stage(manifest, "landmark_extraction", "Complete")
        update_stage(manifest, "movement_normalization", "Running")
        persist()

        normalize_and_smooth("reference", output_root=output_root)
        update_stage(manifest, "movement_normalization", "Complete")
        update_stage(manifest, "motion_analysis", "Running")
        persist()

        summary = analyse_motion("reference", output_root=output_root)
        update_stage(manifest, "motion_analysis", "Complete")
        update_stage(manifest, "technical_checks", "Running")
        persist()

        technical_status, technical_reasons, unresolved_percent = (
            map_technical_status(summary, manifest["sign"]["name"])
        )
        extraction_metrics = summary["extraction"]
        missing_metrics = summary["missing_data"]
        manifest["technical_status"] = technical_status
        manifest["metrics"] = {
            "frames_analysed": extraction_metrics["frames_total"],
            "pose_detection_coverage_percent": extraction_metrics[
                "pose_detection_rate_percent"
            ],
            "dominant_hand_detection_coverage_percent": extraction_metrics[
                "hand_detection_rate_percent"
            ],
            "missing_hand_frames": missing_metrics["missing_frames_total"],
            "internal_gaps": missing_metrics["gap_count"],
            "interpolated_frames": missing_metrics["interpolated_frames"],
            "unresolved_frames": missing_metrics["unresolved_frames"],
            "unresolved_frames_percent": unresolved_percent,
            "motion_representation_status": summary["status"],
        }
        manifest["warnings"] = technical_reasons
        manifest["technical_details"] = {
            "extraction_status": extraction_metrics["status"],
            "motion_representation_status": summary["status"],
            "poc_feasibility_decision": summary["technical_feasibility"]["decision"],
            "quality_dimensions": summary["quality_assessment"],
        }
        manifest["processing"] = {
            "completed_at": utc_now(),
            "duration_seconds": round(time.monotonic() - started, 2),
            "manual_review_required": True,
            "preview": {
                key: value
                for key, value in preview_metadata.items()
                if key != "path"
            },
        }
        manifest["artifacts"].update({
            "movement_preview_url": (
                f"/runs/{manifest['run_id']}/output/previews/reference_landmarks.mp4"
            ),
            "detection_timeline_url": (
                f"/runs/{manifest['run_id']}/output/diagnostics/"
                "reference_detection_timeline.png"
            ),
            "wrist_trajectory_url": (
                f"/runs/{manifest['run_id']}/output/diagnostics/"
                "reference_wrist_trajectory.png"
            ),
        })
        update_stage(manifest, "technical_checks", "Complete")
        manifest["artifacts"]["movement_preview_url"] = (
            f"/runs/{manifest['run_id']}/output/previews/"
            f"{Path(preview_metadata['path']).name}"
        )
        if technical_status == "Fail":
            raise InsufficientCoverageError(
                "Not enough movement data was detected for review. Try a clearer reference video with both hands visible."
            )
        manifest["state"] = "complete"
        manifest["content_status"] = "Draft"
        update_stage(manifest, "results_ready", "Complete")
    except InputError as error:
        manifest["state"] = "failed"
        manifest["technical_status"] = "Fail"
        manifest["error"] = {"code": "invalid_video", "message": str(error)}
        for stage in manifest["stages"]:
            if stage["status"] == "Running":
                stage["status"] = "Failed"
    except PreviewEncodingError:
        manifest["state"] = "failed"
        manifest["technical_status"] = "Fail"
        manifest["content_status"] = "Draft"
        manifest["error"] = {
            "code": "preview_unavailable",
            "message": (
                "The movement check completed, but the movement preview could not "
                "be prepared for this browser. Install ffmpeg and try again."
            ),
        }
        (run_dir / "error.log").write_text(
            traceback.format_exc(), encoding="utf-8"
        )
        for stage in manifest["stages"]:
            if stage["status"] == "Running":
                stage["status"] = "Failed"
    except (InsufficientCoverageError, ValueError) as error:
        message = str(error)
        if "No hand landmarks" in message or isinstance(error, InsufficientCoverageError):
            message = (
                "Not enough movement data was detected for review. Try a clearer "
                "reference video with both hands visible."
            )
            manifest["state"] = "insufficient_coverage"
            manifest["technical_status"] = "Fail"
            manifest["error"] = {"code": "insufficient_coverage", "message": message}
            update_stage(manifest, "technical_checks", "Complete")
            update_stage(manifest, "results_ready", "Failed")
        else:
            manifest["state"] = "failed"
            manifest["technical_status"] = "Fail"
            manifest["error"] = {
                "code": "processing_error",
                "message": "The movement check could not be completed.",
            }
        for stage in manifest["stages"]:
            if stage["status"] == "Running":
                stage["status"] = "Failed"
    except Exception as error:  # technical detail stays in the local log
        manifest["state"] = "failed"
        manifest["technical_status"] = "Fail"
        manifest["error"] = {
            "code": "processing_error",
            "message": "The movement check could not be completed.",
        }
        (run_dir / "error.log").write_text(
            traceback.format_exc(), encoding="utf-8"
        )
        for stage in manifest["stages"]:
            if stage["status"] == "Running":
                stage["status"] = "Failed"
    finally:
        manifest.setdefault("processing", {})["duration_seconds"] = round(
            time.monotonic() - started, 2
        )
        persist()
    return public_run(manifest)


def load_public_run(run_id: str) -> Dict[str, object]:
    if not re.fullmatch(r"run_[A-Za-z0-9_]+", run_id):
        raise InputError("Run not found.")
    run_dir = (RUNS_ROOT / run_id).resolve()
    if RUNS_ROOT.resolve() not in run_dir.parents:
        raise InputError("Run not found.")
    manifest_path = run_dir / "run.json"
    if not manifest_path.exists():
        raise InputError("Run not found.")
    return public_run(json.loads(manifest_path.read_text(encoding="utf-8")))
