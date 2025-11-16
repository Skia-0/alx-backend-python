#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

# -----------------------------
# Unit tests for GithubOrgClient
# -----------------------------
class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns correct URL from payload"""
        client = GithubOrgClient("test_org")
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://fake.url/repo"}
            self.assertEqual(client._public_repos_url, "http://fake.url/repo")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected list of repos"""
        client = GithubOrgClient("test_org")
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_payload
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake.url/repos"
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://fake.url/repos")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns expected boolean"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.has_license(repo, license_key), expected)


# -----------------------------
# Integration tests with fixtures
# -----------------------------
@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get using fixtures"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # map url to fixture payload
        def side_effect(url, *args, **kwargs):
            if url == cls.org_payload["url"]:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            else:
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        """Test public_repos returns expected repos using fixtures"""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)
