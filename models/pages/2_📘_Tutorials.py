import streamlit as st
import json

import requests  
import streamlit as st  
from streamlit_lottie import st_lottie  
from PIL import Image


# Lottie Files: https://lottiefiles.com/

html = """
<div style="background-color:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;">Tutorial</h2>
</div>"""
st.markdown(html, unsafe_allow_html=True)


# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()
    

# lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")



# New
img1 = Image.open("./images/dumbbell.webp")
img2= Image.open("./images/squats.jpg")
img3 = Image.open("./images/pushups.jpeg")
img4 = Image.open("./images/shoulder.jpeg")


app_mode = st.sidebar.selectbox("Choose the tutorial", ["About","Bicep Curls","Squats","Pushups","Shoulder press"])
if app_mode == "About":
    #st_lottie(lottie_hello,key="hello")
    
    with st.container():
        st.write("---")
        st.header("Have a look at these video tutorials")
        st.write("##")
        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.image(img1, width=325)
        with text_column:
            st.subheader("Bicep Curls")
            st.write(
                """
                Get armed with knowledge! Watch this bicep curl tutorial and unlock the secret to sleeve-busting strength!
                """
            )
            st.markdown("[Watch Video...](https://youtu.be/ykJmrZ5v0Oo)")
    
        
    with st.container():
        image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img2, width=325)
    with text_column:
        st.subheader("Squats")
        st.write(
            """
            Get lower, get stronger! Dive into this squat tutorial and unlock the power of a rock-solid foundation!.
            """
        )
        st.markdown("[Watch Video...](https://youtu.be/YaXPRqUwItQ)")
    
    with st.container():
        image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img3, width=325)
    with text_column:
        st.subheader("Pushups")
        st.write(
            """
            Push your limits, pump up your power! Join us for this push-up tutorial and unleash your inner strength!.
            """
        )
        st.markdown("[Watch Video...](https://youtu.be/IODxDxX7oi4)")

    with st.container():
        image_column, text_column = st.columns((1, 2))
    with image_column:
        st.image(img4, width=325)
    with text_column:
        st.subheader("Shoulder press")
        st.write(
            """
            Elevate your strength, shoulder to shoulder! Don't miss this shoulder press tutorial to reach new heights of power!.
            """
        )
        st.markdown("[Watch Video...](https://youtu.be/qEwKCR5JCog)")


elif app_mode == "Bicep Curls":
    st.markdown("## Bicep Curls")
    st.markdown("Here's a step-by-step tutorial for bicep curls:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("##")
        st.write("""
        - Stand up straight with a dumbbell in each hand. Keep your elbows close to your torso and rotate the palms of your hands until they are facing forward. This will be your starting position.
        
        - Now, keeping the upper arms stationary, exhale and curl the weights while contracting your biceps. 
        
        - Continue to raise the weights until your biceps are fully contracted and the dumbbells are at shoulder level. 
        
        - Hold the contracted position for a brief pause as you squeeze your biceps.
        
        - Then, inhale and slowly begin to lower the dumbbells back to the starting position.
        
        Remember, it's important to use appropriate weight for your fitness level and gradually increase the resistance as you get stronger.    
        """)
    with col2:
        st.image("./gif/bicep.gif")



elif app_mode == "Squats":
    st.markdown("## Squats")
    st.markdown("Here's a step-by-step tutorial for performing Squats:")
    
    col1, col2 = st.columns(2)
    st.write("##")
    with col1:
        st.write("""
        - Stand with your feet slightly wider than shoulder-width apart, toes pointing slightly outward. You can also experiment with different foot positions to find what's most comfortable for you.
        
        - Engage your core muscles by pulling your belly button in towards your spine. Keep your back straight and maintain good posture throughout the exercise.
        
        - Begin the squat by bending your knees and pushing your hips back, as if you're sitting back into a chair. Make sure to keep your weight on your heels and your knees tracking in line with your toes.
        
        - Lower your body down until your thighs are parallel to the ground. If you have the flexibility and mobility, you can go lower, but it's important to maintain proper form throughout the movement.
        
        - Pause for a moment at the bottom of the squat, and then begin to push through your heels and straighten your legs to return to the starting position. Keep your core engaged and maintain control of the movement.
        
        - As you come back up, avoid locking your knees at the top. Maintain a slight bend in your knees to keep tension on the muscles and avoid unnecessary strain.
        
        - Repeat the squat for your desired number of repetitions. Start with a weight or bodyweight that allows you to maintain proper form, and gradually increase the difficulty as you become more comfortable and stronger.

        Additional tips:
        - Keep your chest up and your gaze forward throughout the exercise. Avoid rounding your back or looking down.
        - Exhale as you push up from the squat and inhale as you lower down. Breathing properly helps stabilize your core and maintain control.

        Remember, it's important to listen to your body and start with a weight or intensity level that is appropriate for your fitness level. Gradually progress as you gain strength and confidence in your squatting technique.   
        """)
    with col2:
        st.image("./gif/squats.gif")

elif app_mode == "Pushups":
    st.markdown("## Pushups")
    st.markdown("Here's a step-by-step tutorial for performing Pushups:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("##")
        st.write("""
        - Start in a high plank position with your palms flat on the floor, hands shoulder-width apart, shoulders stacked directly above your wrists, legs extended behind you, and your core and glutes engaged.

        - Bend your elbows and begin to lower your body down to the floor. When your chest grazes it, extend your elbows and return to the start. Focus on keeping your elbows close to your body during the movement.

        - Complete as many reps as you can with good form. If you can't perform at least 3–5 reps, modify the movement by dropping to your knees or doing wall push-ups.

        Remember, it's important to listen to your body and start with a weight or intensity level that is appropriate for your fitness level. Gradually progress as you gain strength and confidence in your pushup technique.
   
        """)
    with col2:
        st.image("./gif/pushups.gif")

elif app_mode == "Shoulder press":
    st.markdown("## Shoulder press")
    st.markdown("Here's a step-by-step tutorial for performing Shoulder Press:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("##")
        st.write("""
        - Stand with your feet shoulder-width apart and hold a dumbbell in each hand. Raise the dumbbells to your shoulders, palms facing forward. This is your starting position.

        - Press the weights upward until your arms are fully extended overhead. Keep your head and neck stationary.

        - Pause at the top, then lower the weights back to the starting position.

        Remember, it's important to listen to your body and start with a weight or intensity level that is appropriate for your fitness level. Gradually progress as you gain strength and confidence in your shoulder press technique.
   
        """)
    with col2:
        st.image("./gif/shoulder.gif")