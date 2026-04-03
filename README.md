# **GitHub Repo Guardian 🛡️**

A specialized automation tool built to streamline repository security and contributor auditing. This project was born out of a desire to automate the tedious process of applying branch protection rules across multiple repositories and ensuring collaborator lists remain clean and authorized.

## **🌟 Features**

* **Automated Branch Protection**: Bulk apply protection rules to prevent direct pushes to the main branch (ideal for organization-wide standards).  
* **Collaborator Auditing**: Automatically checks the contributor list for every repository.  
* **Unauthorized Access Removal**: If collaborators other than the owner are detected, the script can automatically remove them to prevent suspicious edits.  
* **Bulk API Operations**: Uses GitHub PATs and the requests module to handle multiple repositories in one go.

## **🛠️ Tech Stack**

* **Language**: Python 3.14  
* **Environment Management**: [uv](https://github.com/astral-sh/uv)  
* **Dev Tools**:  
  * [Ruff](https://github.com/astral-sh/ruff) (Linter & Formatter)  
  * [Ty](https://www.google.com/search?q=https://github.com/pypa/ty) (Development workflow)  
* **Environment**: Developed inside WSL (Ubuntu).

## **🚀 Getting Started**

### **Prerequisites**

This project uses uv for lightning-fast dependency management. Ensure you have it installed.

### **Installation**

1. Clone the repository:  
   git clone (git@github.com:ajaysharadkumar/github_branch_protection.git)
   cd your-repo-name

2. Sync the environment:  
   uv sync

### **Configuration**

Copy the example environment file and fill in your details:

cp .env.example .env

Edit the .env file with your credentials:

* github\_username: Your GitHub handle.  
* github\_pat: Your Personal Access Token (ensure it has repo and admin scopes).

### **Usage**

To run the main automation script:

uv run base.py

## **🧠 Development Philosophy**

This repository was built **without the use of AI**. Every line of code was crafted based on:

* Deep-diving into official GitHub REST API documentation.  
* Manual web searches for technical problem-solving.  
* Direct experimentation within a WSL Ubuntu environment.

*Note: While branch protection is highly effective for organizations, it serves as a robust auditing layer for personal public repositories to ensure no unexpected collaborators gain write access.*
