#!/usr/bin/env python3
"""Test suite for GithubOrgClient functionality."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests covering isolated behaviors of GithubOrgClient."""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Ensure that accessing the 'org' property triggers the appropriate
        API call and yields the JSON response returned by get_json().
        """
        mock_response = {"org": org_name}
        mock_get_json.return_value = mock_response

        client = GithubOrgClient(org_name)
        output = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(output, mock_response)

    def test_public_repos_url(self):
        """
        Verify that the private _public_repos_url attribute correctly extracts
        the repo URL from the organization metadata.
        """
        fake_org_metadata = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
            return_value=fake_org_metadata,
        ) as mock_org:
            client = GithubOrgClient("google")
            url = client._public_repos_url

        self.assertEqual(url, fake_org_metadata["repos_url"])
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Confirm public_repos() retrieves repo data and returns a list of names.
        """
        sample_repos = [
            {"name": "alpha"},
            {"name": "beta"},
            {"name": "gamma"},
        ]
        mock_get_json.return_value = sample_repos

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos",
        ) as mock_repo_url:
            client = GithubOrgClient("google")
            names = client.public_repos()

        self.assertEqual(names, ["alpha", "beta", "gamma"])
        mock_repo_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos",
        )

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """
        Validate the logic determining whether a repository advertises
        a specified license key.
        """
        outcome = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(outcome, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD,
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration-style tests evaluating multiple components together."""

    @classmethod
    def setUpClass(cls):
        """
        Apply a mock to requests.get so that network interactions return
        predefined payloads depending on the URL accessed.
        """
        cls.get_patcher = patch("requests.get")
        mocked_get = cls.get_patcher.start()

        def fake_request(url):
            """Return organization or repo payload based on endpoint."""

            class DummyResponse:
                def __init__(self, data):
                    self._data = data

                def json(self):
                    return self._data

            if url == cls.org_payload["repos_url"]:
                return DummyResponse(cls.repos_payload)
            return DummyResponse(cls.org_payload)

        mocked_get.side_effect = fake_request

    @classmethod
    def tearDownClass(cls):
        """Disable the requests.get patch applied during setup."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration: verify public_repos() with no license filtering returns
        the full set of repository names.
        """
        client = GithubOrgClient("google")
        results = client.public_repos()
        self.assertEqual(results, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Integration: confirm that public_repos() respects an explicit license
        filter and yields only matching repositories.
        """
        client = GithubOrgClient("google")
        results = client.public_repos(license="apache-2.0")
        self.assertEqual(results, self.apache2_repos)
