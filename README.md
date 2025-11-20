Ronin RE Bot — AI Mechanic Assistant for Royal Enfield

Ronin RE Bot is an AI-powered mechanic assistant built for Royal Enfield motorcycles.
It listens to user complaints, predicts the possible issue, retrieves similar past complaints, and provides:

🔧 Predicted Issue Type

🧩 Possible Cause

⚙️ Initial Advice

🔧 Mechanic Diagnosis

🛠 Past Successful Fix

📦 Spare Parts Required

💰 Estimated Repair Costs

This is a complete end-to-end machine learning project with dataset creation, model training, API, and chatbot UI.

🚀 Features
✔ Intelligent Complaint Understanding

Learns from thousands of historical cases to classify issues such as:

engine, electrical, brake, fuel, gear, noise, starting, clutch, wheels, etc.

✔ Human-like Diagnosis

Mechanic-style diagnosis generated from real-world patterns.

✔ Spare Part Pricing

Integrated real Royal Enfield spare part price ranges.

✔ Streamlit Chat UI

Interactive assistant that talks like a garage mechanic.

✔ FastAPI Backend

High-performance REST API serving ML predictions.
📦 Dataset

Total dataset size: ~26,000 rows

13 Complaint Types (2,000 rows each)

body

brake

clutch

drivetrain

electrical

engine

exhaust

fuel

gear

noise

starting

suspension

wheels

Columns include:
complaint_id
model_name
engine_cc
km_run
complaint
complaint_label
initial_diagnosis
initial_advice
mechanic_diagnosis
resolution
spares_replaced
spare_cost
labour_charge
estimated_cost
complints_lemma

Additional Features:

Real Royal Enfield spare part prices mapped for cost realism.

🧠 NLP Pipeline
Phase 1 — spaCy Preprocessing
def preprocess(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z\s]", " ", text)
    doc = nlp(text)
    tokens = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]
    return " ".join(tokens)

Phase 2 — TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000)
X = tfidf.fit_transform(df["complints_lemma"])

Phase 3 — Naive Bayes Classification
model = MultinomialNB()
model.fit(X, df["complaint_label"])

Phase 4 — Similarity-based Retrieval
subset_vecs = tfidf.transform(subset["complints_lemma"])
sims = cosine_similarity(user_vec, subset_vecs).flatten()
best_index = sims.argmax()
row = subset.iloc[best_index]

⚙️ FastAPI Backend

Located in:

backend/main.py


Provides:

POST /predict


Body:

{ "message": "my bike producing knocking sound" }


Returns:

predicted issue

possible cause

advice

mechanic diagnosis

fix

spare parts

estimated cost

💬 Streamlit Chatbot UI

Located in:

frontend/app.py


Features:

Greeting flow

Asks for bike model

Asks for engine capacity

Accepts complaint

Sends API request

Generates complete mechanic-style response

🛠 Technologies Used
Machine Learning

scikit-learn (TF-IDF, Naive Bayes)

numpy

pandas

NLP

spaCy (en_core_web_lg)

Backend

FastAPI

Pydantic

Uvicorn

Frontend

Streamlit

📚 Future Enhancements

Add RAG system for more dynamic explanations

Add multilingual support

Add images (user uploads bike photos)

Create mobile app version

Add live service center locator

🏁 Conclusion

Ronin RE Bot is a fully functional AI-powered mechanic assistant.
It demonstrates complete ML development—from dataset generation to NLP pipeline, modeling, API, and user-facing chatbot interface.

Perfect for:

ML/AI portfolio

End-to-end project demo

Automobile industry applications

Student/academic showcase
