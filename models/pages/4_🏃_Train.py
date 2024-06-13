import streamlit as st
import json

import requests 

import cv2
from cvzone.PoseModule import PoseDetector
import math
import numpy as np
import plotly.graph_objects as go
import tempfile


# Lottie Files: https://lottiefiles.com/

html = """
<div style="background-color:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;">Train here</h2>
</div>"""
st.markdown(html, unsafe_allow_html=True)    



app_mode = st.sidebar.selectbox("Choose the exercise", ["About","Left Dumbbell","Right Dumbbell","Squats","Pushups","Shoulder press"])
if app_mode == "About":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Welcome to the Training arena")
        st.markdown("Choose the workout you wish to do from the sidebar")
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
        img=st.image('./gif/ham.gif')
    


elif app_mode == "Left Dumbbell":
    st.markdown("## Left Dumbbell")
    weight1 = st.slider('What is your weight?', 20, 130, 40)
    st.write("I'm ", weight1, 'kgs')

    st.write("-------------")

    goal_calorie1 = st.slider('Set a goal calorie to burn', 1, 200, 15)
    st.write("I want to burn", goal_calorie1, 'kcal')
    
    st.write("-------------")


    st.write(" Click on the Start button to start the live video feed.")
    st.write("##")
    
    class angleFinder:
        def __init__(self,lmlist,p1,p2,p3,drawPoints):
            self.lmlist = lmlist
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3
            
            self.drawPoints = drawPoints
        #    finding angles

        def angle(self):
            if len(self.lmlist) != 0:
                point1 = self.lmlist[self.p1]
                point2 = self.lmlist[self.p2]
                point3 = self.lmlist[self.p3]
                

                x1,y1 = point1[1:-1]
                x2, y2 = point2[1:-1]
                x3, y3 = point3[1:-1]
                

                # calculating angle for left arm
                leftHandAngle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                            math.atan2(y1 - y2, x1 - x2))

                leftHandAngle = int(np.interp(leftHandAngle, [42,143], [100, 0]))
                

                # drawing circles and lines on selected points
                if self.drawPoints == True:
                    cv2.circle(img, (x1, y1), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x2, y2), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x3, y3), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x3, y3), 15, (0, 255, 0), 6)
                    

                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),4)
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 4)
                    

                return leftHandAngle
    
    if 'type' not in st.session_state:
        st.session_state.type = None


    def handle_click_start():
        st.session_state.type = "Start"

    def handle_click_stop():
        st.write(st.session_state.counter1)
        st.session_state.type = "Stop"
    
    start_button = st.button('Start', on_click=handle_click_start)
    stop_button = st.button('Stop',  on_click=handle_click_stop)


    
    # defining some variables
    counter = 0
    direction = 0


    frame_placeholder = st.empty()

    detector = PoseDetector(detectionCon=0.7,trackCon=0.7)

    
    if st.session_state['type']=='Start':
        
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, img = cap.read()
            img = cv2.resize(img,(640,480))

            detector.findPose(img,draw=0)
            lmList, bboxInfo = detector.findPosition(img, bboxWithHands=0,draw=False)

            angle1 = angleFinder(lmList,11,13,15,drawPoints=True)
            left = angle1.angle()
            
            if left==None:
                left=0

            # Counting number of shoulder ups
            if left >= 90:
                if direction == 0:
                    counter += 0.5
                    st.session_state.counter1 = counter
                    direction = 1
            if left <= 70:
                if direction == 1:
                    counter += 0.5
                    st.session_state.counter1 = counter
                    direction = 0

            
            #putting scores on the screen
            cv2.rectangle(img,(0,0),(120,120),(255,0,0),-1)
            cv2.putText(img,str(int(counter)),(1,70),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.6,(0,0,255),6)

            # Converting values for rectangles
            leftval = np.interp(left,[0,100],[480,280])


            # Drawing left rectangle and putting text
            cv2.rectangle(img, (582, 280), (632, 480), (0, 0, 255), 5)
            cv2.rectangle(img, (582, int(leftval)), (632, 480), (0, 0, 255), -1)


            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            frame_placeholder.image(img, "RGB")
            

    elif st.session_state['type']=='Stop': 
        st.write("The video capture has ended")

        st.write("---------")
        st.write("## Analytics") 
        st.write("You did ",st.session_state.counter1," reps")   
        
        # calories1=3.8*weight1/st.session_state.counter1
        calories1=0.25*st.session_state.counter1
        if calories1<goal_calorie1:
            st.write("You have burned ",calories1,"kcal of calories")
            st.write("You have not achieved your goal. Try again")

        else:
            st.write("You have burned ",calories1,"kcal of calories")
            st.write("You have achieved your goal. Congratulations")
        
        fig = go.Figure(data=[go.Bar(x=['Bicep Curls'], y=[calories1], name='Calories Burned')])

        fig.add_trace(go.Bar(x=['Bicep Curls'], y=[goal_calorie1], name='Goal Calorie'))

        # Set chart layout
        fig.update_layout(
            title='Calories Burned for Bicep Curls',
            xaxis_title='Exercise',
            yaxis_title='Calories Burned'
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig)
                    
            
        

            
    


