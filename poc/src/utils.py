import json
import pandas as pd
import os

def save_metadata(metadata, output_path):
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def save_landmarks_csv(data_list, output_path):
    if not data_list:
        df = pd.DataFrame(columns=['frame', 'timestamp_ms', 'landmark_id', 'x', 'y', 'z', 'visibility'])
    else:
        df = pd.DataFrame(data_list)
    df.to_csv(output_path, index=False)
    
def ensure_directories_exist():
    for d in ["poc/output/landmarks", "poc/output/previews"]:
        os.makedirs(d, exist_ok=True)
