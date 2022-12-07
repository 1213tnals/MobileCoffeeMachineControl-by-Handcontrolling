import cv2
import mediapipe as mp
import numpy as np
import math
import time

import rospy
from std_msgs.msg import Int32

def calculate_angle(a,b):
    a = np.array(a) # first_finger
    b = np.array(b) # second_finger
    
    radians = np.arctan2(b[1]-a[1], b[0]-a[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if b[1] < a[1]:
        angle = -angle + 90
    elif b[0] < a[0]:
        angle = -90
    else:
        angle = 90
        
    return angle

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pub_speed = rospy.Publisher('User/Hand_Speed', Int32, queue_size=10)
#pub_angle = rospy.Publisher('User/Hand_Angle', Int32, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10) # 10hz

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=3,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
            
        image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)   #미디어파이프 모델을 넣기 위해 전처리 과정 필요, 전처리된 이미지를 results로 넘길 수 있음

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for i in range(5): 
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                
                    finger_first = hand_landmarks.landmark[4]   #엄지
                    finger_second = hand_landmarks.landmark[8]   #검지

                    finger_first_2D = [hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y]
                    finger_second_2D = [hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y]

                    diff_xyz = [0,0,0,0,0]

                    diff_x = abs(finger_first.x - finger_second.x)  #두 손가락의 x좌표의 절댓값(퍼센트 정보)
                    diff_y = abs(finger_first.y - finger_second.y)
                    diff_z = abs(finger_first.z - finger_second.z) 
                    diff_xyz[i] = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2) + math.pow(diff_z,2))

                diff = (diff_xyz[0]+diff_xyz[1]+diff_xyz[2]+diff_xyz[3]+diff_xyz[4])/5

                speed = int(diff * 1000) + 30  #볼륨을 정의, 미디어 파이프는 이미지에 대해서 0~0.xx~1의 퍼센트로 반환함
                                          #1000은 튜닝할 값

                angle = int(calculate_angle(finger_first_2D, finger_second_2D))

                pub_speed.publish(speed)
                #pub_angle.publish(angle)                          
                
                cv2.putText(
                    image, text='motor speed: %d' % speed, org=(10,30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(255,127,127), thickness=2)
                cv2.putText(
                    image, text='angle: %d' % angle, org=(10,60),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(127,255,127), thickness=2)

                mp_drawing.draw_landmarks(   #손가락 뼈마디 그리는 부분
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style())
                    
        cv2.imshow('image', image)
        if cv2.waitKey(1) == ord('q'):
            break
                 
    cap.release()