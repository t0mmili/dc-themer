import os
import sys
import test_data
import unittest
from unittest.mock import patch

# Append the parent directory to the system path to access app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import user_config

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

    def test_exists(self):
        """
        Tests the exists method.
        """
        self.assertTrue(
            self.user_config.exists()
        )

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_create_default(self, mock_open):
        """
        Tests the create_default method.
        """
        self.user_config.create_default()

        # Check that open was called correctly
        mock_open.assert_called_once_with(
            test_data.USER_CONFIG_PATH, 'w', encoding='utf-8'
        )

        # Check that write was called the expected number of times
        self.assertEqual(mock_open().write.call_count, 60)

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