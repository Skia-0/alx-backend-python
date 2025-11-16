#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test the public_repos method of GithubOrgClient."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit test GithubOrgClient.public_repos with mocked dependencies."""
        # Mock payload returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        org_client = GithubOrgClient("test_org")

        # Patch _public_repos_url to return a dummy URL
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://api.github.com/orgs/test_org/repos"

            # Call public_repos and check output
            repos = org_client.public_repos()
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            # Ensure mocks were called exactly once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://api.github.com/orgs/test_org/repos")
