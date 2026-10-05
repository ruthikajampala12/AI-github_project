import os


# File extensions that are useful for code analysis
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".html",
    ".css",
    ".sql",
    ".json",
    ".xml",
    ".md",
    ".txt"
}


def get_extension(filename):
    return os.path.splitext(filename)[1].lower()


def is_supported_file(filename):
    extension = get_extension(filename)

    return extension in SUPPORTED_EXTENSIONS


def categorize_file(filename):
    """
    Categorize files based on their extension.
    """

    extension = get_extension(filename)

    categories = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "React",
        ".ts": "TypeScript",
        ".tsx": "React TypeScript",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".h": "C/C++ Header",
        ".html": "HTML",
        ".css": "CSS",
        ".sql": "SQL",
        ".json": "JSON",
        ".xml": "XML",
        ".md": "Documentation",
        ".txt": "Text"
    }

    return categories.get(extension, "Other")


def analyze_file_list(files):
    """
    Analyze repository file list.
    """

    result = {
        "total_files": 0,
        "supported_files": 0,
        "file_types": {},
        "files": []
    }

    for file in files:

        if file.get("type") != "blob":
            continue

        path = file.get("path", "")

        result["total_files"] += 1

        category = categorize_file(path)

        if category not in result["file_types"]:
            result["file_types"][category] = 0

        result["file_types"][category] += 1

        if is_supported_file(path):
            result["supported_files"] += 1

        result["files"].append({
            "path": path,
            "category": category,
            "size": file.get("size", 0)
        })

    return result


def build_project_tree(files):
    """
    Create a simple text representation of the project.
    """

    lines = []

    for file in files:

        if file.get("type") != "blob":
            continue

        path = file.get("path", "")

        depth = path.count("/")

        name = path.split("/")[-1]

        indentation = "    " * depth

        lines.append(
            f"{indentation}├── {name}"
        )

    return "\n".join(lines)