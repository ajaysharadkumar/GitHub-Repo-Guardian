import os
import time
from typing import List, Optional, Dict, Any

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


def get_collaborators(repo_name) -> List:
    url: str = f"https://api.github.com/repos/{USERNAME}/{repo_name}/collaborators"
    response: requests.Response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []


def remove_collaborator(repo_name, collaborator_login):
    url: str = f"https://api.github.com/repos/{USERNAME}/{repo_name}/collaborators/{collaborator_login}"
    response: requests.Response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"     Removed: {collaborator_login}")
    else:
        print(f"     Failed to remove {collaborator_login}: {response.status_code}")


def main(repos: List[Dict[str, Any]]):
    print(f"Scanning collaborators...\n")

    for repo in repos:
        name = repo["name"]
        print(f"→ {name}")

        collaborators = get_collaborators(name)

        if not collaborators:
            print(f"   No collaborators found")
            continue

        others = [c for c in collaborators if c["login"].lower() != USERNAME.lower()]

        if not others:
            print(f"    Only you — nothing to do")
        else:
            for collab in others:
                print(f"     Found: {collab['login']} — removing...")
                # remove_collaborator(name, collab["login"])

        time.sleep(0.5)

    print("\n Done!")


if __name__ == "__main__":
    repos: List[Dict[str, Any]] = []
    main(repos=repos)
