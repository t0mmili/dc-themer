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

        cls.asset_default_config_path = test_data.ASSET_PATH
        cls.cfg_source_content = (
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['content']
        )
        cls.cfg_source_name = test_data.DC_CONFIG_CFG_MOCK['cfgSource']['name']
        cls.cfg_source_schema = (
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['schema']
        )
        cls.cfg_target_name = test_data.DC_CONFIG_CFG_MOCK['cfgTarget']['name']
        cls.dc_config_path_test = test_data.DC_CONFIG_PATHS['test']
        cls.json_source_name = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['name']
        )
        cls.json_source_schema = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['schema']
        )
        cls.json_target_name = (
            test_data.DC_CONFIG_JSON_MOCK['jsonTarget']['name']
        )
        cls.scheme_name = test_data.SCHEME_NAME
        cls.scheme_path = test_data.SCHEME_PATH
        cls.xml_source_content = (
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['content']
        )
        cls.xml_source_name = test_data.DC_CONFIG_XML_MOCK['xmlSource']['name']
        cls.xml_target_name = test_data.DC_CONFIG_XML_MOCK['xmlTarget']['name']
        cls.user_config_extensions = (
            test_data.USER_CONFIG_DEFAULT['schemes']['extensions']
        )

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
        os.makedirs(self.scheme_path, exist_ok=True)
        for ext in ['cfg', 'xml']:
            open(
                os.path.join(
                    self.scheme_path, f'{self.scheme_name}.{ext}'
                ), 'w', encoding='utf-8'
            ).close()

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
        if os.path.exists(self.scheme_path):
            shutil.rmtree(self.scheme_path)

    def test_get_asset_path(self):
        """
        Tests the get_asset_path method.
        """
        asset_path = self.app_utils.get_asset_path(
            self.asset_default_config_path
        )

        # Check that the returned path is the expected path
        self.assertEqual(
            asset_path,
            os.path.abspath(self.asset_default_config_path)
        )

    def test_get_config(self):
        """
        Tests the get_config method.
        """
        dc_config_path = (
            self.dc_file_manager.get_config(self.dc_config_path_test)
        )

        # Check that the returned path is the expected path
        self.assertEqual(
            dc_config_path,
            os.path.expandvars(self.dc_config_path_test)
        )

    def test_backup_config(self):
        """
        Tests the backup_config method.
        """
        self.dc_file_manager.backup_config(
            self.xml_source_name
        )

        # Check that backup files was created successfully
        self.assertTrue(
            os.path.exists(
                f'{self.xml_source_name}.backup'
            ),
            "Config backup file does not exist."
        )

    def test_get_cfg(self):
        """
        Tests the get_cfg method.
        """
        config = self.scheme_file_manager.get_cfg(self.cfg_source_name)

        # Validate config against cfg schema
        config = configobj.ConfigObj(
            config,
            configspec=self.cfg_source_schema.splitlines()
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
            self.scheme_file_manager.get_cfg(self.cfg_source_name),
            self.cfg_target_name
        )

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([
            call(self.cfg_target_name, 'w', encoding='utf-8')
        ])

    def test_get_json(self):
        """
        Tests the get_json method.
        """
        config = self.scheme_file_manager.get_json(self.json_source_name)

        # Validate config against json schema
        jsonschema.validate(config, json.loads(self.json_source_schema))

    @patch(
        'builtins.open', new_callable=mock_open,
        read_data=test_data.DC_CONFIG_JSON_MOCK['jsonSource']['content']
    )
    def test_set_json(self, mock_open):
        """
        Tests the set_json method.
        """
        self.scheme_file_manager.set_json(
            self.scheme_file_manager.get_json(self.json_source_name),
            self.json_target_name
        )

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([
            call(self.json_target_name, 'w', encoding='utf-8')
        ])

    @patch('builtins.open', new_callable=mock_open)
    def test_set_xml(self, mock_open):
        """
        Tests the set_xml method.
        """
        self.scheme_file_manager.set_xml(
            self.xml_source_content.encode('utf-8'), self.xml_target_name
        )

        # Check that open was called with specific arguments
        mock_open.assert_has_calls([call(self.xml_target_name, 'wb')])

    def test_list_schemes(self):
        """
        Tests the list_schemes method.
        """
        with self.assertRaises(FileNotFoundError):
            self.scheme_file_manager.list_schemes(
                self.scheme_path, self.user_config_extensions
            )

if __name__ == '__main__':
    """
    Main execution point of the unit tests.
    """
    unittest.main()