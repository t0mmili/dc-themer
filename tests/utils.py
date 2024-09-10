import os
import shutil
import sys
import unittest
from unittest.mock import call, mock_open, patch
import configobj
import configobj.validate as configobjVal
import json
import jsonschema

# Append the parent directory to the system path to access app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import utils
import test_data

class TestScheme(unittest.TestCase):
    """
    A set of unit tests for the AppUtils, DCFileManager and SchemeFileManager
    classes.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initializes the classes with test data.
        """
        cls.app_utils = utils.AppUtils()
        cls.dc_file_manager = utils.DCFileManager()
        cls.scheme_file_manager = utils.SchemeFileManager()

    def setUp(self):
        """
        Creates the test configuration files and scheme.
        """
        self.create_test_file(test_data.DC_CONFIG_CFG_MOCK['cfgSource'])
        self.create_test_file(test_data.DC_CONFIG_JSON_MOCK['jsonSource'])
        self.create_test_file(test_data.DC_CONFIG_XML_MOCK['xmlSource'])
        self.create_test_scheme()

    def tearDown(self):
        """
        Removes the test configuration file and scheme.
        """
        self.remove_test_file(test_data.DC_CONFIG_CFG_MOCK['cfgSource'])
        self.remove_test_file(test_data.DC_CONFIG_JSON_MOCK['jsonSource'])
        self.remove_test_file(test_data.DC_CONFIG_XML_MOCK['xmlSource'])
        self.remove_test_scheme()

    def create_test_file(self, config_mock):
        """
        Helper method to create a test file.
        """
        with open(config_mock['name'], 'w', encoding='utf-8') as file:
            file.write(config_mock['content'])

    def create_test_scheme(self):
        """
        Helper method to create a test scheme.
        """
        os.makedirs(test_data.SCHEME_PATH, exist_ok=True)
        for ext in ['cfg', 'xml']:
            with open(
                os.path.join(
                    test_data.SCHEME_PATH, f'{test_data.SCHEME_NAME}.{ext}'
                ), 'w', encoding='utf-8'
            ) as file:
                pass

    def remove_test_file(self, config_mock):
        """
        Helper method to remove a test file.
        """
        if os.path.exists(config_mock['name']):
            os.remove(config_mock['name'])
        if os.path.exists(f'{config_mock['name']}.backup'):
            os.remove(f'{config_mock['name']}.backup')

    def remove_test_scheme(self):
        """
        Helper method to remove a test scheme.
        """
        if os.path.exists(test_data.SCHEME_PATH):
            shutil.rmtree(test_data.SCHEME_PATH)

    def test_get_asset_path(self):
        """
        Tests the get_asset_path method.
        """
        asset_path = self.app_utils.get_asset_path(test_data.ASSET_PATH)

        # Check that the returned path is the expected path
        self.assertEqual(asset_path, os.path.abspath(test_data.ASSET_PATH))

    def test_get_config(self):
        """
        Tests the get_config method.
        """
        dc_config_path = (
            self.dc_file_manager.get_config(test_data.DC_CONFIG_PATHS['test'])
        )

        # Check that the returned path is the expected path
        self.assertEqual(
            dc_config_path,
            os.path.expandvars(test_data.DC_CONFIG_PATHS['test'])
        )

    def test_backup_config(self):
        """
        Tests the backup_config method.
        """
        self.dc_file_manager.backup_config(
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['name']
        )

        # Check that backup files was created successfully
        self.assertTrue(
            os.path.exists(
                f'{test_data.DC_CONFIG_XML_MOCK['xmlSource']['name']}.backup'
            ),
            "Config backup file does not exist."
        )

    def test_get_cfg(self):
        """
        Tests the get_cfg method.
        """
        config = self.scheme_file_manager.get_cfg(
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['name']
        )

        # Validate config against cfg schema
        config = configobj.ConfigObj(
            config,
            configspec=test_data.DC_CONFIG_CFG_MOCK['cfgSource']['schema']
                .splitlines()
        )

        validator = configobjVal.Validator()
        validator_result = config.validate(validator, preserve_errors=True)

        self.assertTrue(
            True if validator_result is True else False,
            validator_result
        )

    @patch(
        'builtins.open', new_callable=mock_open,
        read_data=test_data.DC_CONFIG_CFG_MOCK['cfgSource']['content']
    )
    def test_set_cfg(self, mock_open):
        """
        Tests the set_cfg method.
        """
        self.scheme_file_manager.set_cfg(
            self.scheme_file_manager.get_cfg(
                test_data.DC_CONFIG_CFG_MOCK['cfgSource']['name']
            ),
            test_data.DC_CONFIG_CFG_MOCK['cfgTarget']['name']
        )

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([
            call(
                test_data.DC_CONFIG_CFG_MOCK['cfgTarget']['name'], 'w',
                encoding='utf-8'
            )
        ])

    def test_get_json(self):
        """
        Tests the get_json method.
        """
        config = self.scheme_file_manager.get_json(
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['name']
        )

        # Validate config against json schema
        jsonschema.validate(
            config,
            json.loads(test_data.DC_CONFIG_JSON_MOCK['jsonSource']['schema'])
        )

    @patch(
        'builtins.open', new_callable=mock_open,
        read_data=test_data.DC_CONFIG_JSON_MOCK['jsonSource']['content']
    )
    def test_set_json(self, mock_open):
        """
        Tests the set_json method.
        """
        self.scheme_file_manager.set_json(
            self.scheme_file_manager.get_json(
                test_data.DC_CONFIG_JSON_MOCK['jsonSource']['name']
            ),
            test_data.DC_CONFIG_JSON_MOCK['jsonTarget']['name']
        )

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([
            call(
                test_data.DC_CONFIG_JSON_MOCK['jsonTarget']['name'], 'w',
                encoding='utf-8'
            )
        ])

    @patch('builtins.open', new_callable=mock_open)
    def test_set_xml(self, mock_open):
        """
        Tests the set_xml method.
        """
        self.scheme_file_manager.set_xml(
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['content'],
            test_data.DC_CONFIG_XML_MOCK['xmlTarget']['name']
        )

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([
            call(
                test_data.DC_CONFIG_XML_MOCK['xmlTarget']['name'], 'w',
                encoding='utf-8'
            )
        ])

    def test_list_schemes(self):
        """
        Tests the list_schemes method.
        """
        with self.assertRaises(FileNotFoundError):
            self.scheme_file_manager.list_schemes(
                test_data.SCHEME_PATH,
                test_data.USER_CONFIG_DEFAULT['schemes']['extensions']
            )

if __name__ == '__main__':
    """
    Main execution point of the unit tests.
    """
    unittest.main()