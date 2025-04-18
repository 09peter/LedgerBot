import os
from github import Github

class GitHubCommitter:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        repo_name = os.getenv("GITHUB_REPO")
        if not token or not repo_name:
            raise RuntimeError("GITHUB_TOKEN and GITHUB_REPO must be set")
        self.gh = Github(token)
        self.repo = self.gh.get_repo(repo_name)

    def commit_file(self, local_path: str, repo_path: str, message: str):
        # Read file contents
        with open(local_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if file exists in repo
        try:
            contents = self.repo.get_contents(repo_path)
            # Update existing file
            self.repo.update_file(
                path=repo_path,
                message=message,
                content=content,
                sha=contents.sha
            )
        except Exception:
            # Create new file
            self.repo.create_file(
                path=repo_path,
                message=message,
                content=content
            )
