#!/usr/bin/env python

import json
import unittest
import requests
from mock import patch
from mock import Mock
from swiftbulkdelete.swift import Swift


class SwiftTestCase(unittest.TestCase):

    def setUp(self):
        self.objects_json_file = "tests/swift/objects.json"

    @patch('swiftbulkdelete.swift.requests.get')
    def test_list_objects(self, mock_get):

        with open(self.objects_json_file) as j:
            object_json = json.load(j)

        # Create mock response object, with the json function that returns object_json
        mock_response = Mock()
        mock_response.json.return_value = object_json

        # Assign our mock response as the return_value of our patched function
        mock_get.return_value = mock_response

        mock_get.return_value.status_code = requests.codes.ok

        swift = Swift("1234567890", "http://fake.com", "container", 100)

        self.assertEqual(swift.list_objects(100), object_json)

    @patch('swiftbulkdelete.swift.requests.get')
    def test_get_object_offset_marker(self, mock_get):

        with open(self.objects_json_file) as j:
            object_json = json.load(j)

        # Create mock response object, with the json function that returns object_json
        mock_response = Mock()
        mock_response.json.return_value = object_json

        # Assign our mock response as the return_value of our patched function
        mock_get.return_value = mock_response

        mock_get.return_value.status_code = requests.codes.ok

        swift = Swift("1234567890", "http://fake.com", "container", 100)

        self.assertEqual(swift.get_object_offset_marker(100), "0055.txt")

    @patch('swiftbulkdelete.swift.requests.get')
    def test_get_objects(self, mock_get):
        with open(self.objects_json_file) as j:
            object_json = json.load(j)

        # Create mock response object, with the json function that returns object_json
        mock_response = Mock()
        mock_response.json.return_value = object_json

        # Assign our mock response as the return_value of our patched function
        mock_get.return_value = mock_response

        mock_get.return_value.status_code = requests.codes.ok

        swift = Swift("1234567890", "http://fake.com", "container", 100)

        swift.get_objects()

        object_list = ""
        for count in range(1, 56):
            if count is not 15 and count is not 30 and count is not 45:
                object_list += ("container/00%02d.txt\n" % count)

        self.assertEqual(swift.object_list, object_list)
