import torch
from collections import defaultdict
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pyts.image import GramianAngularField
import pandas as pd
import os
from collections import Counter

def save_user_data(X_list, y_list, user_name):
    X_array = np.concatenate(X_list, axis=0)
    y_array = np.concatenate(y_list, axis=0)
    torch.save((torch.tensor(X_array, dtype=torch.float32), torch.tensor(y_array, dtype=torch.long)), f'{user_name}.pt')

# def segment_and_convert_to_gaf_mtf(raw_df, start_time, end_time, step=10, segment_length=200):
#     segment_df = raw_df[(raw_df['Time'] >= start_time) & (raw_df['Time'] <= end_time)]
#     gaf = GramianAngularField(image_size=segment_length, method='difference')
#     transformed_segments = []
#     scaler = MinMaxScaler(feature_range=(-1, 1))
#     for start_idx in range(0, len(segment_df) - segment_length + 1, step):
#         segment = segment_df.iloc[start_idx:start_idx+segment_length]
#         sensor_data = segment[['Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']].values
#         sensor_data_normalized = scaler.fit_transform(sensor_data)
#         temp_gaf_mtf = np.zeros((6, segment_length, segment_length))
#         for i in range(sensor_data.shape[1]):
#             gaf_transformed = gaf.fit_transform(sensor_data_normalized[:, i].reshape(1, -1))
#             temp_gaf_mtf[i] = gaf_transformed[0]
#         transformed_segments.append(temp_gaf_mtf)
#     return np.stack(transformed_segments, axis=0) if transformed_segments else np.array([])

# def load_and_process_task_data(task_number, user_type, task_mapping):
#     task_raw_data_file1 = f'/home/worker/SWIT_Dataset/Task_{task_number}_{user_type}.csv'

#     task_raw_df1 = pd.read_csv(task_raw_data_file1)

#     if task_number in [8, 6]:
#         start_time = 0
#         end_time = 20
#         gaf_data = segment_and_convert_to_gaf_mtf(task_raw_df1, start_time, end_time, step=10)
#         if gaf_data.size > 0:
#             X = np.concatenate([gaf_data], axis=0)
#             y = np.full(X.shape[0], task_mapping.get(task_number, task_number))
#             return X, y
#     else:
#         st_task_file = f'/home/worker/SWIT_Dataset/Segmentation_Status/ST_Task_{task_number}.csv'
#         if not os.path.exists(st_task_file):
#             print(f"File {st_task_file} does not exist.")
#             return None, None

#         st_task_df = pd.read_csv(st_task_file)
#         user_starts_ends = st_task_df.loc[st_task_df['Status'].str.contains('Start|End'), user_type].values
#         adjusted_times = [(time * 0.01) - 1 if idx % 2 == 0 else (time * 0.01) + 1 for idx, time in enumerate(user_starts_ends)]
#         adjusted_times = [max(0, time) for time in adjusted_times]

#         gaf_data_list = []
#         for i in range(0, len(adjusted_times), 2):
#             gaf_data = segment_and_convert_to_gaf_mtf(task_raw_df1, adjusted_times[i], adjusted_times[i + 1], n_bins=n_bins)
#             if gaf_data.size > 0:
#                 gaf_data_list.append(gaf_data)

#         if gaf_data_list:
#             X = np.concatenate(gaf_data_list, axis=0)
#             y = np.full(X.shape[0], task_mapping.get(task_number, task_number))
#         else:
#             X = np.array([])
#             y = np.array([])

#         return X, y



def segment_and_convert_to_gaf_mtf(raw_df, start_time, end_time, step=10, segment_length=200):
    segment_df = raw_df[(raw_df['Time'] >= start_time) & (raw_df['Time'] <= end_time)]
    gaf = GramianAngularField(image_size=segment_length, method='difference')
    transformed_segments = []
    scaler = MinMaxScaler(feature_range=(-1, 1))
    for start_idx in range(0, len(segment_df) - segment_length + 1, step):
        segment = segment_df.iloc[start_idx:start_idx+segment_length]
        sensor_data = segment[['Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']].values
        sensor_data_normalized = scaler.fit_transform(sensor_data)
        temp_gaf_mtf = np.zeros((6, segment_length, segment_length))
        for i in range(sensor_data.shape[1]):
            gaf_transformed = gaf.fit_transform(sensor_data_normalized[:, i].reshape(1, -1))
            temp_gaf_mtf[i] = gaf_transformed[0]
        transformed_segments.append(temp_gaf_mtf)
    return np.stack(transformed_segments, axis=0) if transformed_segments else np.array([])

