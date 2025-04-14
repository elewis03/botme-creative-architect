
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up the Streamlit page
st.set_page_config(page_title="BotMe – Creative Architect", layout="wide")
st.title("🧠 BotMe: Creative Architect Assistant")

# Mode selector
mode = st.selectbox(
    "Select your creative mode:",
    ["Design system", "Map process", "Generate blueprint"]
)

# Input prompt area
prompt = st.text_area("🛠️ What are we designing today?", height=160, placeholder="Example: Help me structure a sustainable housing assistant AI...")

# On button click, send the prompt to GPT
if st.button("Generate Architect Insight"):
    if prompt:
        with st.spinner(f"Creating {mode.lower()}..."):
            try:
                system_prompt = f"""You are BotMe, a creative architect assistant.

You do not explain your process. You structure thoughts clearly, help design high-level systems, and use frameworks when possible.
You think like an architect of ideas — always seeking clarity, flow, and creative alignment.
Speak like a product strategist, not a chatbot.

Your current mode is: {mode}.
Respond accordingly with well-structured insight focused on that mode.
"""
                messages = [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7
                )
                # Output the result
                st.markdown("### ✨ Architect Insight")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("Please enter a design challenge or idea first.")
