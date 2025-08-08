import streamlit as st
import requests
import google.generativeai as genai

import google.generativeai as genai

genai.configure(api_key="AIzaSyCH3JIdg2sObRemJiqIUk-DrTlGXqx87z4")

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

st.title("📚Edutech Learning Platform")

selection=st.sidebar.selectbox("Choose the page",["Submit Learning Data","Recommendation","Feedback","Chat tutor"])

if selection == "Submit Learning Data":
    st.header("Submit Learning Form")
    with st.form("suv=bmit form"):
        user_id=st.number_input("User Id")
        topic=st.selectbox("Topics",["Algebra","Trigonometry","Probability","Feedback","Statistics","Calculus","Limits","Functions","Derivatives"])
        time_spent=st.slider("Time Spend",1,100)
        quiz_score=st.slider("Quiz_score",0,100)
        preference=st.selectbox("Preference",["Visual","Text","Audio","Internet"])
        feedback=st.text_area("Feedback")
        rating=st.slider("Ratings",1,5)
        submit=st.form_submit_button("submit")
        if submit:
            datas={
                "user_id":user_id,
                "topic":topic,
                "time_spent":time_spent,
                "quiz_score":quiz_score,
                "preference":preference,
                "feedback":feedback,
                "rating":rating
            }

            res=requests.post("http://127.0.0.1:8000/submit",json=datas)
            st.success(res.json()["Message"])

elif(selection=="Feedback"):
    st.header("Feedback Sentiment Analysis")
    feedback=st.text_area("Feedback:")
    if st.button("submit Feedback"):
        res=requests.post("http://127.0.0.1:8000/feedback",json={"feedback":feedback})
        st.write(res.json()["Feedback"])

elif(selection=="Chat tutor"):
    st.header("🤖 AI Tutor ChatBot")
    prmt=st.text_input("Ask Your Doubts:")
    chat=model.start_chat(history=[])
    if st.button("Clear The Doubt"):
        res=chat.send_message(prmt)
        st.write("Tutor Response")
        st.write(res.text)

elif(selection=="Recommendation"):
    userid=st.number_input("Enter the user Id",min_value=1,step=1)
    if st.button("Recommend"):
        res=requests.get(f"http://127.0.0.1:8000/get_recommend/{userid}")
        response=res.json()
        st.write("Recommended Topics!!")
        st.write(response.get("recommend","No recommendation available."))