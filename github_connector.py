
import os
from github import Github
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

def get_repo_issues(repo_name, max_issues=5):
    try:
        repo = g.get_repo(repo_name)
        issues = repo.get_issues(state="open")
        return [
            {"title": issue.title, "body": issue.body or "No description."}
            for i, issue in enumerate(issues)
            if i < max_issues
        ]
    except Exception as e:
        return [{"error": str(e)}]

def get_repo_pull_requests(repo_name, max_prs=5):
    try:
        repo = g.get_repo(repo_name)
        prs = repo.get_pulls(state="open", sort="created")
        return [
            {"title": pr.title, "body": pr.body or "No description."}
            for i, pr in enumerate(prs)
            if i < max_prs
        ]
    except Exception as e:
        return [{"error": str(e)}]
