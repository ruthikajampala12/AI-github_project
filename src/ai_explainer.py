import os
from dotenv import load_dotenv
from openai import OpenAI

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please add it to your .env file."
    )


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# ============================================================
# PROJECT EXPLANATION
# ============================================================

def explain_project(
    repository_name,
    description,
    technologies,
    project_tree,
    file_contents
):
    """
    Generate an AI explanation of a GitHub project.
    """

    prompt = f"""
You are an expert software developer and teacher.

Explain the following GitHub project in simple,
student-friendly language.

PROJECT NAME:
{repository_name}

PROJECT DESCRIPTION:
{description}

TECHNOLOGIES:
{technologies}

PROJECT STRUCTURE:
{project_tree}

SOURCE CODE:
{file_contents}

Give the explanation using these sections:

# Project Overview

Explain what the project does.

# Problem It Solves

Explain the problem this project is designed to solve.

# Technologies Used

Explain the technologies and programming languages used.

# Project Structure

Explain the important folders and files.

# How the Project Works

Explain the workflow step by step.

# Important Files

Explain the purpose of the major source files.

# Key Features

List the important features.

# Simple Explanation

Give a short explanation that a college student
could use while presenting the project.

Do not invent features that are not supported
by the repository information.
"""


    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )


    return response.output_text


# ============================================================
# INDIVIDUAL FILE EXPLANATION
# ============================================================

def explain_file(
    file_name,
    file_content
):
    """
    Generate an AI explanation for an individual file.
    """

    prompt = f"""
You are an expert programming teacher.

Explain this source-code file in simple,
student-friendly language.

FILE NAME:
{file_name}

SOURCE CODE:
{file_content}

Explain using these sections:

# Purpose

What is this file used for?

# How It Works

Explain the code step by step.

# Important Functions

Explain the important functions.

# Important Variables

Explain important variables and their purpose.

# Simple Explanation

Give a short explanation suitable for a
college project presentation.

Do not invent functionality that is not present
in the supplied code.
"""


    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )


    return response.output_text

