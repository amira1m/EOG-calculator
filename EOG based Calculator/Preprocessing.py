import os
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
import re
import joblib

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def separate_and_concatenate(text):
    alphabets = ''.join(re.findall(r'[a-zA-Z]+', text))
    return alphabets  # Concatenate alphabets directly


# Extracting the indices from the filenames
def read_signals(folder_path, movement_mapping):
    horiz_indices = set()
    # Initialize lists to store data
    horiz_signals = []
    vert_signals = []
    eye_movements = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            # Extract prefix and extension
            file_prefix, file_ext = os.path.splitext(file_name)

            # Check if the file is horizontal or vertical
            if file_ext == '.txt' and file_prefix.endswith('h'):
                index = file_prefix[:-1]
                horiz_indices.add(index)

    for index in horiz_indices:
        horiz_file = index + 'h.txt'
        vert_file = index + 'v.txt'

        # Skip certain files
        if (horiz_file == "serkanh.txt" and vert_file == "serkanv.txt") or \
                (horiz_file == "Edit2h.txt" and vert_file == "Edit2v.txt"):
            continue

        # Check if corresponding vertical file exists
        if horiz_file in os.listdir(folder_path) and vert_file in os.listdir(folder_path):
            movement = separate_and_concatenate(index)
            for key, movementmap in movement_mapping.items():
                if key.lower() in movement.lower():
                    movement_type = movementmap
                    break

            # Read the horizontal signal data
            with open(os.path.join(folder_path, horiz_file), 'r') as file:
                horiz_signal = [float(line.strip()) for line in file.readlines()]

            # Read the vertical signal data
            with open(os.path.join(folder_path, vert_file), 'r') as file:
                vert_signal = [float(line.strip()) for line in file.readlines()]

            # Append the signals and label to the respective lists
            horiz_signals.append(horiz_signal)
            vert_signals.append(vert_signal)
            eye_movements.append(movement_type)

    return horiz_signals, vert_signals, eye_movements


# label encoding
def LabelEncoding(df, column_name):
    le = LabelEncoder()
    df[column_name] = le.fit_transform(df[column_name])
    model_filename = "Saved Models/LabelEncoding.pkl"
    joblib.dump(le, model_filename)
    return df


def preprocessing(folder_path):
    # Dictionary to map movement types
    movement_mapping = {
        "Yukari": "Up",
        "Asagi": "Down",
        "Sag": "Right",
        "Sol": "Left",
        "Kirp": "Blink"
    }
    horizontal_signals, vertical_signals, eye_movements = read_signals(folder_path, movement_mapping)
    # Create DataFrame
    data = pd.DataFrame({
        'Horizontal_Signal': horizontal_signals,
        'Vertical_Signal': vertical_signals,
        'Eye_Movement': eye_movements
    })
    print(f"Before: data\n{data.head(5)}\n")

    LabelEncoding(data, "Eye_Movement")

    print(f"After: data\n{data.head(5)}\nencoded\n")
    return data


# preprocessing("3-class")
