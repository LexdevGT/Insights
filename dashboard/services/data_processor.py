import os
import pandas as pd
from django.conf import settings
from datetime import datetime

def calculate_developer_metrics(data, developer):
    dev_data = data[data['developer'] == developer]

    total_tasks = len(dev_data)
    total_sp = dev_data['story_points'].sum()

    bugs = dev_data[dev_data['Tipo de Incidencia'].str.contains('Bug', na=False, case=False)]
    bug_ratio = len(bugs) / total_tasks if total_tasks > 0 else 0

    avg_completion_time = dev_data['time_to_complete'].mean()
    sp_per_day = total_sp / dev_data['time_to_complete'].sum() if dev_data['time_to_complete'].sum() > 0 else 0

    return {
        'total_tasks': total_tasks,
        'story_points': total_sp,
        'bug_ratio': bug_ratio,
        'avg_completion_time': avg_completion_time,
        'sp_per_day': sp_per_day
    }
def process_data_files():
    data_dir = settings.DATA_DIR
    processed_files = []

    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        try:
            if file.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                continue

            processed_files.append({
                'file_name': file,
                'columns': list(df.columns),
                'shape': df.shape
            })
        except Exception as e:
            print(f"Error processing {file}: {e}")

    return processed_files


def load_data_from_file():
    data_dir = settings.DATA_DIR
    combined_data = pd.DataFrame()

    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        try:
            if file_name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                df['Creada'] = pd.to_datetime(df['Fecha Creación'], errors='coerce')
                df['Resuelta'] = pd.to_datetime(df['Resuelta'], errors='coerce')

                df['year'] = df['Creada'].dt.year
                df['quarter'] = df['Creada'].dt.quarter
                df['month'] = df['Creada'].dt.month
                df['developer'] = df['Persona asignada']
                df['tasks_completed'] = 1
                df['story_points'] = pd.to_numeric(df['Campo personalizado (Story Points)'], errors='coerce').fillna(0)
                df['time_to_complete'] = (df['Resuelta'] - df['Creada']).dt.total_seconds() / (3600 * 24)

                combined_data = pd.concat([combined_data, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

    return combined_data

def get_developers():
    data = load_data_from_file()
    if 'developer' in data.columns:
        return sorted(data['developer'].dropna().unique().tolist())
    return []

def get_time_filters():
    data = load_data_from_file()
    if data.empty:
        return {'years': [], 'quarters': [], 'months': []}

    return {
        'years': sorted(data['year'].dropna().unique().tolist()),
        'quarters': sorted(data['quarter'].dropna().unique().tolist()),
        'months': sorted(data['month'].dropna().unique().tolist())
    }


def get_filtered_chart_data(year='all', quarter='all', month='all', developer='all'):
    try:
        data = load_data_from_file()
        if data.empty:
            return {"data": [], "layout": {"title": "No data available"}}

        # Aplicar filtros existentes
        if year != 'all':
            data = data[data['year'] == int(year)]
        if quarter != 'all':
            data = data[data['quarter'] == int(quarter)]
        if month != 'all':
            data = data[data['month'] == int(month)]
        if developer != 'all':
            data = data[data['developer'] == developer]

        # Calcular métricas
        metrics_data = []
        for dev in data['developer'].unique():
            metrics = calculate_developer_metrics(data, dev)
            metrics_data.append({
                'developer': dev,
                **metrics
            })

        df_metrics = pd.DataFrame(metrics_data).sort_values('story_points', ascending=False)

        return {
            "data": [
                {
                    "type": "bar",
                    "name": "Story Points",
                    "x": df_metrics['developer'].tolist(),
                    "y": df_metrics['story_points'].tolist(),
                    "marker": {"color": "rgb(55, 83, 109)"}
                },
                {
                    "type": "bar",
                    "name": "Completion Time (hours)",
                    "x": df_metrics['developer'].tolist(),
                    "y": df_metrics['avg_completion_time'].tolist(),
                    "marker": {"color": "rgb(255, 99, 132)"}
                },
                {
                    "type": "bar",
                    "name": "Bug Ratio",
                    "x": df_metrics['developer'].tolist(),
                    "y": df_metrics['bug_ratio'].tolist(),
                    "marker": {"color": "rgb(75, 192, 192)"}
                }
            ],
            "layout": {
                "title": "Developer Performance Metrics",
                "barmode": "group",
                "xaxis": {"title": "Developer"},
                "yaxis": {"title": "Value"},
                "showlegend": True
            }
        }
    except Exception as e:
        print(f"Error in get_filtered_chart_data: {e}")
        return {"data": [], "layout": {"title": f"Error: {str(e)}"}}