from __future__ import annotations

def create_issue(owner: str, repo: str, title: str, body: str) -> dict:
    # Stubbed for demo/CI. Replace with PyGithub or GH REST calls.
    return {
        "status": "created (stub)",
        "owner": owner,
        "repo": repo,
        "title": title,
        "body": body[:200],
        "url": f"https://github.com/{owner}/{repo}/issues/demo"
    }
