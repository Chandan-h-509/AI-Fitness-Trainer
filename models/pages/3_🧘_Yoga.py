# import cv2
# import streamlit as st

# st.title("Webcam Live Feed")
# start = st.button('Start')
# stop = st.button('Stop')
# FRAME_WINDOW = st.image([])
# camera = cv2.VideoCapture(0)

# while start and not stop:
#     _, frame = camera.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     FRAME_WINDOW.image(frame)
#     if stop:
#         break

import datetime
import os
import time
import cv2
import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image
from playsound import playsound

def calculate_angle(a, b, c):
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle   

def count_time(time_interval):
    global last_second, counter, pose_number
    now = datetime.datetime.now()
    current_second = int(now.strftime("%S"))
    if current_second != last_second:
        last_second = current_second
        counter += 1
        if counter == time_interval + 1:
            counter = 0
            pose_number += 1
            playsound(r'E:\AI Fitness Trainer\models\bell.wav')
            if pose_number == 5:
                pose_number = 1
    return counter, pose_number


last_second = 0
counter = 0
pose_number = 1

img1 = Image.open("E:\AI Fitness Trainer\models\gif\yoga.gif")

img2 = Image.open("E:\AI Fitness Trainer\models\images\pranamasana2.png")
img3 = Image.open("E:\AI Fitness Trainer\models\images\Eka_Pada_Pranamasana.png")
img4 = Image.open("E:\AI Fitness Trainer\models\images\Ashwa_Sanchalanasana.webp")

img5 = Image.open(r"E:\AI Fitness Trainer\models\images\ardha_chakrasana.webp")
img6 = Image.open(r"E:\AI Fitness Trainer\models\images\Utkatasana.png")
img7 = Image.open(r"E:\AI Fitness Trainer\models\images\Veerabhadrasan_2.png")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

app_mode = st.sidebar.selectbox("Choose the exercise", ["About","Track 1","Track 2"])

if app_mode == "About":
    if app_mode == "About":
        col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Welcome to the Yoga arena")
        st.markdown("Choose the Track you wish to do from the sidebar")
        st.write("##")
        st.write("""
        Here are few general instructions to follow while doing the workout:

        - It is necessary for you to provide web cam access. If you do not have a webcam, kindly attach an external camera while performing exercises.
        - Please avoid crowded places as the model can only detect 1 person. 
        - Please ensure that the surrounding is well lit so that the camera can detect you.
        - Please make sure the camera is focused on you based on the exercise so that the system can detect the angles and give you the correct input on form and count reps.

        With all that out of the way, Its time for you to get pumped up
        """)

    with col2:
        st.image(img1, width=400)

