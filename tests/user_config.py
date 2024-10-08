import os
import sys
import unittest
from unittest.mock import call, mock_open, patch
import json

# Append the parent directory to the system path to access app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import user_config
import test_data

class TestUserConfigManager(unittest.TestCase):
    """
    A set of unit tests for the UserConfigManager class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initializes the UserConfigManager class with test data.
        """
        cls.user_config = user_config.UserConfigManager(
            test_data.USER_CONFIG_DEFAULT, test_data.USER_CONFIG_PATH
        )

    def setUp(self):
        """
        Creates the test configuration file.
        """
        with open(
            test_data.USER_CONFIG_PATH, 'w', encoding='utf-8'
        ) as json_file:
            json.dump(
                test_data.USER_CONFIG_DEFAULT, json_file, ensure_ascii=False,
                indent=2
            )

    def tearDown(self):
        """
        Removes the test configuration file.
        """
        if os.path.exists(test_data.USER_CONFIG_PATH):
            os.remove(test_data.USER_CONFIG_PATH)

    def test_exists(self):
        """
        Tests the exists method.
        """
        self.assertTrue(
            self.user_config.exists(),
            "DC Themer configuration file does not exist."
        )

    @patch('builtins.open', new_callable=mock_open)
    def test_create_default(self, mock_open):
        """
        Tests the create_default method.
        """
        self.user_config.create_default()

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([
            call(test_data.USER_CONFIG_PATH, 'w', encoding='utf-8')
        ])

    def test_get_config(self):
        """
        Tests the get_config method.
        """
        self.assertDictEqual(
            self.user_config.get_config(
                test_data.USER_CONFIG_PATH
            ),
            test_data.USER_CONFIG_DEFAULT
        )

    def test_verify(self):
        """
        Tests the verify method.
        """
        with self.assertRaises(RuntimeError):
            self.user_config.verify(
                test_data.CONFIG_CURRENT_VERSION, test_data.CONFIG_READ_VERSION
            )

if __name__ == '__main__':
    """
    Main execution point of the unit tests.
    """
    unittest.main()