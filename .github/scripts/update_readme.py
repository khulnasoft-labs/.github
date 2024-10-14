import os
from github import Github
from datetime import datetime

# Initialize GitHub client
g = Github(os.environ['GITHUB_TOKEN'])

# Get the organization
org = g.get_organization(os.environ['GITHUB_REPOSITORY'].split('/')[0])

# Prepare the data table
data_table = "| Name | Build status | Analysis status | Latest release | Issues |\n"
data_table += "|:-----|:-------------|:----------------|:---------------|:-------|\n"

# Iterate through all public repositories
for repo in org.get_repos(type='public'):
    name = repo.name
    if name == '.github':
        continue  # Skip the .github repository itself

    # Get latest release
    latest_release = "N/A"
    release_date = "N/A"
    releases = repo.get_releases()
    if releases.totalCount > 0:
        latest_release = releases[0].tag_name
        release_date = releases[0].created_at.strftime("%Y-%m-%d")

    # Create badges
    repo_url = repo.html_url
    build_badge = f"[![Build Status](https://github.com/{repo.full_name}/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/{repo.full_name}/actions)"
    analysis_badge = f"[![Scan Status](https://scan.coverity.com/projects/{repo.id}/badge.svg?flat=1)](https://scan.coverity.com/projects/{repo.id})"
    release_badge = f"[![Latest Release](https://img.shields.io/github/release/{repo.full_name}.svg?style=flat-square&label=)](https://github.com/{repo.full_name}/releases)"
    release_date_badge = f"[![Release date](https://img.shields.io/github/release-date/{repo.full_name}.svg?style=flat-square&color=informational&label=)](https://github.com/{repo.full_name}/releases)"
    pulls_badge = f"[![Pulls](https://img.shields.io/github/issues-pr-raw/{repo.full_name}.svg?style=flat-square&color=informational&label=pulls)](https://github.com/{repo.full_name}/pulls)"
    issues_badge = f"[![Issues](https://img.shields.io/github/issues-raw/{repo.full_name}.svg?style=flat-square&color=informational&label=issues)](https://github.com/{repo.full_name}/issues)"

    # Add row to data table
    data_table += f"[{name}]({repo_url}) | {build_badge} | {analysis_badge} | {release_badge}{release_date_badge} | {pulls_badge} {issues_badge}\n"

# Read the README template
with open('README.md', 'r') as file:
    readme = file.read()

# Update the README with new data
readme = readme.replace("<!-- DATA_TABLE -->", data_table)
readme = readme.replace("<!-- LAST_UPDATED -->", datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))

# Write the updated README
with open('README.md', 'w') as file:
    file.write(readme)

print("README.md has been updated with the latest repository status and badges.")
