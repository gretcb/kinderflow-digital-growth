import json
import os
from pathlib import Path

import pandas as pd

def save_metadata(metadata, output_path):
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def save_landmarks_csv(data_list, output_path):
    if not data_list:
        df = pd.DataFrame(columns=['frame', 'timestamp_ms', 'landmark_id', 'x', 'y', 'z', 'visibility'])
    else:
        df = pd.DataFrame(data_list)
    df.to_csv(output_path, index=False)
    
def ensure_directories_exist(output_root="poc/output"):
    """Create extraction directories below the requested output root.

    The default preserves the original POC paths. The MVP supplies an isolated
    run directory so live processing cannot overwrite the canonical evidence.
    """
    root = Path(output_root)
    for directory in (root / "landmarks", root / "previews"):
        os.makedirs(directory, exist_ok=True)
