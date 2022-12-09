import cv2                                     #You should install opencv
import mediapipe as mp                         #You should install mediapipe
import numpy as np                             ##You should install numpy
import math
import time

import rospy                                   #You should install ROS!!
from std_msgs.msg import Int32                 #I used ros topic type Int32


#First finger and second finger make virtual line, and this line's direction is robot's direction
#When arctan2 = 0, virtual line is horizental and we should twist our wrist
#So I change the result angle by making this function 
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

rps_gesture = {0:'stop', 5:'run', 10:'coffee make'}
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#I used trained data
file = np.genfromtxt('data/gesture_train.csv', delimiter=',')
angle = file[:,:-1].astype(np.float32)
label = file[:, -1].astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)

#Ros topic publising value make
pub_speed = rospy.Publisher('User/Hand_Speed', Int32, queue_size=1)
pub_angle = rospy.Publisher('User/Hand_Angle', Int32, queue_size=1)
pub_mode = rospy.Publisher('User/Hand_Mode', Int32, queue_size=1)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(1) # 10hz

cap = cv2.VideoCapture(0)

#Using Mediapipe
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
            
        image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for i in range(5): 
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                
                    finger_first = hand_landmarks.landmark[4]   #first_finger
                    finger_second = hand_landmarks.landmark[8]   #second_finger

                    finger_first_2D = [hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y]
                    finger_second_2D = [hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y]

                    diff_xyz = [0,0,0,0,0]

                    diff_x = abs(finger_first.x - finger_second.x)  #두 손가락의 x좌표의 절댓값(퍼센트 정보)
                    diff_y = abs(finger_first.y - finger_second.y)
                    diff_z = abs(finger_first.z - finger_second.z) 
                    diff_xyz[i] = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2) + math.pow(diff_z,2))

                diff = (diff_xyz[0]+diff_xyz[1]+diff_xyz[2]+diff_xyz[3]+diff_xyz[4])/5

                speed = int(diff * 1000) + 30        #our robot's speed is safer at 30~100. So I make speed value like this

                angle_from_vetical = int(calculate_angle(finger_first_2D, finger_second_2D))


                joint = np.zeros((21, 3))
                for j, lm in enumerate(hand_landmarks.landmark):
                    joint[j] = [lm.x, lm.y, lm.z]

                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] #parent joint
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] #child joint
                v = v2 - v1

                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
                #각 벡터의 길이를 구함(Eigen벡터들을 구함)

                angle = np.arccos(np.einsum('nt,nt->n',
                                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
                #아크코사인을 이용하여 각 벡터들에 대한 각도(15개)를 구함

                angle = np.degrees(angle)

                # Inference gesture
                data = np.array([angle], dtype=np.float32)
                ret, result, neighbours, dist = knn.findNearest(data, 5)   #Knn, K=3
                idx = int(result[0][0])

                #ROS publishing part
                pub_speed.publish(speed)
                pub_angle.publish(angle_from_vetical)
                pub_mode.publish(idx)
                time.sleep(0.01)                                    #arduino's processing is late, so give a delay in topic communicating                   
                
                cv2.putText(
                    image, text='motor speed: %d' % speed, org=(10,30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(255,127,127), thickness=2)
                cv2.putText(
                    image, text='angle: %d' % angle_from_vetical, org=(10,60),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(127,255,127), thickness=2)

                if(idx == 0):
                    cv2.putText(
                    image, text='mode change: %s' % rps_gesture[0] , org=(10,90),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(127,127,255), thickness=2)
                elif(idx == 5):
                    cv2.putText(
                    image, text='mode change: %s' % rps_gesture[5] , org=(10,90),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(127,127,255), thickness=2)
                elif(idx == 10):
                    cv2.putText(
                    image, text='coffee make', org=(10,90),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(127,127,255), thickness=2)

                mp_drawing.draw_landmarks(   #손가락 뼈마디 그리는 부분
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style())
                    
        cv2.imshow('image', image)
        if cv2.waitKey(1) == ord('q'):
            break
                 
    cap.release()