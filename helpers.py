import numpy as np
import math
import json
import pandas as pd

def get_data_std_pose(file_path):
    # Đọc dữ liệu JSON từ chuỗi
    with open(file_path, 'r') as file:
        data = json.load(file)

    print(len(data["standard_pose"]) / 10 + int(data["start_time"].split(":")[1]), "second")
    print(len(data["standard_pose"]), "frame")

    return data

def find_index_exercise_from_excel(df, name_exercise):
    index_exercise = 0
    for name in df['title']:
        if name.strip() == name_exercise.strip():
            return index_exercise
        index_exercise += 1
    return -1



def get_data_exercise_frome_excel(file_path, name_exercise):
    df = pd.read_excel(file_path)
    index = find_index_exercise_from_excel(df, name_exercise)
    if index == -1:
        return -1

    state = df["state"][index]
    audio_link = df["audio_link"][index]
    warning = df['warning'][index]


    state = json.loads(state)
    audio_link = json.loads(audio_link)
    warning = json.loads(warning)

    return state, audio_link, warning


def calculate_angles(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


# def calculate_angles(a, b, c):
#     ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
#     return ang + 360 if ang < 0 else ang




def calculate_angle_for_horizontal(a, b, c=None, horizontal_surface=True):
    b = np.array(b)

    if c is not None:
        a = np.array(a)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )
    else:
        if horizontal_surface:
            c = np.array([b[0] + 1, b[1]])  # Điểm cách b 1 đơn vị theo trục x
        else:
            c = np.array([b[0], b[1] + 1])  # Điểm cách b 1 đơn vị theo trục y

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 180 - angle

    return min(angle, 180-angle)

def calculate_distance(x1, x2):
    distance = math.sqrt((x2[0] - x1[0])**2 + (x2[1] - x1[1])**2)
    return distance

def calculate_similarity(vector1, vector2):
    # Tính Euclidean Distance giữa hai vector
    distance = np.linalg.norm(np.array(vector1) - np.array(vector2))

    # Chuyển đổi thành độ tương đồng từ 0 đến 100
    max_possible_distance = np.linalg.norm(np.array([100] * len(vector1)))
    similarity_percent = max(0, 100 - (distance / max_possible_distance) * 100)

    return similarity_percent

