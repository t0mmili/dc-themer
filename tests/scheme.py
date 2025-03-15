import os
import sys
import unittest
from unittest.mock import patch
import tkinter.messagebox as messagebox
import configobj
import defusedxml.ElementTree as defusedxmlET

# Append the parent directory to the system path to access app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import scheme
import test_data

class TestScheme(unittest.TestCase):
    """
    A set of unit tests for the Scheme class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Initializes the Scheme class with test data.
        """
        cls.scheme = scheme.Scheme(
            test_data.SCHEME_NAME, test_data.SCHEME_PATH,
            test_data.DC_CONFIG_PATHS, test_data.DC_BACKUP_CONFIGS,
            test_data.DARK_MODE, test_data.SCHEME_XML_TAGS
        )
        cls.scheme_creator = scheme.SchemeCreator(
            test_data.SCHEME_NAME, test_data.SCHEME_PATH,
            test_data.DC_CONFIG_PATHS['cfg'],
            test_data.DC_CONFIG_PATHS['json'],
            test_data.DC_CONFIG_PATHS['xml'], 2, test_data.SCHEME_XML_TAGS
        )
        
        cls.cfg_source_name = test_data.DC_CONFIG_CFG_MOCK['cfgSource']['name']
        cls.cfg_target_name = test_data.DC_CONFIG_CFG_MOCK['cfgTarget']['name']
        cls.json_source_name = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['name']
        )
        cls.json_target_name = (
            test_data.DC_CONFIG_JSON_MOCK['jsonTarget']['name']
        )
        cls.scheme_xml_tags = test_data.SCHEME_XML_TAGS
        cls.xml_source_name = test_data.DC_CONFIG_XML_MOCK['xmlSource']['name']
        cls.xml_target_name = test_data.DC_CONFIG_XML_MOCK['xmlTarget']['name']
        cls.xml_source_version = (
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['version']
        )
        cls.xml_target_version = (
            test_data.DC_CONFIG_XML_MOCK['xmlTarget']['version']
        )

    def setUp(self):
        """
        Creates the test configuration files.
        """
        self.create_test_file(test_data.DC_CONFIG_CFG_MOCK['cfgSource'])
        self.create_test_file(test_data.DC_CONFIG_CFG_MOCK['cfgTarget'])
        self.create_test_file(test_data.DC_CONFIG_JSON_MOCK['jsonSource'])
        self.create_test_file(test_data.DC_CONFIG_JSON_MOCK['jsonTarget'])
        self.create_test_file(test_data.DC_CONFIG_XML_MOCK['xmlSource'])
        self.create_test_file(test_data.DC_CONFIG_XML_MOCK['xmlTarget'])

    def tearDown(self):
        """
        Removes the test configuration file.
        """
        self.remove_test_file(test_data.DC_CONFIG_CFG_MOCK['cfgSource'])
        self.remove_test_file(test_data.DC_CONFIG_CFG_MOCK['cfgTarget'])
        self.remove_test_file(test_data.DC_CONFIG_JSON_MOCK['jsonSource'])
        self.remove_test_file(test_data.DC_CONFIG_JSON_MOCK['jsonTarget'])
        self.remove_test_file(test_data.DC_CONFIG_XML_MOCK['xmlSource'])
        self.remove_test_file(test_data.DC_CONFIG_XML_MOCK['xmlTarget'])

    def create_test_file(self, config_mock):
        """
        Helper method to create a test file.
        """
        with open(config_mock['name'], 'w', encoding='utf-8') as file:
            file.write(config_mock['content'])

    def remove_test_file(self, config_mock):
        """
        Helper method to remove a test file.
        """
        if os.path.exists(config_mock['name']):
            os.remove(config_mock['name'])

    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_apply_scheme_cfg(self, mock_join, mock_get_config):
        """
        Tests the apply_scheme_cfg method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_apply(
            mock_join, mock_get_config, self.cfg_source_name,
            self.cfg_target_name
        )

        self.scheme.apply_scheme_cfg()

        # Check that changes were applied correctly
        self.assert_config_files_equal(
            scheme.SchemeFileManager.get_cfg, self.cfg_source_name,
            self.cfg_target_name
        )

    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_apply_scheme_json(self, mock_join, mock_get_config):
        """
        Tests the apply_scheme_json method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_apply(
            mock_join, mock_get_config, self.json_source_name,
            self.json_target_name
        )

        self.scheme.apply_scheme_json()

        # Check that changes were applied correctly
        self.assert_config_files_equal(
            scheme.SchemeFileManager.get_json, self.json_source_name,
            self.json_target_name
        )

    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_apply_scheme_xml(self, mock_join, mock_get_config):
        """
        Tests the apply_scheme_xml method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_apply(
            mock_join, mock_get_config, self.xml_source_name,
            self.xml_target_name
        )

        self.scheme.apply_scheme_xml()

        # Check that changes were applied correctly
        self.assert_xml_files_equal(
            self.xml_source_name, self.xml_target_name, self.scheme_xml_tags
        )

    @patch('tkinter.messagebox._show')
    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_verify_scheme_version_xml(
            self, mock_join, mock_get_config, mock_show
        ):
        """
        Tests the verify_scheme_version_xml method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_apply(
            mock_join, mock_get_config, self.xml_source_name,
            self.xml_target_name
        )

        self.scheme.verify_scheme_version_xml()

        mock_show.assert_called_once_with(
            "Warning",
            (
                'XML configuration scheme version mismatch:\n\n'
                'Source scheme: '
                f'{self.xml_source_version}\n'
                'Target scheme: '
                f'{self.xml_target_version}\n\n'
                'The apply process will continue.\n'
                'In case of any issues, please verify your configuration '
                'files.'
            ),
            messagebox.WARNING, messagebox.OK
        )

    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_create_scheme_cfg(self, mock_get_config, mock_join):
        """
        Tests the create_scheme_cfg method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_create(
            mock_get_config, mock_join, self.cfg_source_name,
            self.cfg_target_name
        )

        self.scheme_creator.create_scheme_cfg()

        # Check that changes were applied correctly
        self.assert_config_files_darkmode_equal(
            scheme.SchemeFileManager.get_cfg, self.cfg_source_name,
            self.cfg_target_name
        )

    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_create_scheme_json(self, mock_get_config, mock_join):
        """
        Tests the create_scheme_json method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_create(
            mock_get_config, mock_join, self.json_source_name,
            self.json_target_name
        )

        self.scheme_creator.create_scheme_json()

        # Check that changes were applied correctly
        self.assert_config_files_equal(
            scheme.SchemeFileManager.get_json, self.json_source_name,
            self.json_target_name
        )

    @patch('app.utils.DCFileManager.get_config')
    @patch('os.path.join')
    def test_create_scheme_xml(self, mock_get_config, mock_join):
        """
        Tests the create_scheme_xml method.
        """
        # Mock the return values for the dependent methods
        self.setup_mock_methods_create(
            mock_get_config, mock_join, self.xml_source_name,
            self.xml_target_name
        )

        self.scheme_creator.create_scheme_xml()

        # Check that changes were applied correctly
        self.assert_xml_files_equal(
            self.xml_source_name, self.xml_target_name, self.scheme_xml_tags
        )

    def setup_mock_methods_apply(
            self, mock_join, mock_get_config, source_name, target_name
        ):
        """
        Helper method to setup mock methods for apply related tests.
        """
        mock_join.return_value = source_name
        mock_get_config.return_value = target_name

    def setup_mock_methods_create(
            self, mock_get_config, mock_join, source_name, target_name
        ):
        """
        Helper method to setup mock methods for create related tests.
        """
        mock_get_config.return_value = source_name
        mock_join.return_value = target_name

    def assert_config_files_equal(self, get_method, source_name, target_name):
        """
        Helper method to assert that config files are equal.
        """
        source_config = get_method(source_name)
        target_config = get_method(target_name)

        self.assertDictEqual(source_config, target_config)

    def assert_config_files_darkmode_equal(
            self, get_method, source_name, target_name
        ):
        """
        Helper method to assert that config files have equal DarkMode key.
        """
        source_config: configobj.ConfigObj = get_method(source_name)
        target_config: configobj.ConfigObj = get_method(target_name)

        self.assertEqual(source_config['DarkMode'], target_config['DarkMode'])

    def assert_xml_files_equal(self, source_name, target_name, xml_tags):
        """
        Helper method to assert that XML files are equal.
        """
        source_config = defusedxmlET.parse(source_name)
        target_config = defusedxmlET.parse(target_name)

        for item in xml_tags:
            source_tag = source_config.find(f'./{item}')
            target_tag = target_config.find(f'./{item}')

            if source_tag is not None and target_tag is not None:
                self.assertEqual(
                    defusedxmlET.tostring(
                        source_tag, encoding='utf-8'
                    ).decode('utf-8').strip(),
                    defusedxmlET.tostring(
                        target_tag, encoding='utf-8'
                    ).decode('utf-8').strip()
                )

if __name__ == '__main__':
    """
    Main execution point of the unit tests.
    """
    unittest.main()