import os
import time
import yaml
import schedule
from github import Github
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Load configuration
with open("/app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPOS = config["repositories"]
INTERVAL = config["interval"]

# Database setup
Base = declarative_base()
engine = create_engine("sqlite:////app/db/pr_metrics.db")
Session = sessionmaker(bind=engine)

class PRMetric(Base):
    __tablename__ = "pr_metrics"
    id = Column(Integer, primary_key=True)
    repo = Column(String, nullable=False)
    author = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    state = Column(String, nullable=False)

Base.metadata.create_all(engine)

# GitHub client
g = Github(GITHUB_TOKEN)

def fetch_prs():
    session = Session()
    for repo_name in REPOS:
        try:
            repo = g.get_repo(repo_name)
            prs = repo.get_pulls(state="open")
            for pr in prs:
                # Check if PR already exists
                existing = session.query(PRMetric).filter_by(repo=repo_name, pr_number=pr.number).first()
                if not existing:
                    metric = PRMetric(
                        repo=repo_name,
                        author=pr.user.login,
                        pr_number=pr.number,
                        created_at=pr.created_at,
                        state="open"
                    )
                    session.add(metric)
            session.commit()
            print(f"Fetched PRs for {repo_name}")
        except Exception as e:
            print(f"Error fetching PRs for {repo_name}: {e}")
    session.close()

# Schedule task
schedule.every(INTERVAL).seconds.do(fetch_prs)

if __name__ == "__main__":
    print("Starting Collector Service...")
    fetch_prs()  # First Run before the scheduled run
    while True:
        schedule.run_pending()
        time.sleep(1)
