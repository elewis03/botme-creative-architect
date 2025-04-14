
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from fpdf import FPDF
import base64

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

# Save state
if "architect_output" not in st.session_state:
    st.session_state.architect_output = ""

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

                output = response.choices[0].message.content
                st.session_state.architect_output = output

                st.markdown("### ✨ Architect Insight")
                st.markdown(output)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a prompt first.")

# Export section
if st.session_state.architect_output:
    st.markdown("---")
    st.subheader("📦 Export Your Insight")

    # Copy to clipboard
    st.code(st.session_state.architect_output, language="markdown")

    # Save as PDF
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "BotMe Architect Insight", ln=True, align="C")
            self.ln(10)
        def chapter_body(self, body):
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 10, body)

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(st.session_state.architect_output)

    pdf_output_path = "/tmp/architect_output.pdf"
    pdf.output(pdf_output_path)

    with open(pdf_output_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="architect_output.pdf">📄 Download as PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)
