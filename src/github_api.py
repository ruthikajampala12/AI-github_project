import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_URL = "https://api.github.com"


def get_headers():
    headers = {
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


def parse_github_url(url):
    """
    Extract owner and repository name from a GitHub URL.
    """

    url = url.strip().rstrip("/")

    if "github.com/" not in url:
        raise ValueError("Please enter a valid GitHub repository URL.")

    parts = url.split("github.com/")[1].split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def get_repository_info(owner, repo):
    """
    Get basic repository information.
    """

    url = f"{BASE_URL}/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=20
    )

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code}"
        )

    return response.json()


def get_repository_files(owner, repo):
    """
    Get the file tree of a repository.
    """

    repo_info = get_repository_info(owner, repo)

    default_branch = repo_info["default_branch"]

    url = (
        f"{BASE_URL}/repos/{owner}/{repo}/git/trees/"
        f"{default_branch}?recursive=1"
    )

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"Could not retrieve repository files: "
            f"{response.status_code}"
        )

    data = response.json()

    return data.get("tree", [])


def get_file_content(owner, repo, file_path):
    """
    Download the content of a single file.
    """

    url = (
        f"{BASE_URL}/repos/{owner}/{repo}/contents/"
        f"{file_path}"
    )

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=20
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("type") != "file":
        return None

    download_url = data.get("download_url")

    if not download_url:
        return None

    file_response = requests.get(
        download_url,
        headers=get_headers(),
        timeout=20
    )

    if file_response.status_code != 200:
        return None

    return file_response.text