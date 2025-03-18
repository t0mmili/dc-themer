import io
import os
import sys
import unittest
from unittest.mock import mock_open, patch
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

        cls.cfg_source_content = (
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['content']
        )
        cls.cfg_source_name = test_data.DC_CONFIG_CFG_MOCK['cfgSource']['name']
        cls.cfg_source_schema = (
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['schema']
        )
        cls.cfg_target_name = test_data.DC_CONFIG_CFG_MOCK['cfgTarget']['name']
        cls.json_source_name = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['name']
        )
        cls.json_source_schema = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['schema']
        )
        cls.json_target_name = (
            test_data.DC_CONFIG_JSON_MOCK['jsonTarget']['name']
        )
        cls.xml_source_content = (
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['content']
        )
        cls.xml_source_name = test_data.DC_CONFIG_XML_MOCK['xmlSource']['name']
        cls.xml_target_name = test_data.DC_CONFIG_XML_MOCK['xmlTarget']['name']

        cls.asset_default_config_path = test_data.ASSET_PATH
        cls.dc_config_path_test = test_data.DC_CONFIG_PATHS['test']
        cls.scheme_name = test_data.SCHEME_NAME
        cls.scheme_path = test_data.SCHEME_PATH
        cls.user_config_extensions = (
            test_data.USER_CONFIG_DEFAULT['schemes']['extensions']
        )

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

    @patch('shutil.copy', return_value=None)
    def test_backup_config(self, mock_copy):
        """
        Tests the backup_config method.
        """
        self.dc_file_manager.backup_config(self.xml_source_name)

        # Check that mock was called once with specific arguments
        mock_copy.assert_called_once_with(
            self.xml_source_name, f'{self.xml_source_name}.backup'
        )

    def test_get_cfg(self):
        """
        Tests the get_cfg method.
        """
        # Mock source cfg file
        cfg_source_file = io.StringIO(self.cfg_source_content)

        config = self.scheme_file_manager.get_cfg(cfg_source_file)

        # Validate config against cfg schema
        config.configspec = configobj.ConfigObj(
            self.cfg_source_schema.splitlines()
        )
        validator = configobjVal.Validator()
        validator_result = config.validate(validator, preserve_errors=True)

        self.assertTrue(
            True if validator_result is True else False, validator_result
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
        mock_open.assert_called_with(
            self.cfg_target_name, 'w', encoding='utf-8'
        )

    @patch(
        'builtins.open', new_callable=mock_open,
        read_data=test_data.DC_CONFIG_JSON_MOCK['jsonSource']['content']
    )
    def test_get_json(self, mock_open):
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
        mock_open.assert_called_with(
            self.json_target_name, 'w', encoding='utf-8'
        )

    @patch('builtins.open', new_callable=mock_open)
    def test_set_xml(self, mock_open):
        """
        Tests the set_xml method.
        """
        self.scheme_file_manager.set_xml(
            self.xml_source_content.encode('utf-8'), self.xml_target_name
        )

        # Check that open was called with specific arguments
        mock_open.assert_called_with(self.xml_target_name, 'wb')

    @patch(
        'os.listdir',
        return_value=['test-scheme.cfg', 'test-scheme.json', 'test-scheme.xml']
    )
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_list_schemes_success(
        self, mock_isfile, mock_exists, mock_listdir
    ):
        """
        Tests the list_schemes method.
        """
        scheme_list = self.scheme_file_manager.list_schemes(
            self.scheme_path, self.user_config_extensions
        )

        # Check that the returned scheme list is the expected list
        self.assertEqual(scheme_list, [self.scheme_name])

    @patch(
        'os.listdir', return_value=['test-scheme.cfg', 'test-scheme.xml']
    )
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    def test_list_schemes_missing_files(
        self, mock_isfile, mock_exists, mock_listdir
    ):
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