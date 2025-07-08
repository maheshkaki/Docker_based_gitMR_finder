# GitHub Metrics

A system to fetch and expose GitHub repository pull request (PR) metrics via an API. The system consists of a Collector Service to periodically fetch PR data and an API Service to expose open PR counts grouped by repository and author.

## Features
- **Collector Service**: Fetches open PRs for configured GitHub repositories at a configurable interval and stores them in a database.
- **API Service**: Provides a REST API endpoint (`/api/prs`) to retrieve open PR counts grouped by repository and author.
- **Containerization**: Orchestrated with Docker Compose for easy setup and deployment.
- **Tech Stack**: Python, FastAPI, PyGithub, SQLAlchemy, SQLite (or PostgreSQL), Docker.

## Requirements
- Python 3.10 or higher
- Docker and Docker Compose
- A GitHub Personal Access Token (PAT) with `repo` scope

## Project Structure

github-metrics/
├── collector/
│   ├── main.py              # Collector Service code
│   ├── requirements.txt     # Dependencies for Collector Service
│   └── Dockerfile           # Docker configuration for Collector Service
├── api/
│   ├── main.py              # API Service code
│   ├── requirements.txt     # Dependencies for API Service
│   └── Dockerfile           # Docker configuration for API Service
├── config.yaml              # Configuration file for repositories and polling interval
├── docker-compose.yml       # Docker Compose orchestration file
└── README.md                # Project documentation


## Setup Instructions
1. Untar the file github-metrics.tar.gz
   cd github-metrics
   
2. Create a .env File: Create a .env file in the project root to store your GitHub Personal Access Token:
echo "GITHUB_TOKEN=ghp_your_personal_access_token" > .env
Replace ghp_your_personal_access_token with your actual GitHub PAT.

3. Configure Repositories: Edit config.yaml to specify the GitHub repositories to monitor and the polling interval (in seconds). Example:
github:
  token: "${GITHUB_TOKEN}"  # Loaded from .env
repositories:
  - "octocat/hello-world"
  - "owner/repo2"
interval: 300  # Fetch every 5 minutes

4. Build and Run Services: Start the Collector and API services using Docker Compose:
docker-compose up --build
This command builds the Docker images and starts the services. The SQLite database (pr_metrics.db) is stored in a shared volume (./data).

5. Access the API:
Open PR counts are available at: http://localhost:8089/api/prs

[
  {"repo": "octocat/hello-world", "author": "user1", "pr_count": 2},
  {"repo": "octocat/hello-world", "author": "user2", "pr_count": 1},
  {"repo": "owner/repo2", "author": "user1", "pr_count": 3}
]

6. Stop the Services: To stop the services, press Ctrl+C in the terminal or run:
docker-compose down


