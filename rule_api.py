import os
import time
from typing import List, Dict, Any, Optional

import requests
from dotenv import load_dotenv

# Load environment variable from .env file
load_dotenv()

TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
USERNAME: Optional[str] = os.getenv("GITHUB_USERNAME")

HEADERS: Dict[str, str] = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_all_repos() -> List[Dict[str, Any]]:
    """Fetch all personal repos — handles pagination."""
    repos: List[Dict[str, Any]] = []
    page: int = 1

    while True:
        url: str = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
        response: requests.Response = requests.get(url, headers=HEADERS)
        data: Any = response.json()

        # Break if data is empty or contains an error message
        if not data or (isinstance(data, dict) and "message" in data):
            break

        if isinstance(data, list):
            repos.extend(data)
            # If we received fewer than 100 items, it's the last page
            if len(data) < 100:
                break

        page += 1

    return repos


def apply_protection(repo_name, branch):
    """Block direct pushes by requiring a PR — works on personal repos."""
    url: str = f"https://api.github.com/repos/{USERNAME}/{repo_name}/branches/{branch}/protection"

    payload: Dict[str, Any] = {
        "required_status_checks": None,
        "enforce_admins": False,  # if True, even you can't merge your own PRs without review
        "required_pull_request_reviews": {
            "required_approving_review_count": 0,  # 0 = you can self-approve and merge
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": False
        },
        "restrictions": None  # None = no user whitelist (not supported on personal repos)
    }

    response: requests.Response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        print(f"  ✅ Protected: {repo_name}/{branch}")
    elif response.status_code == 404:
        print(f"  ⚠️  Branch '{branch}' not found in {repo_name} — skipping")
    elif response.status_code == 422:
        print(f"  ⚠️  {repo_name} may be empty or archived — skipping")
    elif response.status_code == 403:
        print(f"  ❌ No permission for {repo_name} — check token scopes")
    else:
        error_msg: str = response.json().get('message', 'Unknown error')
        print(f"  ❌ Failed {repo_name}: {response.status_code} — {error_msg}")


def main():
    """
        Main execution flow: fetches all repositories and applies protection to non-archived ones.
        """
    if not TOKEN or not USERNAME:
        print("❌ Error: GITHUB_TOKEN or GITHUB_USERNAME not found in environment.")
        return

    print(f"Fetching repos for '{USERNAME}'...\n")
    repos: List[Dict[str, Any]] = get_all_repos()
    print(f"Found {len(repos)} repos. Applying protection...\n")

    for repo in repos:
        name: str = repo.get("name", "unknown")
        branch: str = repo.get("default_branch", "main")
        is_archived: bool = repo.get("archived", False)

        if is_archived:
            print(f"→ {name} — skipping (archived)")
            continue

        print(f"→ {name} (default branch: {branch})")
        # apply_protection(name, branch)

        # Slight delay to respect API secondary rate limits
        time.sleep(0.5)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
