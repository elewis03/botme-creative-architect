
import openai
import os
from dotenv import load_dotenv
from github_connector import get_repo_issues

# Load API keys from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_issues_with_gpt(issues):
    issue_text = ""
    for i, issue in enumerate(issues):
        if "error" not in issue:
            title = issue["title"]
            body = issue["body"][:200] if issue["body"] else "No description"
            issue_text += f"{i+1}. {title}: {body}\n"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful chatbot assistant. You receive GitHub issues and summarize them."
        },
        {
            "role": "user",
            "content": "Summarize the following GitHub issues:\n" + issue_text
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5
    )
    return response.choices[0].message["content"]

def run_bot():
    repo_name = input("Enter the GitHub repo (e.g. openai/openai-python): ")
    issues = get_repo_issues(repo_name)
    if issues and "error" in issues[0]:
        print(f"❌ Error: {issues[0]['error']}")
        return

    summary = summarize_issues_with_gpt(issues)
    print("\n🤖 GPT Summary of GitHub Issues:\n")
    print(summary)

if __name__ == "__main__":
    run_bot()