def load_and_process_task_data(task_number, user_type, task_mapping):
    task_raw_data_file1 = f'/home/worker/SWIT_Dataset/Task_{task_number}_{user_type}.csv'
    task_raw_df1 = pd.read_csv(task_raw_data_file1)

    st_task_file = f'/home/worker/SWIT_Dataset/Segmentation_Status/ST_Task_{task_number}.csv'
    if not os.path.exists(st_task_file):
        print(f"File {st_task_file} does not exist.")
        return None, None

    st_task_df = pd.read_csv(st_task_file)
    user_starts_ends = st_task_df.loc[st_task_df['Status'].str.contains('Start|End'), user_type].values
    adjusted_times = [(time * 0.01) - 1 if idx % 2 == 0 else (time * 0.01) + 1 for idx, time in enumerate(user_starts_ends)]
    adjusted_times = [max(0, time) for time in adjusted_times]

    gaf_data_list = []
    for i in range(0, len(adjusted_times), 2):
        gaf_data = segment_and_convert_to_gaf_mtf(task_raw_df1, adjusted_times[i], adjusted_times[i + 1], n_bins=n_bins)
        if gaf_data.size > 0:
            gaf_data_list.append(gaf_data)

    if gaf_data_list:
        X = np.concatenate(gaf_data_list, axis=0)
        y = np.full(X.shape[0], task_mapping.get(task_number, task_number))
    else:
        X = np.array([])
        y = np.array([])

    return X, y

def process_task_data_for_user(task_number, user_id, task_mapping):
    X_list, y_list = [], []
    user_data_count = defaultdict(int)

    X, y = load_and_process_task_data(task_number, user_id, task_mapping)
    if X is not None and X.size > 0:
        X_list.append(X)
        y_list.append(y)
        user_data_count[task_number] += X.shape[0]
    
    return X_list, y_list, user_data_count

def balance_classes(X_list, y_list):
    combined_X = np.concatenate(X_list, axis=0)
    combined_y = np.concatenate(y_list, axis=0)
    
    counter = Counter(combined_y)
    min_count = min(counter.values())
    
    balanced_X, balanced_y = [], []
    for label in counter.keys():
        indices = np.where(combined_y == label)[0]
        selected_indices = np.random.choice(indices, min_count, replace=False)
        balanced_X.append(combined_X[selected_indices])
        balanced_y.append(combined_y[selected_indices])
    
    balanced_X = np.concatenate(balanced_X, axis=0)
    balanced_y = np.concatenate(balanced_y, axis=0)
    
    return balanced_X, balanced_y

tasks_to_process = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
task_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9}

# List of users
user_ids = ['User_1', 'User_2', 'User_3', 'User_4', 'User_5', 'User_6', 'User_7', 'User_8', 'User_9', 'User_10', 
            'User_11', 'User_12', 'User_13','User_14', 'User_15', 'User_16', 'User_17', 'User_18', 'User_19', 'User_20',
            'User_21', 'User_22', 'User_23', 'User_24', 'User_25', 'User_26', 'User_27']

user_data_counts = defaultdict(lambda: defaultdict(int))  # Use nested defaultdict 

for user_id in user_ids:
    user_X_list, user_y_list = [], []
    
    for task_number in tasks_to_process:
        X_user, y_user, task_counts = process_task_data_for_user(task_number, user_id, task_mapping)
        if X_user:
            user_X_list.extend(X_user)
            user_y_list.extend(y_user)
            for task, count in task_counts.items():
                user_data_counts[user_id][task] += count
    
    if user_X_list and user_y_list:
        balanced_user_X, balanced_user_y = balance_classes(user_X_list, user_y_list)
        save_user_data([balanced_user_X], [balanced_user_y], f'user_{user_id}')

for user_id, tasks in user_data_counts.items():
    for task, count in tasks.items():
        print(f"{user_id} Task {task}: {count} samples")
