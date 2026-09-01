import cv2
import argparse
import os
from pathlib import Path
import mediapipe as mp

from utils import save_metadata, save_landmarks_csv, ensure_directories_exist
from validate_output import generate_validation_summary

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_video(video_path, output_root="poc/output"):
    """Extract landmarks using the original Holistic pipeline.

    ``output_root`` defaults to the Round 1 location for full CLI backwards
    compatibility. Callers such as the MVP can provide an isolated run root.
    """
    output_root = Path(output_root)
    ensure_directories_exist(output_root)
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError("Could not open the reference video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    metadata = {
        "video_name": video_name,
        "fps": fps,
        "resolution": {"width": width, "height": height},
        "total_frames_metadata": total_frames
    }

    preview_path = output_root / "previews" / f"{video_name}_landmarks.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(preview_path, fourcc, fps if fps > 0 else 30, (width, height))
    if not out.isOpened():
        cap.release()
        raise RuntimeError("Could not create the landmark preview video")

    hand_data = []
    pose_data = []
    frame_idx = 0

    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image_rgb)
            image.flags.writeable = True

            if results.pose_landmarks:
                for idx, lm in enumerate(results.pose_landmarks.landmark):
                    pose_data.append({
                        "frame": frame_idx,
                        "timestamp_ms": round(timestamp_ms, 2),
                        "landmark_id": idx,
                        "x": lm.x,
                        "y": lm.y,
                        "z": lm.z,
                        "visibility": getattr(lm, 'visibility', 0.0)
                    })

            for hand_results, hand_label in zip(
                [results.left_hand_landmarks, results.right_hand_landmarks], 
                ["Left", "Right"]
            ):
                if hand_results:
                    for idx, lm in enumerate(hand_results.landmark):
                        hand_data.append({
                            "frame": frame_idx,
                            "timestamp_ms": round(timestamp_ms, 2),
                            "hand": hand_label,
                            "landmark_id": idx,
                            "x": lm.x,
                            "y": lm.y,
                            "z": lm.z,
                            "visibility": getattr(lm, 'visibility', 0.0)
                        })

            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            mp_drawing.draw_landmarks(
                image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())
            mp_drawing.draw_landmarks(
                image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())

            out.write(image)
            frame_idx += 1

    cap.release()
    out.release()

    landmarks_dir = output_root / "landmarks"
    save_metadata(metadata, landmarks_dir / f"{video_name}_metadata.json")
    save_landmarks_csv(pose_data, landmarks_dir / f"{video_name}_pose_landmarks.csv")
    save_landmarks_csv(hand_data, landmarks_dir / f"{video_name}_hand_landmarks.csv")
    
    print(f"Extraction complete. Processed {frame_idx} frames.")
    validation = generate_validation_summary(
        video_name,
        frame_idx,
        hand_data,
        pose_data,
        output_root / "validation_summary.json",
    )
    return {
        "video_name": video_name,
        "frames_processed": frame_idx,
        "preview_path": str(preview_path),
        "validation": validation,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract landmarks from reference sign video.")
    parser.add_argument("--video", type=str, required=True, help="Path to the input video file")
    parser.add_argument(
        "--output-root",
        default="poc/output",
        help="Output directory (defaults to the canonical POC output path)",
    )
    args = parser.parse_args()
    
    process_video(args.video, args.output_root)
