import os
import pandas as pd
import numpy as np

def normalize_and_smooth(video_name, window_size=3):
    pose_path = f"poc/output/landmarks/{video_name}_pose_landmarks.csv"
    hand_path = f"poc/output/landmarks/{video_name}_hand_landmarks.csv"
    
    if not os.path.exists(pose_path) or not os.path.exists(hand_path):
        print(f"Error: Required CSV files for {video_name} not found.")
        return

    df_pose = pd.read_csv(pose_path)
    df_hand = pd.read_csv(hand_path)

    # 1. Calcular el centro de los hombros (IDs 11 y 12 en MediaPipe) como punto cero
    shoulder_left = df_pose[df_pose['landmark_id'] == 11][['frame', 'x', 'y', 'z']]
    shoulder_right = df_pose[df_pose['landmark_id'] == 12][['frame', 'x', 'y', 'z']]
    
    shoulders = pd.merge(shoulder_left, shoulder_right, on='frame', suffixes=('_l', '_r'))
    shoulders['center_x'] = (shoulders['x_l'] + shoulders['x_r']) / 2
    shoulders['center_y'] = (shoulders['y_l'] + shoulders['y_r']) / 2
    shoulders['center_z'] = (shoulders['z_l'] + shoulders['z_r']) / 2

    # 2. Centrar coordenadas de Pose respecto al torso
    df_pose = df_pose.merge(shoulders[['frame', 'center_x', 'center_y', 'center_z']], on='frame', how='left')
    df_pose['norm_x'] = df_pose['x'] - df_pose['center_x']
    df_pose['norm_y'] = df_pose['y'] - df_pose['center_y']
    df_pose['norm_z'] = df_pose['z'] - df_pose['center_z']

    # 3. Centrar coordenadas de Manos respecto al torso
    df_hand = df_hand.merge(shoulders[['frame', 'center_x', 'center_y', 'center_z']], on='frame', how='left')
    df_hand['norm_x'] = df_hand['x'] - df_hand['center_x']
    df_hand['norm_y'] = df_hand['y'] - df_hand['center_y']
    df_hand['norm_z'] = df_hand['z'] - df_hand['center_z']

    # 4. Rellenar fotogramas faltantes e interpolar suaves
    for col in ['norm_x', 'norm_y', 'norm_z']:
        df_pose[col] = df_pose.groupby('landmark_id')[col].transform(
            lambda x: x.interpolate(method='linear').rolling(window_size, min_periods=1).mean()
        )
        if not df_hand.empty:
            df_hand[col] = df_hand.groupby(['hand', 'landmark_id'])[col].transform(
                lambda x: x.interpolate(method='linear').rolling(window_size, min_periods=1).mean()
            )

    # 5. Exportar CSVs normalizados
    output_dir = "poc/output/normalized"
    os.makedirs(output_dir, exist_ok=True)
    
    output_pose_path = f"{output_dir}/{video_name}_pose_normalized.csv"
    output_hand_path = f"{output_dir}/{video_name}_hand_normalized.csv"
    
    df_pose.to_csv(output_pose_path, index=False)
    df_hand.to_csv(output_hand_path, index=False)
    
    print(f"Normalization complete.")
    print(f"Saved pose landmarks: {output_pose_path}")
    print(f"Saved hand landmarks: {output_hand_path}")

if __name__ == "__main__":
    normalize_and_smooth("sign_reference")