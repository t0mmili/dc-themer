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
        cls.cfg_source_schema = (
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['schema']
        )
        cls.json_source_content = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['content']
        )
        cls.json_source_schema = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['schema']
        )
        cls.xml_source_content = (
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['content']
        )

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

    def test_get_config_success(self):
        """
        Tests the get_config method for success.
        """
        dc_config_path = (
            self.dc_file_manager.get_config(self.dc_config_path_test)
        )

        # Check that the returned path is the expected path
        self.assertEqual(
            dc_config_path,
            os.path.expandvars(self.dc_config_path_test)
        )

    @patch('os.path.exists')
    def test_get_config_file_not_found(self, mock_exists):
        """
        Tests the get_config method for failure.
        Case details: Config file was not found at the specified path.
        """
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            self.dc_file_manager.get_config(self.dc_config_path_test)

    @patch('shutil.copy')
    def test_backup_config_success(self, mock_copy):
        """
        Tests the backup_config method for success.
        """
        mock_copy.return_value = None

        self.dc_file_manager.backup_config('source.xml')

        # Check that mock was called once with specific arguments
        mock_copy.assert_called_once_with('source.xml', 'source.xml.backup')

    @patch('shutil.copy')
    def test_backup_config_copy_error(self, mock_copy):
        """
        Tests the backup_config method for failure.
        Case details: Error occurred during the copy operation.
        """
        mock_copy.side_effect = OSError()

        with self.assertRaises(OSError):
            self.dc_file_manager.backup_config('source.xml')

    def test_get_cfg_success(self):
        """
        Tests the get_cfg method for success.
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

    def test_get_cfg_invalid_config(self):
        """
        Tests the get_cfg method for failure.
        Case details: Config file contains invalid values.
        """
        # Mock source cfg file
        cfg_source_file = io.StringIO('TestKey: TestValue')

        with self.assertRaises(configobj.ConfigObjError):
            self.scheme_file_manager.get_cfg(cfg_source_file)

    @patch('builtins.open', new_callable=mock_open)
    def test_set_cfg_success(self, mock_open):
        """
        Tests the set_cfg method for success.
        """
        mock_open.read_data = self.cfg_source_content

        self.scheme_file_manager.set_cfg(configobj.ConfigObj(), 'target.cfg')

        # Check that open was called with specific arguments
        mock_open.assert_called_with('target.cfg', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_set_cfg_failed_write(self, mock_open):
        """
        Tests the set_cfg method for failure.
        Case details: Writing to file raised an exception.
        """
        mock_open.side_effect = OSError()

        with self.assertRaises(OSError):
            self.scheme_file_manager.set_cfg(
                configobj.ConfigObj(), 'target.cfg'
            )

    @patch('builtins.open', new_callable=mock_open)
    def test_get_json_success(self, mock_open):
        """
        Tests the get_json method for success.
        """
        mock_open.return_value.read.return_value = self.json_source_content

        config = self.scheme_file_manager.get_json('source.json')

        # Validate config against json schema
        jsonschema.validate(config, json.loads(self.json_source_schema))

    @patch('builtins.open', new_callable=mock_open)
    def test_get_json_type_error(self, mock_open):
        """
        Tests the get_json method for failure.
        Case details: Config file does not contain data of the correct type.
        """
        mock_open.return_value.read.return_value = str([])

        with self.assertRaises(TypeError):
            self.scheme_file_manager.get_json('source.json')

    @patch('builtins.open', new_callable=mock_open)
    def test_set_json_success(self, mock_open):
        """
        Tests the set_json method for success.
        """
        mock_open.return_value.read.return_value = self.json_source_content

        self.scheme_file_manager.set_json(
            self.scheme_file_manager.get_json('source.json'), 'target.json'
        )

        # Check that open was called with specific arguments
        mock_open.assert_called_with('target.json', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_set_json_failed_write(self, mock_open):
        """
        Tests the set_json method for failure.
        Case details: Writing to file raised an exception.
        """
        mock_open.side_effect = OSError()

        with self.assertRaises(OSError):
            self.scheme_file_manager.set_json({}, 'target.json')

    @patch('builtins.open', new_callable=mock_open)
    def test_set_xml_success(self, mock_open):
        """
        Tests the set_xml method for success.
        """
        self.scheme_file_manager.set_xml(
            self.xml_source_content.encode('utf-8'), 'target.xml'
        )

        # Check that open was called with specific arguments
        mock_open.assert_called_with('target.xml', 'wb')

    @patch('builtins.open', new_callable=mock_open)
    def test_set_xml_failed_write(self, mock_open):
        """
        Tests the set_xml method for failure.
        Case details: Writing to file raised an exception.
        """
        mock_open.side_effect = OSError()

        with self.assertRaises(OSError):
            self.scheme_file_manager.set_xml(''.encode('utf-8'), 'target.xml')

    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_list_schemes_success(
        self, mock_isfile, mock_exists, mock_listdir
    ):
        """
        Tests the list_schemes method for success.
        """
        mock_listdir.return_value = [
            'test-scheme.cfg', 'test-scheme.json', 'test-scheme.xml'
        ]
        mock_exists.return_value = True
        mock_isfile.return_value = True

        scheme_list = self.scheme_file_manager.list_schemes(
            self.scheme_path, self.user_config_extensions
        )

        # Check that the returned scheme list is the expected list
        self.assertEqual(scheme_list, [self.scheme_name])

    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_list_schemes_missing_files(
        self, mock_isfile, mock_exists, mock_listdir
    ):
        """
        Tests the list_schemes method for failure.
        Case details: One of the scheme files is missing.
        """
        mock_listdir.return_value = ['test-scheme.cfg', 'test-scheme.xml']
        mock_exists.return_value = True
        mock_isfile.return_value = True

        with self.assertRaises(FileNotFoundError):
            self.scheme_file_manager.list_schemes(
                self.scheme_path, self.user_config_extensions
            )

if __name__ == '__main__':
    """
    Main execution point of the unit tests.
    """
    unittest.main()