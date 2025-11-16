#!/usr/bin/env python3
from utils import get_json

class GithubOrgClient:
    """Client to interact with Github organization API"""

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Return org data as JSON"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        return self.org().get("repos_url")

    def public_repos(self):
        """Return list of repo names"""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    def has_license(self, repo, license_key):
        return repo.get("license", {}).get("key") == license_key
