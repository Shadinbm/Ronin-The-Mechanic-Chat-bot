from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import re
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI(title='Ronin The Mechanic API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
tfidf=joblib.load('models/tfidfvectorizer.pkl')
model=joblib.load('models/model.pkl')
df=pd.read_csv('data/main_data.csv')
nlp=spacy.load('en_core_web_lg')
def preprocess(text):
    text=str(text).strip().lower()
    text=re.sub(r"[^a-z\s]"," ",text)
    doc=nlp(text)
    token=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.lemma_)>2]
    return " ".join(token)
class InputText(BaseModel):
    message:str
@app.get("/")
def home():
    return {"message": "Ronin RE Bot API is running! Use POST /predict to get results."}


@app.post("/predict")
def predict(data:InputText):
    user_input=preprocess(data.message)
    user_vec = tfidf.transform([user_input])
    
    type={0: 'body', 1: 'brake', 2: 'clutch', 3: 'drivetrain', 4: 'electrical', 5: 'engine', 6: 'exhaust', 7: 'fuel', 8: 'gear', 9: 'noise', 10: 'starting', 11: 'suspension', 12: 'wheels'}

    predicted_type = model.predict(user_vec)[0]
    
 
    subset = df[df["complaint_label"] == predicted_type]
    
    
    
    subset_vecs = tfidf.transform(subset["complints_lemma"])
    sims = cosine_similarity(user_vec,subset_vecs ).flatten()
    idx = sims.argmax()
    row = subset.iloc[idx]
    return {
        "predicted_type": type.get(predicted_type,-1),
        "possible_cause": row["initial_diagnosis"],
        "initial_advice": row["initial_advice"],
        "mechanic_diagnosis": row["mechanic_diagnosis"],
        "fix": row["resolution"],
        "spare_parts": row["spares_replaced"],
        "estimated_cost": int(row["spare_cost"]),
    }

