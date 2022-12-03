import cv2
import mediapipe as mp
import math
import time

import rospy
from std_msgs.msg import Int32


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pub = rospy.Publisher('User/Hand', Int32, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10) # 10hz

cap = cv2.VideoCapture(-1)

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
                    diff_xyz = [0,0,0,0,0]

                    diff_x = abs(finger_first.x - finger_second.x)  #두 손가락의 x좌표의 절댓값(퍼센트 정보)
                    diff_y = abs(finger_first.y - finger_second.y)
                    diff_z = abs(finger_first.z - finger_second.z) 
                    diff_xyz[i] = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2) + math.pow(diff_z,2))

                diff = (diff_xyz[0]+diff_xyz[1]+diff_xyz[2]+diff_xyz[3]+diff_xyz[4])/5

                speed = int(diff * 1000) + 30  #볼륨을 정의, 미디어 파이프는 이미지에 대해서 0~0.xx~1의 퍼센트로 반환함
                                          #500은 튜닝할 값
                pub.publish(speed)                          
                
                cv2.putText(
                    image, text='motor speed: %d' % speed, org=(10,30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=255, thickness=2)

                mp_drawing.draw_landmarks(   #손가락 뼈마디 그리는 부분
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
        cv2.imshow('image', image)
        if cv2.waitKey(1) == ord('q'):
            break
                 
    cap.release()
