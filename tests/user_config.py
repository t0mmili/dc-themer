import os
import sys
import unittest
from unittest.mock import mock_open, patch
import jsonschema

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
        cls.user_config_default = test_data.USER_CONFIG_DEFAULT
        cls.user_config_path = test_data.USER_CONFIG_PATH

        cls.user_config = user_config.UserConfigManager(
            cls.user_config_default, cls.user_config_path
        )

        cls.config_ver_current = test_data.CONFIG_VERSION_CURRENT
        cls.config_ver_read_fail = test_data.CONFIG_VERSION_READ_FAIL
        cls.config_ver_read_success = test_data.CONFIG_VERSION_READ_SUCCESS
        cls.user_config_schema = test_data.USER_CONFIG_SCHEMA

    @patch('os.path.isfile')
    def test_exists(self, mock_isfile):
        """
        Tests the exists method.
        """
        mock_isfile.return_value = True

        self.assertTrue(self.user_config.exists())

    @patch('builtins.open', new_callable=mock_open)
    def test_create_default(self, mock_open):
        """
        Tests the create_default method.
        """
        self.user_config.create_default()

        # Check that open was called with specific arguments
        mock_open.assert_called_with(
            self.user_config_path, 'w', encoding='utf-8'
        )

    @patch('builtins.open', new_callable=mock_open)
    def test_get_config(self, mock_open):
        """
        Tests the get_config method.
        """
        mock_open.return_value.read.return_value = str(
            self.user_config_default
        )

        user_config = self.user_config.get_config(self.user_config_path)

        # Validate user config against json schema
        jsonschema.validate(user_config, self.user_config_schema)

    def test_verify_success(self):
        """
        Tests the verify method for success.
        """
        self.user_config.verify(
            self.config_ver_current, self.config_ver_read_success
        )

    def test_verify_version_mismatch(self):
        """
        Tests the verify method for failure.
        Case details: Config's read and current version mismatch.
        """
        with self.assertRaises(RuntimeError):
            self.user_config.verify(
                self.config_ver_current, self.config_ver_read_fail
            )

if __name__ == '__main__':
    """
    Main execution point of the unit tests.
    """
    unittest.main()