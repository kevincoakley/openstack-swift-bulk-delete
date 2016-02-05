#!/usr/bin/env python

import unittest
import requests
from mock import patch
from mock import Mock
from swiftbulkdelete.auth.swauth import Swauth


class SwauthTestCase(unittest.TestCase):

    def setUp(self):
        pass

    @patch('swiftbulkdelete.auth.swauth.requests.get')
    def test_get_auth_token(self, mock_get):

        json_data = {"storage": {"default": "local", "local": "https://fake.com:443/v1/AUTH_fake"}}

        # Create mock response object, with the json function that returns json_data
        mock_response = Mock()
        mock_response.json.return_value = json_data

        # Assign our mock response as the return_value of our patched function
        mock_get.return_value = mock_response

        mock_get.return_value.headers = {"x-auth-token": "1234567890"}
        mock_get.return_value.status_code = requests.codes.ok

        swauth = Swauth("http://fake.com", "fake_project", "fake_user", "fake_pass")
        swauth.get_auth_token()

        self.assertEqual(swauth.auth_token, "1234567890")
        self.assertEqual(swauth.storage_url, "https://fake.com:443/v1/AUTH_fake")
