#!/usr/bin/env python3
"""Unittests for the client module."""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class."""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_class = GithubOrgClient(org)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that the result of _public_repos_url is the expected one."""
        mock_org.return_value = {
            'repos_url': 'https://api.github.com/orgs/google/repos'}
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class._public_repos_url,
                         "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that the result of _public_repos is the expected one."""
        mock_get_json.return_value = [
            {'name': 'repo1'},
            {'name': 'repo2'}
        ]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/google/repos"
            test_class = GithubOrgClient("google")
            repos = test_class.public_repos()
            self.assertEqual(repos, ['repo1', 'repo2'])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that the result of has_license is the expected one."""
        test_class = GithubOrgClient("google")
        result = test_class.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up for all tests in the class."""
        cls.get_patcher = patch(
            'requests.get',
            side_effect=cls.get_side_effect)
        cls.get_patcher.start()

    @staticmethod
    def get_side_effect(url):
        """Side effect for requests.get."""
        if url == "https://api.github.com/orgs/google":
            return TestIntegrationGithubOrgClient.org_payload
        elif url == "https://api.github.com/orgs/google/repos":
            return TestIntegrationGithubOrgClient.repos_payload
        else:
            return None

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that the result of _public_repos is the expected one."""
        mock_get_json.return_value = [
            {'name': 'repo1'},
            {'name': 'repo2'}
        ]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/google/repos"
            test_class = GithubOrgClient("google")
            repos = test_class.public_repos()
            self.assertEqual(repos, ['repo1', 'repo2'])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")
            mock_public_repos_url.assert_called_once()

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test that the result of _public_repos
        with license is the expected one.
        """
        mock_get_json.return_value = [
            {'name': 'repo1', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo2', 'license': {'key': 'mit'}}
        ]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/google/repos"
            test_class = GithubOrgClient("google")
            repos = test_class.public_repos(license="apache-2.0")
            self.assertEqual(repos, ['repo1'])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")
            mock_public_repos_url.assert_called_once()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests in the class."""
        cls.get_patcher.stop()
