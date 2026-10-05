import os
import streamlit as st

# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from src.github_api import (
    parse_github_url,
    get_repository_info,
    get_repository_files,
    get_file_content
)

from src.file_analyzer import (
    analyze_file_list,
    build_project_tree,
    is_supported_file
)

from src.ai_explainer import (
    explain_project,
    explain_file
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI GitHub Project Explainer",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# LOAD CSS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

css_path = os.path.join(
    BASE_DIR,
    "assets",
    "style.css"
)

if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI GitHub Project Explainer")

st.write(
    "Understand GitHub projects using Artificial Intelligence. "
    "Enter a GitHub repository URL and get an explanation "
    "of the project structure, technologies, files and code."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Project Settings")

    st.write(
        "Enter a public GitHub repository URL "
        "to analyze the project."
    )

    st.divider()

    st.info(
        """
        Example:

        https://github.com/username/repository
        """
    )


# ============================================================
# GITHUB URL INPUT
# ============================================================

github_url = st.text_input(
    "🔗 Enter GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🚀 Analyze GitHub Project",
    type="primary",
    use_container_width=True
)


# ============================================================
# PROJECT ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # Check URL
    # --------------------------------------------------------

    if not github_url.strip():

        st.warning(
            "⚠️ Please enter a GitHub repository URL."
        )

        st.stop()


    try:

        # ====================================================
        # STEP 1: PARSE GITHUB URL
        # ====================================================

        with st.spinner("🔗 Connecting to GitHub..."):

            owner, repo = parse_github_url(
                github_url
            )


        # ====================================================
        # STEP 2: GET REPOSITORY INFORMATION
        # ====================================================

        with st.spinner(
            "📡 Getting repository information..."
        ):

            repo_info = get_repository_info(
                owner,
                repo
            )


        # ====================================================
        # STEP 3: GET REPOSITORY FILES
        # ====================================================

        with st.spinner(
            "📂 Reading repository files..."
        ):

            files = get_repository_files(
                owner,
                repo
            )


        st.success(
            f"✅ Successfully loaded **{owner}/{repo}**"
        )


        # ====================================================
        # REPOSITORY INFORMATION
        # ====================================================

        st.header("📊 Repository Information")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "⭐ Stars",
                repo_info.get(
                    "stargazers_count",
                    0
                )
            )


        with col2:

            st.metric(
                "🍴 Forks",
                repo_info.get(
                    "forks_count",
                    0
                )
            )


        with col3:

            st.metric(
                "🐛 Open Issues",
                repo_info.get(
                    "open_issues_count",
                    0
                )
            )


        with col4:

            st.metric(
                "📁 Files",
                len(files)
            )


        # ====================================================
        # PROJECT DESCRIPTION
        # ====================================================

        st.subheader("📝 Project Description")


        description = repo_info.get(
            "description"
        )


        if description:

            st.write(description)

        else:

            st.write(
                "No project description is available."
            )


        # ====================================================
        # FILE ANALYSIS
        # ====================================================

        analysis = analyze_file_list(
            files
        )


        # ====================================================
        # TECHNOLOGIES
        # ====================================================

        st.subheader(
            "🛠️ Technologies Detected"
        )


        technologies = list(
            analysis.get(
                "file_types",
                {}
            ).keys()
        )


        if technologies:

            technology_columns = st.columns(
                min(
                    len(technologies),
                    4
                )
            )


            for index, technology in enumerate(
                technologies
            ):

                with technology_columns[
                    index % len(technology_columns)
                ]:

                    st.info(
                        technology
                    )

        else:

            st.write(
                "No recognizable technologies found."
            )


        # ====================================================
        # PROJECT STRUCTURE
        # ====================================================

        st.subheader(
            "📂 Project Structure"
        )


        project_tree = build_project_tree(
            files
        )


        with st.expander(
            "View Project Files",
            expanded=True
        ):

            if project_tree:

                st.code(
                    project_tree,
                    language="text"
                )

            else:

                st.write(
                    "No project structure available."
                )


        # ====================================================
        # FIND SUPPORTED FILES
        # ====================================================

        supported_files = []


        for file in files:

            if file.get("type") != "blob":
                continue


            path = file.get(
                "path",
                ""
            )


            if is_supported_file(path):

                supported_files.append(
                    file
                )


        # ====================================================
        # READ PROJECT SOURCE FILES
        # ====================================================

        file_contents = ""


        # Limit number of files sent to AI
        selected_files = supported_files[:15]


        with st.spinner(
            "📖 Reading important project files..."
        ):

            for file in selected_files:

                file_path = file.get(
                    "path",
                    ""
                )


                try:

                    content = get_file_content(
                        owner,
                        repo,
                        file_path
                    )

                except Exception:

                    content = ""


                if content:

                    # Limit individual file size
                    content = content[:8000]


                    file_contents += (
                        "\n\n"
                        "==================================================\n"
                        f"FILE: {file_path}\n"
                        "==================================================\n"
                        f"{content}"
                    )


        # ====================================================
        # AI PROJECT EXPLANATION
        # ====================================================

        st.header(
            "🤖 AI Project Explanation"
        )


        try:

            with st.spinner(
                "🧠 AI is analyzing the project..."
            ):

                explanation = explain_project(
                    repository_name=repo,
                    description=(
                        description
                        if description
                        else "No description available."
                    ),
                    technologies=", ".join(
                        technologies
                    ),
                    project_tree=project_tree,
                    file_contents=file_contents
                )


            if explanation:

                st.markdown(
                    explanation
                )

            else:

                st.warning(
                    "The AI returned an empty explanation."
                )


        except Exception as ai_error:

            st.error(
                "❌ AI explanation could not be generated."
            )

            st.code(
                str(ai_error)
            )


        # ====================================================
        # INDIVIDUAL FILE EXPLAINER
        # ====================================================

        st.divider()


        st.header(
            "📄 Individual File Explainer"
        )


        if supported_files:

            file_paths = [
                file.get("path", "")
                for file in supported_files
            ]


            selected_file = st.selectbox(
                "Choose a source file",
                file_paths
            )


            explain_file_button = st.button(
                "🔍 Explain Selected File"
            )


            if explain_file_button:

                with st.spinner(
                    "📖 Reading selected file..."
                ):

                    try:

                        content = get_file_content(
                            owner,
                            repo,
                            selected_file
                        )

                    except Exception as file_read_error:

                        st.error(
                            "Could not read the selected file."
                        )

                        st.code(
                            str(file_read_error)
                        )

                        content = None


                if content:

                    st.subheader(
                        f"📄 {selected_file}"
                    )


                    with st.expander(
                        "View Source Code",
                        expanded=False
                    ):

                        st.code(
                            content,
                            language="text"
                        )


                    try:

                        with st.spinner(
                            "🧠 AI is explaining the file..."
                        ):

                            file_explanation = explain_file(
                                selected_file,
                                content[:12000]
                            )


                        st.subheader(
                            "🤖 File Explanation"
                        )


                        if file_explanation:

                            st.markdown(
                                file_explanation
                            )

                        else:

                            st.warning(
                                "The AI returned an empty explanation."
                            )


                    except Exception as file_ai_error:

                        st.error(
                            "❌ Could not generate the file explanation."
                        )

                        st.code(
                            str(file_ai_error)
                        )


                elif content == "":

                    st.warning(
                        "The selected file is empty."
                    )


        else:

            st.info(
                "No supported source-code files were found."
            )


    # ========================================================
    # GENERAL ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "❌ Something went wrong while analyzing the repository."
        )

        st.code(
            str(error)
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI GitHub Project Explainer • "
    "Python + Streamlit + GitHub API + AI"
)