elif app_mode == "Track 1":

    st.markdown("## Welcome to Track1")

    with st.container():
        left_column1, right_column1 = st.columns(2)
        with left_column1:
            st.write("""
                Pranamasana (Prayer Pose):
                - Stand straight with feet together.
                - Bring palms together in front of chest.
                - Keep the spine erect and shoulders relaxed.
                - Focus on breathing deeply and evenly.
                - Hold for 5 seconds, breathe deeply.
            """)
              
        with right_column1:
            st.image(img2, width=200)

        st.write("-------------")

        left_column2, right_column2 = st.columns(2)
        with left_column2:
            st.write("""
                Eka Pada Pranamasana (One-Legged Prayer Pose):
                - Shift weight to left leg.
                - Bend right knee, place right foot on inner thigh.
                - Hold for 5 seconds.
                - Repeat on other side.
                
            """)
        with right_column2:
            st.image(img3, width=200)

        st.write("-------------")
        
        left_column3, right_column3 = st.columns(2)
        with left_column3:
            st.write("""
                Ashwa Sanchalanasana (Equestrian Pose):
                - Step right foot back into lunge.
                - Lower right knee, raise arms overhead.
                - Hold for 5 seconds.
                - Repeat on other side.
            """)
        with right_column3:
            st.image(img4, width=200)
        
    
    st.write("-------------")

    st.write("Click on the Start button to start the live video feed.")

    
    start = st.button("Start")
    cap = cv2.VideoCapture(0)
    FRAME_WINDOW = st.empty()
    stop = st.button("Stop")
    
    while start and not stop:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image,(800,600))

        try:
            landmarks = results.pose_landmarks.landmark
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
            
            # if len(overlay_list) != 0:
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            
            
            # Check pose and display feedback
            if pose_number == 1:
                #pranamasana
                left_angle = calculate_angle(left_wrist, left_shoulder, left_hip)
                right_angle = calculate_angle(right_wrist, right_shoulder, right_hip)
                distance = np.sqrt((right_wrist[0] - left_wrist[0])**2 + (right_wrist[1] - left_wrist[1])**2)
                if left_angle < 100 and right_angle < 100 and distance < 0.1:
                    cv2.putText(image, "Pose: Correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter, pose_number = count_time(5)
                    cv2.putText(image, f"TIME: {int(counter)}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "Pose: Incorrect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    counter = 0

            elif pose_number == 2:
                #ekapada pranamsana
                left_angle = calculate_angle(left_wrist, left_shoulder, left_hip)
                right_angle = calculate_angle(right_wrist, right_shoulder, right_hip)
                right_knee = calculate_angle(right_hip, right_knee, right_ankle)

                    # Calculate distance between wrists
                distance = np.sqrt((right_wrist[0] - left_wrist[0])**2 + (right_wrist[1] - left_wrist[1])**2)

                    # Check if wrists are close to the shoulders and (Pranamasana posture) and add timer
                if left_angle > 100 and right_angle > 100 and right_knee < 90 and distance < 0.1:
                    cv2.putText(image, "asana: Correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter, pose_number = count_time(5)
                    cv2.putText(image, f"TIME: {int(counter)}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "Pose: Incorrect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    counter = 0

            # Ashwa Sanchalanasana        
            elif pose_number == 3:
                left_angle = calculate_angle(left_shoulder,left_hip , left_knee)
                right_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

                left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)

                if left_leg_angle > 90 and right_leg_angle < 150 :
                    cv2.putText(image, "asana: Correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter, pose_number = count_time(5)
                    cv2.putText(image, f"TIME: {int(counter)}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "asana: Incorrect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    counter = 0
            else:
                #pause the frame
                cv2.putText(image, "Track completed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                st.write("Task Completed")
                start = False

        except:
            pass     

        # Display the image
        # FRAME_WINDOW.image(image, channels="BGR")
        FRAME_WINDOW.image(image, channels="BGR", use_column_width=True)
        
    cap.release()

    

elif app_mode == "Track 2":
    
    st.markdown("## Welcome to Track2")

    with st.container():
        left_column1, right_column1 = st.columns(2)
        with left_column1:
            st.write("""
                Ardha Chakrasana (Half Wheel Pose):
                - Stand with feet hip-width apart.
                - Inhale, raise arms overhead, palms together.
                - Exhale, bend backwards, keeping arms straight.
                - Hold for 5 seconds.
            """)
              
        with right_column1:
            st.image(img5, width=200)

        st.write("-------------")

        left_column2, right_column2 = st.columns(2)
        with left_column2:
            st.write("""
                Utkatasana (Chair Pose):
                - Stand with feet together.
                - Inhale, raise arms overhead.
                - Exhale, bend knees and lower hips as if sitting on a chair.
                - Hold for 5 seconds.
                
            """)
        with right_column2:
            st.image(img6, width=200)

        st.write("-------------")
        
        left_column3, right_column3 = st.columns(2)
        with left_column3:
            st.write("""
                Veerabhadrasana 2 (Warrior 2 Pose):
                - Step left foot back, right foot forward.
                - Bend right knee, aligning it with ankle.
                - Extend arms parallel to ground, palms facing down.
                - Hold for 5 seconds.
            """)
        with right_column3:
            st.image(img7, width=200)
        
    
    st.write("-------------")

    st.write("Click on the Start button to start the live video feed.")

    
    start = st.button("Start")
    cap = cv2.VideoCapture(0)
    FRAME_WINDOW = st.empty()
    stop = st.button("Stop")
    
    while start and not stop:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image,(800,600))

        try:
            landmarks = results.pose_landmarks.landmark
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
            
            # if len(overlay_list) != 0:
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            
            
            # Check pose and display feedback
            if pose_number == 1:
                #ardha chakrasana
                left_angle = calculate_angle(left_wrist, left_shoulder, left_hip)
                right_angle = calculate_angle(right_wrist, right_shoulder, right_hip)
                right_knee = calculate_angle(right_hip, right_knee, right_ankle)
                distance = np.sqrt((right_wrist[0] - left_wrist[0])**2 + (right_wrist[1] - left_wrist[1])**2)

                if left_angle > 100 and right_angle > 100 and  distance < 0.1:
                    cv2.putText(image, "Pose: Correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter, pose_number = count_time(5)
                    cv2.putText(image, f"TIME: {int(counter)}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "Pose: Incorrect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    counter = 0

            elif pose_number == 2:
                #utkatasana
                left_angle = calculate_angle(left_shoulder,left_hip , left_knee)
                right_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

                left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)

                    # Calculate distance between wrists
                distance = np.sqrt((right_wrist[0] - left_wrist[0])**2 + (right_wrist[1] - left_wrist[1])**2)

                    # Check if wrists are close to the shoulders and (Pranamasana posture) and add timer
                if right_leg_angle < 150 and left_leg_angle < 150 and left_arm_angle > 150 and right_arm_angle > 150 and left_shoulder_angle > 120  and right_shoulder_angle > 120 :
                    cv2.putText(image, "asana: Correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter, pose_number = count_time(5)
                    cv2.putText(image, f"TIME: {int(counter)}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "Pose: Incorrect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    counter = 0
                    
            # Veerabadrasana 2
            elif pose_number == 3:
                left_angle = calculate_angle(left_shoulder,left_hip , left_knee)
                right_angle = calculate_angle(right_shoulder, right_hip, right_knee)

                left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

                left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)

                if right_leg_angle < 120  and left_arm_angle > 150 and right_arm_angle > 150 and left_shoulder_angle < 120  and right_shoulder_angle < 120 :
                    cv2.putText(image, "asana: Correct", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter, pose_number = count_time(5)
                    cv2.putText(image, f"TIME: {int(counter)}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "asana: Incorrect", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    counter = 0
            else:
                #pause the frame
                cv2.putText(image, "Track completed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                start = False

        except:
            pass     

        # Display the image
        FRAME_WINDOW.image(image, channels="BGR")
        # FRAME_WINDOW.image(image, channels="BGR", use_column_width=True)
        
    cap.release()
   
