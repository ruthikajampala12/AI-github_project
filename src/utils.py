import re


def clean_text(text, max_length=5000):
    """
    Clean and limit text length.
    """

    if not text:
        return ""

    text = text.strip()

    return text[:max_length]


def extract_repository_name(url):
    """
    Extract repository name from GitHub URL.
    """

    url = url.strip().rstrip("/")

    parts = url.split("/")

    if len(parts) >= 2:
        return parts[-1].replace(".git", "")

    return "GitHub Repository"


def format_file_size(size):
    """
    Convert bytes into readable format.
    """

    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.1f} MB"


def is_safe_file(path):
    """
    Avoid processing unnecessary or potentially huge files.
    """

    blocked = [
        ".git/",
        "node_modules/",
        "__pycache__/",
        ".venv/",
        "venv/",
        "dist/",
        "build/"
    ]

    return not any(item in path for item in blocked)