import os
from typing import Optional, Dict, List, Any
import rule_api
import remove_collaborators

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

def main():
    if not TOKEN or not USERNAME:
        print("Error: GITHUB_TOKEN or GITHUB_USERNAME not found in environment.")
        return

    print(f"Fetching repos for '{USERNAME}'...\n")
    repos: List[Dict[str, Any]] = get_all_repos()
    print(f"Found {len(repos)} ...\n")
    option = input("Press 1 to run rule_api \nPress 2 to run remove_collaborators \n")
    while True:
        match option:
            case "1":
                print("Running rule_api\n")
                rule_api.main(repos)
                break
            case "2":
                print("Running remove_collaborators\n")
                remove_collaborators.main(repos)
                break
            case _:
                print("Unknown option")
                break


if __name__ == '__main__':
    main()
