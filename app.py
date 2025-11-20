import streamlit as st
import requests

st.set_page_config(page_title="Ronin BOT", page_icon="logobot.png")
st.image("logobot.png", width=250)
st.title("Ronin The Mechanic")
st.write("Hello Royal Enfield Customer!! Describe Your Bike problem and I’ll diagnose it!")

API_URL = "http://127.0.0.1:8000/predict"

# ---------------------- SESSION VARIABLES ----------------------
if "step" not in st.session_state:
    st.session_state["step"] = "greet"

if "model" not in st.session_state:
    st.session_state["model"] = None

if "engine_cc" not in st.session_state:
    st.session_state["engine_cc"] = None

if "complaint" not in st.session_state:
    st.session_state["complaint"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------------- DISPLAY CHAT HISTORY ----------------------
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------------- USER INPUT ----------------------
user_input = st.chat_input("Tell me your complaint")

if user_input:

    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # ---------------------- BOT LOGIC ----------------------
    if st.session_state["step"] == "greet":
        if user_input.lower() in ["hi", "hello", "hey", "hola"]:
            bot_reply = (
                "Hello! I’m Ronin, your Royal Enfield mechanic assistant. \n\n"
                "What is your bike model?"
            )
        else:
            bot_reply = "Hi! Before I diagnose the issue, please tell me your bike model."

        st.session_state["step"] = "ask_model"

    elif st.session_state["step"] == "ask_model":
        st.session_state["model"] = user_input
        bot_reply = (
            f"Got it — **{user_input}**. 👍\n\n"
            "Now tell me the engine capacity (e.g., 350cc, 411cc, 650cc)."
        )
        st.session_state["step"] = "ask_cc"

    elif st.session_state["step"] == "ask_cc":
        st.session_state["engine_cc"] = user_input
        bot_reply = "Great! Now please describe your complaint in detail."
        st.session_state["step"] = "ask_complaint"

    elif st.session_state["step"] == "ask_complaint":
        st.session_state["complaint"] = user_input

        payload = {"message": user_input}

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()

                bot_reply = f"""Looks Like Your Bike Have complaint on
                   **{data['predicted_type']}** part

                  Possible Cause is may be  
                  {data['possible_cause']}

                  my Initial Advice is to: 
                  {data['initial_advice']}

                  from my past data matched Mechanic Diagnosis: 
                  {data['mechanic_diagnosis']}

                   Fix done by mechanic:
                  {data['fix']}

                  ⚙ Spare Parts Needed:  
                  {data['spare_parts']}

                  💰 Estimated Cost of spare part: 
                  ₹{data['estimated_cost']}
                 """ 
            else:
                bot_reply = "⚠️ Error connecting to API."

        except Exception:
            bot_reply = "⚠️ Could not reach FastAPI. Make sure API is running."

        st.session_state["step"] = "greet"

    # ---------------------- SHOW BOT MESSAGE ----------------------
    st.chat_message("assistant").write(bot_reply)
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
