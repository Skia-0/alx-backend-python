# fixtures.py

org_payload = {
    "login": "holberton",
    "id": 1,
    "repos_url": "https://api.github.com/orgs/holberton/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}}
]

expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]  # Only repos with license key apache-2.0
