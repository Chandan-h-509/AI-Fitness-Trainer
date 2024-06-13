# # Main file for the project
# import streamlit as st
# import requests
# from streamlit_lottie import st_lottie

# html = """
#     <div style="background-color:#025246 ;padding:10px">
#     <h2 style="color:white;text-align:center;">AI Fitness Trainer</h2>
#     </div>"""
# st.markdown(html, unsafe_allow_html=True)

# col1, col2 = st.columns([10,8], gap="large")

# with col1:
#     st.write("## Trainer")


# frame_placeholder = st.empty()
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_hello = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_FYx0Ph.json")

# with col2:
#    st_lottie(lottie_hello,key="hello1", height=500, width=400)
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image


# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Fitness Trainer", page_icon=":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("E:\AI Fitness Trainer\models\styles\styles.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_FYx0Ph.json")
music = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ikk4jhps.json")
podcast = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_JjpNLdaKYX.json")


img_contact_form = Image.open("./images/home.jpg")
img_lottie_animation = Image.open("./images/home.jpg")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hello, welcome to our website :wave:")
    st.title("AI Fitness Trainer")
    st.write(
        "Step into a fitter future: Welcome to your fitness revolution!"
    )
    #st.write("[Learn More >](https://pythonandvba.com)")

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    st.write("## About us :point_down:")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("")
        #st.write("##")
        st.write(
            """
            - We are thrilled to have you here on our platform dedicated to empowering and inspiring individuals on their journey towards a healthier and fitter lifestyle. Whether you're a seasoned fitness enthusiast or just starting your fitness journey, we have everything you need to reach your goals and achieve the best version of yourself.
            
            - What sets us apart is the fact that we provide personalized assistance at the comfort of your home or any place of your choice at a price that is both convenient and much cheaper that traditional gyms.

            Let your fitness journey start here!
            Join us today and embark on a transformative experience that will enhance your physical and mental well-being. Let's build strength, resilience, and a healthier future together!
            """
        )

    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

# ---- PROJECTS ----
with st.container():
    st.write("---")
    st.header("Get fit, Jam on, Repeat :headphones:")
    st.write("##")
    image_column, text_column = st.columns((1, 2))
    with image_column:
        #st.image(img_lottie_animation)
        st_lottie(music, height=300, key="music")
    with text_column:
        st.write("##")
        st.subheader("Workout music")
        st.write(
            """
            Power up your workout with the ultimate music fuel!
            """
        )
        st.markdown("[Have a Listen...](https://open.spotify.com/playlist/6N0Vl77EzPm13GIOlEkoJn?si=9207b7744d094bd3)")
with st.container():
    image_column, text_column = st.columns((1, 2))
    with image_column:
        #st.image(img_contact_form)
        st_lottie(podcast, height=300, key="podcast")
    with text_column:
        st.write("##")
        st.subheader("Podcast")
        st.write(
            """
            Take your workouts to the next level with our immersive podcast that pumps you up from start to finish!
            """
        )
        st.markdown("[Have a listen...](https://open.spotify.com/playlist/09Ig7KfohF5WmU9RhbDBjs?si=jyZ79y3wQgezrEDHim0NvQ)")

# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")

    # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
    contact_form = """
    <form action="https://formsubmit.co/c722428e42528bf09a0c149f6b7d3909" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()