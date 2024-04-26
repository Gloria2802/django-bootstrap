import os
import shutil
import git
import requests

def create_pull_request(repo_url, branch_name, title, description):
    local_repo_path = os.path.join(os.getcwd(), "django-bootstrap")
    if os.path.exists(local_repo_path):
        shutil.rmtree(local_repo_path)
    git.Repo.clone_from(repo_url, local_repo_path)

    repo = git.Repo(local_repo_path)

    repo.git.pull()

def get_pull_requests(repo_owner, repo_name, placeholders):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    response = requests.get(url)
    if response.status_code == 200:
        pull_requests = response.json()
        filtered_pull_requests = []
        for pr in pull_requests:
            if all(placeholder in pr['title'] for placeholder in placeholders):
                filtered_pull_requests.append(pr)
        return filtered_pull_requests
    else:
        print(f"Eroare: {response.status_code}")
        return []

def test_and_create_pull_request(repo_url, branch_name, title, description, test_placeholder):
    if test_placeholder in description:
        print(f"Se detectează {test_placeholder} în descriere. Crearea automată a pull request-ului...")
        create_pull_request(repo_url, branch_name, title, description)
    else:
        print(f"Nu s-a detectat {test_placeholder} în descriere. Nu se va face automat niciun pull request.")

repo_url = "https://github.com/Gloria2802/django-bootstrap"
branch_name = "main"
title = "Actualizare {main} cu placeholder1"
description = "Modificări din ramura {main} pentru a adăuga un nou placeholder."
test_placeholder = "placeholder"

test_and_create_pull_request(repo_url, branch_name, title, description, test_placeholder)

repo_owner = "Gloria2802"
repo_name = "django-bootstrap"
placeholders = ["placeholder"]
pull_requests = get_pull_requests(repo_owner, repo_name, placeholders)

if pull_requests:
    print("Pull request-urile sunt:")
    for pr in pull_requests:
        print(f"- #{pr['number']}: {pr['title']}")
else:
    print("N-avem pull request-uri care să conțină toți placeholder-urile.")