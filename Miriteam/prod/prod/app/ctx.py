import cv2 as cv
from net.AgeGenderRecognitionNet import AgeGenderRecognitionNet
from net.EmotionRecognitionNet import EmotionRecognitionNet
from net.FaceDetectionNet import FaceDetectionNet
from net.HeadPoseEstimationNet import HeadPoseEstimationNet

face_detection_net = FaceDetectionNet(
    "models/face-detection-retail-0005.xml",
    "models/face-detection-retail-0005.bin",
    (300, 300)
)

age_gender_recognition_net = AgeGenderRecognitionNet(
    "models/age-gender-recognition-retail-0013.xml",
    "models/age-gender-recognition-retail-0013.bin",
    (62, 62)
)

emotion_recognition_net = EmotionRecognitionNet(
    "models/emotions-recognition-retail-0003.xml",
    "models/emotions-recognition-retail-0003.bin",
    (64, 64)
)

head_pose_estimation_net = HeadPoseEstimationNet(
    "models/head-pose-estimation-adas-0001.xml",
    "models/head-pose-estimation-adas-0001.bin",
    (60, 60)
)

slide = [
    cv.imread('app/slides/logo.png'),
    cv.imread('app/slides/hello.png'),
    cv.imread('app/slides/bye.png'),
]
