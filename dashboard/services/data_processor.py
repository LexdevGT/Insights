import os
import pandas as pd
from django.conf import settings

def process_data_files():
    data_dir = settings.DATA_DIR
    files = os.listdir(data_dir)
    processed_data = []

    for file in files:
        file_path = os.path.join(data_dir, file)
        try:
            if file.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.endswith('.xlsx') or file.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                continue

            processed_data.append({
                'file_name': file,
                'columns': df.columns.tolist(),
                'shape': df.shape,
            })
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    return processed_data