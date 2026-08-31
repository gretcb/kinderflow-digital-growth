import json
import pandas as pd

def generate_validation_summary(video_name, total_frames, hand_data, pose_data):
    hand_df = pd.DataFrame(hand_data)
    pose_df = pd.DataFrame(pose_data)
    
    frames_with_pose = pose_df['frame'].nunique() if not pose_df.empty else 0
    pose_detection_rate = (frames_with_pose / total_frames) * 100 if total_frames > 0 else 0
    
    frames_with_hands = hand_df['frame'].nunique() if not hand_df.empty else 0
    hand_detection_rate = (frames_with_hands / total_frames) * 100 if total_frames > 0 else 0
    
    frames_with_left = hand_df[hand_df['hand'] == 'Left']['frame'].nunique() if not hand_df.empty else 0
    frames_with_right = hand_df[hand_df['hand'] == 'Right']['frame'].nunique() if not hand_df.empty else 0
    missing_frames = total_frames - frames_with_hands
    
    if hand_detection_rate > 50 and pose_detection_rate > 80:
        status = "PASS"
        notes = ["Sufficient technical landmark stability for motion tracking."]
    elif hand_detection_rate > 20:
        status = "PARTIAL"
        notes = ["Motion captured, but hand detection rate is low."]
    else:
        status = "FAIL"
        notes = ["Failed to capture meaningful hand motion data."]

    summary = {
        "video": video_name,
        "metrics": {
            "frames_total": total_frames,
            "frames_with_hands": frames_with_hands,
            "hand_detection_rate_percent": round(hand_detection_rate, 2),
            "frames_with_pose": frames_with_pose,
            "pose_detection_rate_percent": round(pose_detection_rate, 2),
            "frames_with_left_hand": frames_with_left,
            "frames_with_right_hand": frames_with_right,
            "missing_frames": missing_frames
        },
        "status": status,
        "notes": notes
    }
    
    output_path = "poc/output/validation_summary.json"
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=4)
        
    print(f"Validation summary generated at {output_path}")
    print(f"Status: {status}")
