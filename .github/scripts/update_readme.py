import os
from github import Github
from datetime import datetime

# Initialize GitHub client
g = Github(os.environ['GITHUB_TOKEN'])

# Get the organization
org = g.get_organization(os.environ['GITHUB_REPOSITORY'].split('/')[0])

# Prepare the data table
data_table = ""

# Iterate through all public repositories
for repo in org.get_repos(type='public'):
    name = repo.name
    if name == '.github':
        continue  # Skip the .github repository itself

    # Get latest release
    latest_release = "N/A"
    releases = repo.get_releases()
    if releases.totalCount > 0:
        latest_release = releases[0].tag_name

    # Get open PRs count
    open_prs = repo.get_pulls(state='open').totalCount

    # Get open issues count
    open_issues = repo.get_issues(state='open').totalCount

    # Add row to data table
    data_table += f"| [{name}]({repo.html_url}) | {latest_release} | {open_prs} | {open_issues} |\n"

# Read the README template
with open('README.md', 'r') as file:
    readme = file.read()

# Update the README with new data
readme = readme.replace("<!-- DATA_TABLE -->", data_table)
readme = readme.replace("<!-- LAST_UPDATED -->", datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))

# Write the updated README
with open('README.md', 'w') as file:
    file.write(readme)

print("README.md has been updated with the latest repository status.")
