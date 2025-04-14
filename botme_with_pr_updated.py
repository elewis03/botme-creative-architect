
from openai import OpenAI
import os
from dotenv import load_dotenv
from github_connector import get_repo_issues, get_repo_pull_requests

# Load API keys
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_issues_with_gpt(issues):
    issue_text = ""
    for i, issue in enumerate(issues):
        if "error" not in issue:
            title = issue["title"]
            body = issue["body"][:200] if issue["body"] else "No description"
            issue_text += f"{i+1}. {title}: {body}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant summarizing GitHub issues."
            },
            {
                "role": "user",
                "content": "Summarize the following GitHub issues:\n" + issue_text
            }
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

def summarize_prs_with_gpt(prs):
    pr_text = ""
    for i, pr in enumerate(prs):
        if "error" not in pr:
            title = pr["title"]
            body = pr["body"][:200] if pr["body"] else "No description"
            pr_text += f"{i+1}. {title}: {body}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant summarizing GitHub pull requests."
            },
            {
                "role": "user",
                "content": "Summarize the following GitHub pull requests:\n" + pr_text
            }
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

def run_bot():
    repo_name = input("Enter the GitHub repo (e.g. openai/openai-python): ")
    choice = input("Type '1' to summarize issues, '2' to summarize pull requests: ").strip()

    if choice == '1':
        issues = get_repo_issues(repo_name)
        if issues and "error" in issues[0]:
            print(f"❌ Error: {issues[0]['error']}")
            return
        summary = summarize_issues_with_gpt(issues)
        print("\n🤖 GPT Summary of GitHub Issues:\n")
        print(summary)
    elif choice == '2':
        prs = get_repo_pull_requests(repo_name)
        if prs and "error" in prs[0]:
            print(f"❌ Error: {prs[0]['error']}")
            return
        summary = summarize_prs_with_gpt(prs)
        print("\n🤖 GPT Summary of GitHub Pull Requests:\n")
        print(summary)
    else:
        print("Invalid choice. Please type '1' or '2'.")

if __name__ == "__main__":
    run_bot()
