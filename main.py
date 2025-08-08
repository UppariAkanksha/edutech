from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import random
from transformers import pipeline

app = FastAPI()

df = pd.read_csv("C:/Users/sunit/OneDrive/Desktop/edutech/edtech_adaptive_learning_dataset.csv")

class FormInput(BaseModel):
    user_id: int
    topic: str
    time_spent: int
    quiz_score: int
    preference: str
    feedback: str
    rating: int


class FeedbackInput(BaseModel):
    feedback: str


@app.post("/submit")
def form_submit(data: FormInput):
    global df
    new_data = pd.DataFrame([data.dict()])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("C:/Users/sunit/OneDrive/Desktop/edutech/edtech_adaptive_learning_dataset.csv", index=False)
    return {"message": "Data submitted successfully"}


@app.get("/get_recommend")
def recommend(userid: int):
    user = df[df["user_id"] == userid]
    if user.empty:
        return {"message": "User Not Found"}
    
    visited_topics = user["topic"].unique().tolist()
    all_topics = df["topic"].unique().tolist()
    not_visited = list(set(all_topics) - set(visited_topics))

    recommendations = random.sample(not_visited, k=min(3, len(not_visited)))
    return {"recommendations": recommendations}


@app.post("/feedback")
def feedback_analysis(fb: FeedbackInput):
    ml = pipeline("sentiment-analysis")
    res = ml(fb.feedback)
    return {"Feedback": res[0]}

   