elif app_mode == "Right Dumbbell":
    st.markdown("## Right Dumbbell")
    weight2 = st.slider('What is your weight?', 20, 130, 40)
    st.write("I'm ", weight2, 'kgs')

    st.write("-------------")

    goal_calorie2 = st.slider('Set a goal calorie to burn', 1, 200, 15)
    st.write("I want to burn", goal_calorie2, 'kcal')
    
    st.write("-------------")


    st.write(" Click on the Start button to start the live video feed.")
    st.write("##")
    


    # Creating Angle finder class
    class angleFinder:
        def __init__(self,lmlist,p1,p2,p3,drawPoints):
            self.lmlist = lmlist
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3
            
            self.drawPoints = drawPoints
        #    finding angles

        def angle(self):
            if len(self.lmlist) != 0:
                point1 = self.lmlist[self.p1]
                point2 = self.lmlist[self.p2]
                point3 = self.lmlist[self.p3]
                

                x1,y1 = point1[1:-1]
                x2, y2 = point2[1:-1]
                x3, y3 = point3[1:-1]
                

                # calculating angle for left arm
                leftHandAngle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                            math.atan2(y1 - y2, x1 - x2))

                leftHandAngle = int(np.interp(leftHandAngle, [42,143], [100, 0]))
                

                # drawing circles and lines on selected points
                if self.drawPoints == True:
                    cv2.circle(img, (x1, y1), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x2, y2), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x3, y3), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x3, y3), 15, (0, 255, 0), 6)
                    

                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),4)
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 4)
                    

                return leftHandAngle
            
    if 'type' not in st.session_state:
        st.session_state.type = None


    def handle_click_start():
        st.session_state.type = "Start2"

    def handle_click_stop():
        st.write(st.session_state.counter2)
        st.session_state.type = "Stop2"
    
    start_button = st.button('Start', on_click=handle_click_start)
    stop_button = st.button('Stop',  on_click=handle_click_stop)

    # defining some variables
    counter = 0
    direction = 0

    frame_placeholder = st.empty()

    detector = PoseDetector(detectionCon=0.7,trackCon=0.7)

    


    if st.session_state['type']=='Start2':
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, img = cap.read()
            img = cv2.resize(img,(640,480))

            detector.findPose(img,draw=0)
            lmList, bboxInfo = detector.findPosition(img, bboxWithHands=0,draw=False)

            angle1 = angleFinder(lmList,12,14,16,drawPoints=True)
            left = angle1.angle()
            
            if left==None:
                left=0

            # Counting number of shoulder ups
            if left >= 90:
                if direction == 0:
                    counter += 0.5
                    st.session_state.counter2 = counter
                    direction = 1
            if left <= 70:
                if direction == 1:
                    counter += 0.5
                    st.session_state.counter2 = counter
                    direction = 0



            #putting scores on the screen
            cv2.rectangle(img,(0,0),(120,120),(255,0,0),-1)
            cv2.putText(img,str(int(counter)),(1,70),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.6,(0,0,255),6)

            # Converting values for rectangles
            leftval = np.interp(left,[0,100],[480,280])


            # Drawing left rectangle and putting text
            cv2.rectangle(img, (582, 280), (632, 480), (0, 0, 255), 5)
            cv2.rectangle(img, (582, int(leftval)), (632, 480), (0, 0, 255), -1)



            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            frame_placeholder.image(img, "RGB")

            cv2.waitKey(1)
            
    elif st.session_state['type']=='Stop2': 
        st.write("The video capture has ended")

        st.write("---------")
        st.write("## Analytics") 
        st.write("You did ",st.session_state.counter2," reps")   
        
        # calories2=3.8*weight2/st.session_state.counter2
        calories2=0.25*st.session_state.counter2
        if calories2<goal_calorie2:
            st.write("You have burned ",calories2,"kcal of calories")
            st.write("You have not achieved your goal. Try again")

        else:
            st.write("You have burned ",calories2,"kcal of calories")
            st.write("You have achieved your goal. Congratulations")
        
        fig = go.Figure(data=[go.Bar(x=['Bicep Curls'], y=[calories2], name='Calories Burned')])

        fig.add_trace(go.Bar(x=['Bicep Curls'], y=[goal_calorie2], name='Goal Calorie'))

        # Set chart layout
        fig.update_layout(
            title='Calories Burned for Bicep Curls',
            xaxis_title='Exercise',
            yaxis_title='Calories Burned'
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig)
    

