
import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from github_connector import get_repo_issues, get_repo_pull_requests

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App title
st.title("🤖 BotMe: GitHub Summarizer + GPT Assistant")

# State
if "summary_history" not in st.session_state:
    st.session_state.summary_history = ""

# Input
repo_name = st.text_input("Enter GitHub repo (e.g. openai/openai-python)")

# Buttons
col1, col2 = st.columns(2)
summarize_issues = col1.button("Summarize Issues")
summarize_prs = col2.button("Summarize Pull Requests")

def summarize_with_gpt(items, mode="issues"):
    content_type = "issues" if mode == "issues" else "pull requests"
    text = ""
    for i, item in enumerate(items):
        if "error" not in item:
            title = item["title"]
            body = item["body"][:200] if item["body"] else "No description"
            text += f"{i+1}. {title}: {body}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that summarizes GitHub {content_type}."
            },
            {
                "role": "user",
                "content": f"Summarize the following GitHub {content_type}:\n{text}"
            }
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

def ask_gpt_followup(question, summary_context):
    messages = [
        {
            "role": "system",
            "content": "You are a GitHub-savvy assistant helping a user understand and interact with project issues and pull requests."
        },
        {
            "role": "user",
            "content": f"Based on the following context:\n{summary_context}\n\nQuestion: {question}"
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5
    )
    return response.choices[0].message.content

# Run summaries
if summarize_issues and repo_name:
    with st.spinner("Summarizing issues with GPT..."):
        issues = get_repo_issues(repo_name)
        if issues and "error" in issues[0]:
            st.error(f"❌ {issues[0]['error']}")
        else:
            summary = summarize_with_gpt(issues, mode="issues")
            st.session_state.summary_history = summary
            st.subheader("📝 GPT Summary of Issues")
            st.text(summary)

if summarize_prs and repo_name:
    with st.spinner("Summarizing pull requests with GPT..."):
        prs = get_repo_pull_requests(repo_name)
        if prs and "error" in prs[0]:
            st.error(f"❌ {prs[0]['error']}")
        else:
            summary = summarize_with_gpt(prs, mode="prs")
            st.session_state.summary_history = summary
            st.subheader("📝 GPT Summary of Pull Requests")
            st.text(summary)

# Follow-up GPT question input
if st.session_state.summary_history:
    st.markdown("### 💬 Ask a follow-up question")
    followup_q = st.text_input("Ask something about the summary above")
    if st.button("Ask GPT"):
        with st.spinner("Thinking..."):
            answer = ask_gpt_followup(followup_q, st.session_state.summary_history)
            st.markdown("**🤖 GPT's Response:**")
            st.text(answer)
