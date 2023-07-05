# AI-Fitness-Trainer
This is a web application with followng features:
1. Ecxercise form tracking.
2. Rep counting.
3. Tutorials of each excercise(both video as well as text based)
4. Daily Nutrition Tracker
5. FitBot(Our chatbot)


## Home Page
- Contains a brief of what we offer.
- Contains a music playlist to pump up your workout regime.
- Also contains a podcast playlist(for guidance and motivation)
  
https://github.com/Chandan-h-509/AI-Fitness-Trainer/assets/76171489/e502f9d4-8a82-47da-9637-41df30f594ba

## Training Arena
Here's where the fun begins. You get to choose the excercise which you want to perform and our model tracks your form and reps.

Available Excercises:
- Left Bicep Curl
- Right Bicep Curl
- Squats
- Pushups
- Shoulder Press
  
Here is a sample video to track your left Bicep Curl:

https://github.com/Chandan-h-509/AI-Fitness-Trainer/assets/76171489/7370a00c-0b7e-4df7-abee-3868ef94e286

 
Here is a sample video to track Shoulder Press:

https://github.com/Chandan-h-509/AI-Fitness-Trainer/assets/76171489/0423948f-2fbc-4eb2-8b2b-0610a10a2040

## Nutrition Tracker
- The user can track his/her nutrition by listing out the food items they ate for a particular meal.
- This helps one to monitor their food diet and adjust their next meal accordingly.

https://github.com/Chandan-h-509/AI-Fitness-Trainer/assets/76171489/8b8a50cd-526d-4b55-834c-d1fb18b164ef

Finally, a chatbot is also integrated which answers questions on fitness and fitness related queries.

## Tech Stack
- OpenCV: To allow access of webcamera and convert the live feed to frames so that neccessary operations can be performed.
- Mediapipe: To extract key-points from the human body which helps to calculate angles between different body parts.
- Stramlit: Python based framework to develop website.
- OpenAI: To build the chat bot.

## Note:
- Make sure to use your OpenAi API key to enable the chatbot.(Change to be made in 4_🤖_Chatbot.py file)
- Make sure to put in your email id to allow form submission.(Change to be made in 1_🏠_Home.py file)

## How to run
- Clone the repository
```
git clone https://github.com/Chandan-h-509/AI-Fitness-Trainer
```
- Go to the models directory
```
cd models
```
- Run the website
```
streamlit run 1_🏠_Home.py
```
Feel free to raise any issues/bugs/suggestions in the issues page of this repository.

Thank You!!
