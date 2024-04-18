import cv2
from helpers import *

def read_angle(landmarks):

    list_angle_predict = []

    # Refer
    # mmpose https://mmpose.readthedocs.io/en/latest/dataset_zoo/3d_body_keypoint.html
    # mediapipe https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
    list_landmark = {
        'left_ankle': [landmarks[6][0], landmarks[6][1], landmarks[6][2]],
        'right_ankle': [landmarks[3][0], landmarks[3][1], landmarks[3][2]],
        'left_knee': [landmarks[5][0], landmarks[5][1], landmarks[5][2]],
        'right_knee': [landmarks[2][0], landmarks[2][1], landmarks[2][2]],
        'left_hip': [landmarks[4][0], landmarks[4][1], landmarks[4][2]],
        'right_hip': [landmarks[1][0], landmarks[1][1], landmarks[1][2]],
        'left_shoulder': [landmarks[11][0], landmarks[11][1], landmarks[11][2]],
        'right_shoulder': [landmarks[14][0], landmarks[14][1], landmarks[14][2]],
        # 'left_index': can not match - check ankle,
        # 'right_index': can not match - check ankle,
        # 'left_heel': can not match - check ankle,
        # 'right_heel': can not match - check ankle,
        # 'left_foot_index': can not match - check ankle,
        # 'right_foot_index': can not match - check ankle,
        'left_elbow': [landmarks[12][0], landmarks[12][1], landmarks[12][2]],
        'right_elbow': [landmarks[15][0], landmarks[15][1], landmarks[15][2]],
        'left_wrist': [landmarks[13][0], landmarks[13][1], landmarks[13][2]],
        'right_wrist': [landmarks[16][0], landmarks[16][1], landmarks[16][2]],
        # 'left_mouth': can not match - check nose,
        # 'right_mouth': can not match - check nose,
        'nose': [landmarks[9][0], landmarks[9][1], landmarks[9][2]],
        # 'left_eye_inner': can not match - check nose,
        # 'left_eye': can not match - check nose,
        # 'left_eye_outer': can not match - check noise,
        # 'right_eye_inner': can not match - check noise,
        # 'right_eye': can not match - check noise,
        # 'right_eye_outer': can not match - check noise,
        # 'left_ear': can not match - check noise,
        # 'right_ear': can not match - check noise,
        # 'left_pinky': can not match - check wrist,
        # 'right_pinky': can not match - check wrist,
        # 'left_thumb': can not match - check wrist,
        # 'right_thumb': can not match - check wrist,
        }


    '''
    Nếu các bộ phận bên trái bị bộ phận bên phải che thì ta gán các landmark bộ phận bên trái bằng bên phải luôn và ngược lại
    '''
    hip = None
    knee = None
    ankle = None
    # heel = None
    shoulder = None

    list_get = []
    if list_landmark["left_shoulder"][2] > list_landmark["right_shoulder"][2]:
        shoulder = list_landmark['left_shoulder']
    else:
        shoulder = list_landmark['right_shoulder']

    if list_landmark["left_hip"][2] > list_landmark["right_hip"][2]:
        hip = list_landmark['left_hip']
    else:
        hip = list_landmark['right_hip']

    if list_landmark["left_knee"][2] > list_landmark["right_knee"][2]:
        knee = list_landmark['left_knee']
    else:
        knee = list_landmark['right_knee']

    if list_landmark["left_ankle"][2] > list_landmark["right_ankle"][2]:
        ankle = list_landmark['left_ankle']
    else:
        ankle = list_landmark['right_ankle']

    # Remove heel, check by ankle
    # print(list_landmark["left_hip"], list_landmark["right_hip"], list_landmark['nose'], shoulder, hip, knee, ankle)
    l_e = list_landmark["left_hip"][0]
    r_e = list_landmark["right_hip"][0]

    # remove heel from ans formular
    ans = abs(calculate_distance(list_landmark["left_hip"], list_landmark["right_hip"])) / abs(calculate_distance(list_landmark['nose'], shoulder) + calculate_distance(shoulder, hip) + calculate_distance(hip, knee) + calculate_distance(knee, ankle))

    list_convert = ["shoulder", "elbow", "wrist", "hip", "knee", "ankle"]  # remove eye, ear, index, thumb, heel, foot_index

    for name_landmark in list_convert:
        name_landmark_left = "left_" + name_landmark
        name_landmark_right = "right_" + name_landmark

        # Nếu đứng ngang thì luôn chọn bên phải vì mediapipe detect bên phải là điểm gần màn hình
        if ans < 0.05:
            list_landmark[name_landmark_left] = list_landmark[name_landmark_right]

    angle1_predict = round(calculate_angles(list_landmark['right_wrist'], list_landmark['right_elbow'], list_landmark['right_shoulder']))
    angle2_predict = round(calculate_angles(list_landmark['left_wrist'], list_landmark['left_elbow'], list_landmark['left_shoulder']))
    angle3_predict = round(calculate_angles(list_landmark['right_elbow'], list_landmark['right_shoulder'], list_landmark['left_hip']))
    angle4_predict = round(calculate_angles(list_landmark['left_elbow'], list_landmark['left_shoulder'], list_landmark['right_hip']))
    angle5_predict = round(calculate_angles(list_landmark['right_shoulder'], list_landmark['right_hip'], list_landmark['right_knee']))
    angle6_predict = round(calculate_angles(list_landmark['left_shoulder'], list_landmark['left_hip'], list_landmark['left_knee']))
    angle7_predict = round(calculate_angles(list_landmark['right_hip'], list_landmark['right_knee'], list_landmark['right_ankle']))
    angle8_predict = round(calculate_angles(list_landmark['left_hip'], list_landmark['left_knee'], list_landmark['left_ankle']))

    list_angle_predict.append(angle1_predict)
    list_angle_predict.append(angle2_predict)
    list_angle_predict.append(angle3_predict)
    list_angle_predict.append(angle4_predict)
    list_angle_predict.append(angle5_predict)
    list_angle_predict.append(angle6_predict)
    list_angle_predict.append(angle7_predict)
    list_angle_predict.append(angle8_predict)


    return list_angle_predict