elif app_mode == "Squats":
    st.markdown("## Squats")
    weight3 = st.slider('What is your weight?', 20, 130, 40)
    st.write("I'm ", weight3, 'kgs')

    st.write("-------------")

    goal_calorie3 = st.slider('Set a goal calorie to burn', 1, 200, 15)
    st.write("I want to burn", goal_calorie3, 'kcal')
    
    st.write("-------------")


    st.write(" Click on the Start button to start the live video feed.")
    st.write("##")


    # Creating Angle finder class
    class angleFinder:
        def __init__(self,lmlist,p1,p2,p3,p4,p5,p6,drawPoints):
            self.lmlist = lmlist
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3
            self.p4 = p4
            self.p5 = p5
            self.p6 = p6
            self.drawPoints = drawPoints
        #    finding angles

        def angle(self):
            if len(self.lmlist) != 0:
                point1 = self.lmlist[self.p1]
                point2 = self.lmlist[self.p2]
                point3 = self.lmlist[self.p3]
                point4 = self.lmlist[self.p4]
                point5 = self.lmlist[self.p5]
                point6 = self.lmlist[self.p6]

                x1,y1 = point1[1:-1]
                x2, y2 = point2[1:-1]
                x3, y3 = point3[1:-1]
                x4, y4 = point4[1:-1]
                x5, y5 = point5[1:-1]
                x6, y6 = point6[1:-1]

                # calculating angle for left leg
                leftLegAngle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                            math.atan2(y1 - y2, x1 - x2))

                leftLegAngle = int(np.interp(leftLegAngle, [42,143], [100, 0]))
                

                # drawing circles and lines on selected points
                if self.drawPoints == True:
                    cv2.circle(img, (x1, y1), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x2, y2), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x3, y3), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x3, y3), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x4, y4), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x4, y4), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x5, y5), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x5, y5), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x6, y6), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x6, y6), 15, (0, 255, 0), 6)

                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),4)
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 4)
                    cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 4)
                    cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 4)
                    cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 4)

                return leftLegAngle
            
    if 'type' not in st.session_state:
        st.session_state.type = None


    def handle_click_start():
        st.session_state.type = "Start3"

    def handle_click_stop():
        st.write(st.session_state.counter3)
        st.session_state.type = "Stop3"
    
    start_button = st.button('Start', on_click=handle_click_start)
    stop_button = st.button('Stop',  on_click=handle_click_stop)

    # defining some variables
    counter = 0
    direction = 0

    frame_placeholder = st.empty()

    detector = PoseDetector(detectionCon=0.7,trackCon=0.7)


    if st.session_state['type']=='Start3':
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, img = cap.read()
            img = cv2.resize(img,(640,480))

            detector.findPose(img,draw=0)
            lmList, bboxInfo = detector.findPosition(img, bboxWithHands=0,draw=False)

            angle1 = angleFinder(lmList,24,26,28,23,25,27,drawPoints=True)
            left = angle1.angle()
            
            if left==None:
                left=0

            # Counting number of shoulder ups
            if left >= 90:
                if direction == 0:
                    counter += 0.5
                    st.session_state.counter3 = counter
                    direction = 1
            if left <= 70:
                if direction == 1:
                    counter += 0.5
                    st.session_state.counter3 = counter
                    direction = 0



            #putting scores on the screen
            cv2.rectangle(img,(0,0),(120,120),(255,0,0),-1)
            cv2.putText(img,str(int(counter)),(1,70),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.6,(0,0,255),6)

            # Converting values for rectangles
            leftval = np.interp(left,[0,100],[480,280])


            # Drawing left rectangle and putting text
            cv2.rectangle(img, (582, 280), (632, 480), (0, 0, 255), 5)
            cv2.rectangle(img, (582, int(leftval)), (632, 480), (0, 0, 255), -1)


            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            frame_placeholder.image(img, "RGB")
            
            cv2.waitKey(1)
            
    elif st.session_state['type']=='Stop3': 
        st.write("The video capture has ended")

        st.write("---------")
        st.write("## Analytics") 
        st.write("You did ",st.session_state.counter3," reps")   
        
        # calories3=6.0*weight3/st.session_state.counter3
        calories3=0.3*st.session_state.counter3
        if calories3<goal_calorie3:
            st.write("You have burned ",calories3,"kcal of calories")
            st.write("You have not achieved your goal. Try again")

        else:
            st.write("You have burned ",calories3,"kcal of calories")
            st.write("You have achieved your goal. Congratulations")
        
        fig = go.Figure(data=[go.Bar(x=['Bicep Curls'], y=[calories3], name='Calories Burned')])

        fig.add_trace(go.Bar(x=['Bicep Curls'], y=[goal_calorie3], name='Goal Calorie'))

        # Set chart layout
        fig.update_layout(
            title='Calories Burned for Bicep Curls',
            xaxis_title='Exercise',
            yaxis_title='Calories Burned'
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig)

    

