
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database setup
conn = sqlite3.connect("architect_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    mode TEXT,
    prompt TEXT,
    response TEXT,
    timestamp TEXT
)''')
conn.commit()

# UI config
st.set_page_config(page_title="BotMe – Creative Architect", layout="wide")
st.title("🧠 BotMe: Creative Architect Studio")

# User identification
user = st.text_input("🔐 Enter your username or email to track your history:", key="user_input")

# Mode and prompt templates
modes = {
    "Design system": "Design a system for managing sustainable smart home communities using AI assistants.",
    "Map process": "Map out the user journey for a 55+ homebuyer finding a container-based home in Georgia.",
    "Generate blueprint": "Generate a blueprint for a personal AI that organizes creative projects.",
    "Startup Canvas": "Create a one-page startup canvas for an AI-powered health journaling app.",
    "Persona Builder": "Design a customer persona for a solo entrepreneur using productivity tools.",
    "Service Blueprint": "Build a service blueprint for an on-demand home repair app with AI support."
}

mode = st.selectbox("🎨 Choose a creative mode:", list(modes.keys()))
template_prompt = modes[mode]
prompt = st.text_area("🛠️ Customize or expand your design prompt:", value=template_prompt, height=180)

if "architect_output" not in st.session_state:
    st.session_state.architect_output = ""

# Generate insight
if st.button("Generate Architect Insight"):
    if prompt and user:
        with st.spinner("Generating insight..."):
            try:
                system_prompt = f"""You are BotMe, a creative architect assistant.

Your current creative mode is: {mode}.
You do not explain your process. You structure thoughts clearly, help design high-level systems, and use frameworks when possible.
You think like an architect of ideas — always seeking clarity, flow, and creative alignment.
Speak like a product strategist, not a chatbot."""

                messages = [
                    { "role": "system", "content": system_prompt },
                    { "role": "user", "content": prompt }
                ]

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7
                )

                output = response.choices[0].message.content
                st.session_state.architect_output = output

                # Save to database
                cursor.execute(
                    "INSERT INTO history (user, mode, prompt, response, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (user, mode, prompt, output, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()

                st.markdown("### ✨ Architect Insight")
                st.markdown(output)

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter both your user name and a prompt.")

# Display history
if user:
    st.sidebar.title("🗂️ Your Past Architect Sessions")
    cursor.execute("SELECT id, timestamp, mode FROM history WHERE user = ? ORDER BY timestamp DESC LIMIT 10", (user,))
    rows = cursor.fetchall()
    for row in rows:
        if st.sidebar.button(f"[{row[1]}] {row[2]}", key=row[0]):
            cursor.execute("SELECT prompt, response FROM history WHERE id = ?", (row[0],))
            record = cursor.fetchone()
            if record:
                st.session_state.architect_output = record[1]
                st.markdown("### 🧠 Recalled Prompt")
                st.markdown(record[0])
                st.markdown("### 🔁 Recalled Response")
                st.markdown(record[1])
