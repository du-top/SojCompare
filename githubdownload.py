from github import Github
import os
import requests

class GithubDownload:
    
    def __init__(self, token):
        self.token = token

    def download_directory_from_github(self, owner, repo_name, branch, directory, destination):
        """
        Downloads a specific directory from a GitHub repository using PyGithub.
        """
        # Authenticate with GitHub
        g = Github(self.token)
        repo = g.get_repo(f"{owner}/{repo_name}")
    
        # Get the contents of the specified directory
        contents = repo.get_contents(directory, ref=branch)
    
        # Ensure the destination folder exists
        os.makedirs(destination, exist_ok=True)
    
        for content in contents:
            if content.type == "file":
                # Download the file
                file_url = content.download_url
                file_path = os.path.join(destination, content.name)
            
                print(f"Downloading {content.path} to {file_path}...")
                response = requests.get(file_url)
                with open(file_path, "wb") as file:
                    file.write(response.content)
            elif content.type == "dir":
                # Recursively download subdirectory
                sub_dir = os.path.join(destination, content.name)
                self.download_directory_from_github(owner, repo_name, branch, content.path, sub_dir)

    




