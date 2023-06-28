import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
# from pydataset import data
from streamlit_extras.no_default_selectbox import selectbox
import matplotlib.pyplot as plt

st.set_page_config(page_title='Nutrition Calorie Tracker', layout='wide')

html = """
<div style="background-color:#025246 ;padding:10px">
<h2 style="color:white;text-align:center;">Nutrition</h2>
</div>"""
st.markdown(html, unsafe_allow_html=True) 

st.write("")

# st.title('Nutrition Calorie Tracker')
df=pd.read_csv("./food1.csv", encoding='mac_roman')
ye=st.number_input('Enter Number of dishes', min_value=1, max_value=10)
i=0
j=0
calories=0
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]
list7=[]
list8=[]


try:
    while(i<ye):
        st.write("--------------------")
        sel=selectbox('Select the food ',df['Shrt_Desc'].unique(),no_selection_label=" ",key=i)
        list1.append(sel)
        sel_serving=st.number_input('Select the number of servings ',min_value=1,max_value=10,value=1,step=1,key=j+100)
        # list2.append(sel_serving)
        i=i+1
        j=j+1
        st.write("Food : ",sel)
        st.write("Serving : ",sel_serving)
        st.write("Calories per serving : ",df[df['Shrt_Desc']==sel]['Energ_Kcal'].values[0])
        cal= df[df['Shrt_Desc']==sel]['Energ_Kcal'].values[0]*sel_serving
        list2.append(cal)
        st.write("Total calories for ",sel_serving,"servings of ",sel ,"= ",cal,"Energ_Kcal")
        
        #protine

        protine= df[df['Shrt_Desc']==sel]['Protein_(g)'].values[0]*sel_serving
        list3.append(protine)
        
        carbs= df[df['Shrt_Desc']==sel]['Carbohydrt_(g)'].values[0]*sel_serving
        list4.append(carbs)
        
        fat= df[df['Shrt_Desc']==sel]['Lipid_Tot_(g)'].values[0]*sel_serving
        list5.append(fat)
        
        sugar= df[df['Shrt_Desc']==sel]['Sugar_Tot_(g)'].values[0]*sel_serving
        list7.append(sugar)
        
        calcium= df[df['Shrt_Desc']==sel]['Calcium_(mg)'].values[0]*sel_serving
        list8.append(calcium)
        
        calories += cal
   
    
    st.write("Total Calories:", calories)
    st.write("--------------------")
    

    col1,col2,col3=st.columns(3)

    # Create pie chart
    with col1:
        fig = go.Figure(data=[go.Pie(labels=list1, values=list2, textinfo='percent', insidetextorientation='radial')])
        fig.update_layout(title="Calorie Breakdown")
        st.plotly_chart(fig)
    with col2:
        fig1 = go.Figure(data=[go.Pie(labels=list1, values=list3, textinfo='percent', insidetextorientation='radial')])
        fig1.update_layout(title="Protein Breakdown")
        st.plotly_chart(fig1)
    with col3:
        fig2 = go.Figure(data=[go.Pie(labels=list1, values=list4, textinfo='percent', insidetextorientation='radial')])
        fig2.update_layout(title="Carbs Breakdown")
        st.plotly_chart(fig2)
    with col1:
        fig3 = go.Figure(data=[go.Pie(labels=list1, values=list5, textinfo='percent', insidetextorientation='radial')])
        fig3.update_layout(title="Fat Breakdown")
        st.plotly_chart(fig3)
    with col3:
        fig5 = go.Figure(data=[go.Pie(labels=list1, values=list7, textinfo='percent', insidetextorientation='radial')])
        fig5.update_layout(title="Sugar Breakdown")
        st.plotly_chart(fig5)
    
except:
    st.write("")