elif app_mode == "Pushups":
    st.markdown("## Pushups")
    weight4 = st.slider('What is your weight?', 20, 130, 40)
    st.write("I'm ", weight4, 'kgs')

    st.write("-------------")

    goal_calorie4 = st.slider('Set a goal calorie to burn', 1, 200, 15)
    st.write("I want to burn", goal_calorie4, 'kcal')
    
    st.write("-------------")


    st.write(" Click on the Start button to start the live video feed.")
    st.write("##")


    #cap = cv2.VideoCapture('vid1.mp4')
    

    def angles(lmlist,p1,p2,p3,p4,p5,p6,drawpoints):
            global counter
            global direction

            if len(lmlist)!= 0:
                point1 = lmlist[p1]
                point2 = lmlist[p2]
                point3 = lmlist[p3]
                point4 = lmlist[p4]
                point5 = lmlist[p5]
                point6 = lmlist[p6]

                x1,y1 = point1[1:-1]
                x2, y2 = point2[1:-1]
                x3, y3 = point3[1:-1]
                x4, y4 = point4[1:-1]
                x5, y5 = point5[1:-1]
                x6, y6 = point6[1:-1]

                if drawpoints == True:
                    cv2.circle(img,(x1,y1),10,(255,0,255),5)
                    cv2.circle(img, (x1, y1), 15, (0,255, 0),5)
                    cv2.circle(img, (x2, y2), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), 5)
                    cv2.circle(img, (x3, y3), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x3, y3), 15, (0, 255, 0), 5)
                    cv2.circle(img, (x4, y4), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x4, y4), 15, (0, 255, 0), 5)
                    cv2.circle(img, (x5, y5), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x5, y5), 15, (0, 255, 0), 5)
                    cv2.circle(img, (x6, y6), 10, (255, 0, 255), 5)
                    cv2.circle(img, (x6, y6), 15, (0, 255, 0), 5)

                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),6)
                    cv2.line(img, (x2,y2), (x3, y3), (0, 0, 255), 6)
                    cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 6)
                    cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 6)
                    cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 6)

                lefthandangle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                            math.atan2(y1 - y2, x1 - x2))

                righthandangle = math.degrees(math.atan2(y6 - y5, x6 - x5) -
                                            math.atan2(y4 - y5, x4 - x5))

                # print(lefthandangle,righthandangle)

                leftHandAngle = int(np.interp(lefthandangle, [-30, 180], [100, 0]))
                rightHandAngle = int(np.interp(righthandangle, [34, 173], [100, 0]))

                left, right = leftHandAngle, rightHandAngle

                if left >= 60 and right >= 60:
                    if direction == 0:
                        counter += 0.5
                        st.session_state.counter4 = counter
                        direction = 1
                if left <= 60 and right <= 60:
                    if direction == 1:
                        counter += 0.5
                        st.session_state.counter4 = counter
                        direction = 0

                cv2.rectangle(img, (0, 0), (120, 120), (255, 0, 0), -1)
                cv2.putText(img, str(int(counter)), (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

                leftval  = np.interp(right,[0,100],[400,200])
                rightval = np.interp(right, [0, 100], [400, 200])

                cv2.putText(img,'R', (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
                cv2.rectangle(img,(8,200),(50,400),(0,255,0),5)
                cv2.rectangle(img, (8, int(rightval)), (50, 400), (255,0, 0), -1)

                cv2.putText(img, 'L', (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 7)
                cv2.rectangle(img, (952, 200), (995, 400), (0, 255, 0), 5)
                cv2.rectangle(img, (952, int(leftval)), (995, 400), (255, 0, 0), -1)


                if left > 70:
                    cv2.rectangle(img, (952, int(leftval)), (995, 400), (0, 0, 255), -1)

                if right > 70:
                    cv2.rectangle(img, (8, int(leftval)), (50, 400), (0, 0, 255), -1)


    if 'type' not in st.session_state:
        st.session_state.type = None


    def handle_click_start():
        st.session_state.type = "Start4"

    def handle_click_stop():
        st.write(st.session_state.counter4)
        st.session_state.type = "Stop4"
    
    start_button = st.button('Start', on_click=handle_click_start)
    stop_button = st.button('Stop',  on_click=handle_click_stop)

    counter = 0
    direction = 0
    
    frame_placeholder = st.empty()

    pd = PoseDetector(detectionCon=0.7,trackCon=0.7)


    if st.session_state['type']=='Start4':
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret,img = cap.read()
            # if not ret:
            #     cap = cv2.VideoCapture('vid1.mp4')
            #     continue

            img = cv2.resize(img,(1000,500))
            #cvzone.putTextRect(img,'AI Push Up Counter',[345,30],thickness=2,border=2,scale=2.5)
            pd.findPose(img,draw=0)
            lmlist ,bbox = pd.findPosition(img ,draw=0,bboxWithHands=0)


            angles(lmlist,11,13,15,12,14,16,drawpoints=1)



            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            frame_placeholder.image(img, "RGB")

            cv2.waitKey(1)
            
    elif st.session_state['type']=='Stop4': 
        st.write("The video capture has ended")

        st.write("---------")
        st.write("## Analytics") 
        st.write("You did ",st.session_state.counter4," reps")   
        
        # calories4=8.0*weight4/st.session_state.counter4
        calories4=0.32*st.session_state.counter4
        if calories4<goal_calorie4:
            st.write("You have burned ",calories4,"kcal of calories")
            st.write("You have not achieved your goal. Try again")

        else:
            st.write("You have burned ",calories4,"kcal of calories")
            st.write("You have achieved your goal. Congratulations")
        
        fig = go.Figure(data=[go.Bar(x=['Bicep Curls'], y=[calories4], name='Calories Burned')])

        fig.add_trace(go.Bar(x=['Bicep Curls'], y=[goal_calorie4], name='Goal Calorie'))

        # Set chart layout
        fig.update_layout(
            title='Calories Burned for Bicep Curls',
            xaxis_title='Exercise',
            yaxis_title='Calories Burned'
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig)


elif app_mode == "Shoulder press":
    st.markdown("## Shoulder Press")
    weight5 = st.slider('What is your weight?', 20, 130, 40)
    st.write("I'm ", weight5, 'kgs')

    st.write("-------------")

    goal_calorie5 = st.slider('Set a goal calorie to burn', 1, 200, 15)
    st.write("I want to burn", goal_calorie5, 'kcal')
    
    st.write("-------------")


    st.write(" Click on the Start button to start the live video feed.")
    st.write("##")


    # Creating Angle finder class
    class angleFinder:
        def __init__(self,lmlist,p1,p2,p3,p4,p5,p6,drawPoints):
            self.lmlist = lmlist
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3
            self.p4 = p4
            self.p5 = p5
            self.p6 = p6
            self.drawPoints = drawPoints
        #    finding angles

        def angle(self):
            if len(self.lmlist) != 0:
                point1 = self.lmlist[self.p1]
                point2 = self.lmlist[self.p2]
                point3 = self.lmlist[self.p3]
                point4 = self.lmlist[self.p4]
                point5 = self.lmlist[self.p5]
                point6 = self.lmlist[self.p6]

                x1,y1 = point1[1:-1]
                x2, y2 = point2[1:-1]
                x3, y3 = point3[1:-1]
                x4, y4 = point4[1:-1]
                x5, y5 = point5[1:-1]
                x6, y6 = point6[1:-1]

                # calculating angle for left and right hands
                leftHandAngle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                            math.atan2(y1 - y2, x1 - x2))

                rightHandAngle = math.degrees(math.atan2(y6 - y5, x6 - x5) -
                                            math.atan2(y4 - y5, x4 - x5))

                leftHandAngle = int(np.interp(leftHandAngle, [-170, 180], [100, 0]))
                #rightHandAngle = int(np.interp(rightHandAngle, [-50, 20], [100, 0]))
                rightHandAngle = int(np.interp(rightHandAngle, [-170, 180], [100, 0]))
                

                # drawing circles and lines on selected points
                if self.drawPoints == True:
                    cv2.circle(img, (x1, y1), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x2, y2), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x3, y3), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x3, y3), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x4, y4), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x4, y4), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x5, y5), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x5, y5), 15, (0, 255, 0), 6)
                    cv2.circle(img, (x6, y6), 10, (0, 255, 255), 5)
                    cv2.circle(img, (x6, y6), 15, (0, 255, 0), 6)

                    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),4)
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 4)
                    cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 4)
                    cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 4)
                    cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 4)

                return list([leftHandAngle,rightHandAngle])
            
    if 'type' not in st.session_state:
        st.session_state.type = None


    def handle_click_start():
        st.session_state.type = "Start5"

    def handle_click_stop():
        st.write(st.session_state.counter5)
        st.session_state.type = "Stop5"
    
    start_button = st.button('Start', on_click=handle_click_start)
    stop_button = st.button('Stop',  on_click=handle_click_stop)

    # defining some variables
    counter = 0
    direction = 0

    frame_placeholder = st.empty()

    detector = PoseDetector(detectionCon=0.7,trackCon=0.7)


    if st.session_state['type']=='Start5':
        cap=cv2.VideoCapture(0)

        while cap.isOpened():
            ret, img = cap.read()
            img = cv2.resize(img,(1000,600))

            detector.findPose(img,draw=0)
            lmList, bboxInfo = detector.findPosition(img, bboxWithHands=0,draw=False)

            angle1 = angleFinder(lmList,11,13,15,12,14,16,drawPoints=True)
            hands = angle1.angle()

            if hands==None:
                continue

            left, right = hands[0:]

            # Counting number of shoulder ups
            if left >= 90 and right >= 90:
                if direction == 0:
                    counter += 0.5
                    st.session_state.counter5 = counter
                    direction = 1
            if left <= 70 and right <= 70:
                if direction == 1:
                    counter += 0.5
                    st.session_state.counter5 = counter
                    direction = 0



            #putting scores on the screen
            cv2.rectangle(img,(0,0),(120,120),(255,0,0),-1)
            cv2.putText(img,str(int(counter)),(1,70),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1.6,(0,0,255),6)

            # Converting values for rectangles
            leftval = np.interp(left,[0,100],[400,200])
            rightval = np.interp(right, [0, 100], [400, 200])

            # For color changing
            value_left = np.interp(left, [0, 100], [0, 100])
            value_right = np.interp(right,  [0, 100], [0, 100])

            # Drawing right rectangle and putting text
            cv2.putText(img,'R',(24,195),cv2.FONT_HERSHEY_DUPLEX,1,(255, 0, 0),5)
            cv2.rectangle(img,(8,200),(50,400),(0,255,0),5)
            cv2.rectangle(img, (8, int(rightval)), (50, 400), (255, 0, 0), -1)


            # Drawing left rectangle and putting text
            cv2.putText(img, 'L', (900,195),cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0),5)
            cv2.rectangle(img, (882, 200), (932, 400), (0, 255, 0), 5)
            cv2.rectangle(img, (882, int(leftval)), (932, 400), (255, 0, 0), -1)

            if value_left > 70:
                cv2.rectangle(img, (882, int(leftval)), (932, 400), (0, 0, 255), -1)

            if value_right > 70:
                cv2.rectangle(img, (8, int(rightval)), (50, 400), (0, 0, 255), -1)


            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

            frame_placeholder.image(img, "RGB")
            
            cv2.waitKey(1)
            
    elif st.session_state['type']=='Stop5': 
        st.write("The video capture has ended")

        st.write("---------")
        st.write("## Analytics") 
        st.write("You did ",st.session_state.counter5," reps")   
        
        # calories5=5.5*weight5/st.session_state.counter5
        calories5=0.22*st.session_state.counter5
        if calories5<goal_calorie5:
            st.write("You have burned ",calories5,"kcal of calories")
            st.write("You have not achieved your goal. Try again")

        else:
            st.write("You have burned ",calories5,"kcal of calories")
            st.write("You have achieved your goal. Congratulations")
        
        fig = go.Figure(data=[go.Bar(x=['Bicep Curls'], y=[calories5], name='Calories Burned')])

        fig.add_trace(go.Bar(x=['Bicep Curls'], y=[goal_calorie5], name='Goal Calorie'))

        # Set chart layout
        fig.update_layout(
            title='Calories Burned for Bicep Curls',
            xaxis_title='Exercise',
            yaxis_title='Calories Burned'
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig)