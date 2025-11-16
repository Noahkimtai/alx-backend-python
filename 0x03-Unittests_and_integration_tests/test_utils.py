#!/usr/bin/env python3
"""This test file test utility functions"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests access_nested_map function"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """method to test that the method returns what it is supposed to."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, nested_map, path):
        """Tests that nested_map_function raises key error on accessing
        missing keys"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test get_json Function"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """test that get_json function will return expected payload"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test Memoize"""

    def test_memoize(self):
        """Test that memoize function caches the result of a method"""

        class TestClass:
            """Memoize test class"""

            def a_method(self):
                """a_method returns 42"""
                return 42

            @memoize
            def a_property(self):
                """return a_method function"""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock:
            first = test_obj.a_property
            second = test_obj.a_property

        self.assertEqual(first, 42)
        self.assertEqual(second, 42)
        mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
