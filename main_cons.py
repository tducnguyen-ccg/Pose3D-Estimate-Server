from mmpose.apis import MMPoseInferencer
from kafka import KafkaConsumer, KafkaProducer
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import time
import cv2
from pose_util.solve_exercise_mmpose import read_angle 


# Kafka configuration
bootstrap_servers = 'localhost:9092'
topic_image = 'topic-image'
topic_data = 'topic-data'

# Function to encode image to bytes
def image_to_bytes(image):
    # Encode the image to bytes
    _, encoded_image = cv2.imencode('.jpg', image)
    return encoded_image.tobytes()

# Function to decode bytes to image
def bytes_to_image(byte_data):
    # Decode bytes to numpy array
    decoded_image = cv2.imdecode(np.frombuffer(byte_data, np.uint8), -1)
    return decoded_image

# Create Kafka consumer
consumer = KafkaConsumer(topic_image, bootstrap_servers=bootstrap_servers)

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# AI model initialize
inferencer = MMPoseInferencer(
    pose3d='configs/body_3d_keypoint/motionbert/h36m/' \
           'motionbert_dstformer-ft-243frm_8xb32-120e_h36m.py',
    pose3d_weights='https://download.openmmlab.com/mmpose/v1/body_3d_keypoint/' \
                   'pose_lift/h36m/motionbert_ft_h36m-d80af323_20230531.pth'
)

def main():
    for message in consumer:
        print("Receive message")
        decoded_image = bytes_to_image(message.value)
        print("Key", message.key)
        print("Image size", decoded_image.shape)

        # Run pose estimation
        s1 = time.time()
        result_generator = inferencer(decoded_image, return_vis=False, show=False)
        result = next(result_generator)
        s2 = time.time()
        print("Processing time", s2-s1)
        keypoints = result['predictions'][0][0]['keypoints']
        print("Output keypoint", len(keypoints))
        list_angles = read_angle(keypoints)
        print("List angle", list_angles)

       # Sent data to consumer
        list_angles_str = ','.join(map(str, list_angles))
        list_angles_encoded = list_angles_str.encode('utf-8')
        producer.send(topic_data, key=message.key, value=list_angles_encoded)
        print("Sent list angle to consumer!")


if __name__ == '__main__':
    main()
