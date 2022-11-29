import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue
            
        image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)   #미디어파이프 모델을 넣기 위해 전처리 과정 필요, 전처리된 이미지를 results로 넘길 수 있음

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_first = hand_landmarks.landmark[4]   #엄지
                finger_second = hand_landmarks.landmark[8]   #검지

                diff = abs(finger_first.x - finger_second.x)  #두 손가락의 x좌표의 절댓값(퍼센트 정보)

                speed = int(diff * 200) + 30  #볼륨을 정의, 미디어 파이프는 이미지에 대해서 0~0.xx~1의 퍼센트로 반환함
                                          #500은 튜닝할 값
                
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