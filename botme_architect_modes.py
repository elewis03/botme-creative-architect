
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# UI config
st.set_page_config(page_title="BotMe – Creative Architect", layout="wide")
st.title("🧠 BotMe: Creative Architect Studio")

# Mode to prompt template mapping
modes = {
    "Design system": "Design a system for managing sustainable smart home communities using AI assistants.",
    "Map process": "Map out the user journey for a 55+ homebuyer finding a container-based home in Georgia.",
    "Generate blueprint": "Generate a blueprint for a personal AI that organizes creative projects.",
    "Startup Canvas": "Create a one-page startup canvas for an AI-powered health journaling app.",
    "Persona Builder": "Design a customer persona for a solo entrepreneur using productivity tools.",
    "Service Blueprint": "Build a service blueprint for an on-demand home repair app with AI support."
}

# Dropdown to select creative mode
mode = st.selectbox("🎨 Choose a creative mode:", list(modes.keys()))

# Auto-fill prompt with template
template_prompt = modes[mode]
prompt = st.text_area("🛠️ Customize or expand your design prompt:", value=template_prompt, height=180)

# On submit
if st.button("Generate Architect Insight"):
    if prompt:
        with st.spinner("Generating your architect insight..."):
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

                st.markdown("### ✨ Architect Insight")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a prompt first.")
