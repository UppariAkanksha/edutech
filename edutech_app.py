import streamlit as st
import requests
import  google.generativeai as  genai

genai.configure(api_key="AIzaSyCL8bTj2pysQZiPk5hF6YKg-z4-8JXro5E")

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

st.title("📖Edutech Learning Platform📚")


selection = st.sidebar.selectbox("Choose the page", ["Submit Learning Data", "Recommendation", "Feedback", "Chat tutor"])

if selection == "Submit Learning Data":
    st.header("Submit Learning Form")
    with st.form("submit_form"):
        user_id = st.number_input("User Id", min_value=1, step=1)
        topic = st.selectbox("Topics", ["Algebra", "Trigonometry", "Probability", "Feedback", "Statistics", "Calculus", "Limits", "Functions", "Derivatives"])
        time_spent = st.slider("Time Spent (minutes)", 1, 100)
        quiz_score = st.slider("Quiz Score", 0, 100)
        preference = st.selectbox("Preference", ["Visual", "Text", "Audio", "Internet"])
        feedback = st.text_area("Feedback")
        rating = st.slider("Ratings", 1, 5)
        submit = st.form_submit_button("Submit")

        if submit:
            datas = {
                "user_id": user_id,
                "topic": topic,
                "time_spent": time_spent,
                "quiz_score": quiz_score,
                "preference": preference,
                "feedback": feedback,
                "rating": rating
            }
            try:
                res = requests.post("http://127.0.0.1:8000/submit", json=datas)
                res.raise_for_status()
                st.success(res.json().get("Message", "Submitted successfully!"))
            except Exception as e:
                st.error(f"Failed to submit data: {e}")

elif selection == "Feedback":
    st.header("Feedback Sentiment Analysis")
    feedback = st.text_area("Feedback:")
    if st.button("Submit Feedback"):
        if feedback.strip() == "":
            st.warning("Please enter some feedback.")
        else:
            try:
                res = requests.post("http://127.0.0.1:8000/feedback", json={"feedback": feedback})
                res.raise_for_status()
                st.write(res.json().get("Feedback", "No sentiment returned."))
            except Exception as e:
                st.error(f"Failed to analyze feedback: {e}")


elif selection == "Chat tutor":
    st.header("🤖 AI Tutor ChatBot")
    prmt = st.text_input("Ask Your Doubts:")
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    if st.button("Clear The Doubt"):
        if prmt.strip() == "":
            st.warning("Please enter a question.")
        else:
            try:
                res = st.session_state.chat.send_message(prmt)
                st.write("Tutor Response:")
                st.write(res.text)
            except Exception as e:
                st.error(f"Error during AI response: {e}")


elif selection == "Recommendation":
    userid = st.number_input("Enter the User ID", min_value=1, step=1)
    if st.button("Recommend"):
        try:
            res = requests.get(f"http://127.0.0.1:8000/get_recommend/{userid}")
            res.raise_for_status()
            response = res.json()
            st.write("Recommended Topics!!")
            st.write(response.get("recommend", "No recommendation available."))
        except Exception as e:
            st.error(f"Failed to get recommendations: {e}")
