import io
import os
import sys
import unittest
from unittest.mock import patch
import configobj
import json_repair
import defusedxml.ElementTree as defusedxmlET
import xml.etree.ElementTree as ET

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
            test_data.AUTO_DARK_MODE, test_data.SCHEME_XML_TAGS
        )
        cls.scheme_creator = scheme.SchemeCreator(
            test_data.SCHEME_NAME, test_data.SCHEME_PATH,
            test_data.DC_CONFIG_PATHS['cfg'],
            test_data.DC_CONFIG_PATHS['json'],
            test_data.DC_CONFIG_PATHS['xml'], 0, test_data.SCHEME_XML_TAGS
        )
        
        cls.cfg_source_content = (
            test_data.DC_CONFIG_CFG_MOCK['cfgSource']['content']
        )
        cls.cfg_target_content = (
            test_data.DC_CONFIG_CFG_MOCK['cfgTarget']['content']
        )
        cls.json_source_content = (
            test_data.DC_CONFIG_JSON_MOCK['jsonSource']['content']
        )
        cls.json_target_content = (
            test_data.DC_CONFIG_JSON_MOCK['jsonTarget']['content']
        )
        cls.scheme_xml_tags = test_data.SCHEME_XML_TAGS
        cls.xml_source_content = (
            test_data.DC_CONFIG_XML_MOCK['xmlSource']['content']
        )
        cls.xml_target_content = (
            test_data.DC_CONFIG_XML_MOCK['xmlTarget']['content']
        )

    @patch('os.path.join', return_value='source.cfg')
    @patch('app.utils.DCFileManager.get_config', return_value='target.cfg')
    @patch('app.utils.SchemeFileManager.get_cfg')
    @patch('app.utils.DCFileManager.backup_config')
    @patch('app.utils.SchemeFileManager.set_cfg')
    def test_apply_scheme_cfg_source_target(
        self, mock_set_cfg, mock_backup_config, mock_get_cfg, *_
    ):
        """
        Tests the apply_scheme_cfg method for success.
        Case details: Set target DarkMode based on source value.
        """
        mock_get_cfg.side_effect = lambda path: configobj.ConfigObj(
            io.StringIO(
                self.cfg_source_content if 'source' in path else
                self.cfg_target_content
            )
        )

        self.scheme.apply_scheme_cfg()

        # Check that source 'DarkMode' value was applied correctly to target
        self.assertEqual(
            mock_get_cfg('source')['DarkMode'],
            mock_set_cfg.call_args[0][0]['DarkMode']
        )

    @patch('os.path.join', return_value='source.cfg')
    @patch('app.utils.DCFileManager.get_config', return_value='target.cfg')
    @patch('app.utils.SchemeFileManager.get_cfg')
    @patch('app.utils.DCFileManager.backup_config')
    @patch('app.utils.SchemeFileManager.set_cfg')
    def test_apply_scheme_cfg_auto_dark_mode(
        self, mock_set_cfg, mock_backup_config, mock_get_cfg, *_
    ):
        """
        Tests the apply_scheme_cfg method for success.
        Case details: Set target DarkMode to auto.
        """
        mock_get_cfg.side_effect = lambda path: configobj.ConfigObj(
            io.StringIO(
                self.cfg_source_content if 'source' in path else
                self.cfg_target_content
            )
        )

        with patch.object(self.scheme, 'auto_dark_mode', new=True):
            self.scheme.apply_scheme_cfg()

        # Check that target has 'DarkMode' value set to auto
        self.assertEqual(mock_set_cfg.call_args[0][0]['DarkMode'], '1')

    @patch('os.path.join', return_value='source.json')
    @patch('app.utils.DCFileManager.get_config', return_value='target.json')
    @patch('app.utils.SchemeFileManager.get_json')
    @patch('app.utils.DCFileManager.backup_config')
    @patch('app.utils.SchemeFileManager.set_json')
    def test_apply_scheme_json(
        self, mock_set_json, mock_backup_config, mock_get_json, *_
    ):
        """
        Tests the apply_scheme_json method.
        """
        mock_get_json.side_effect = lambda path: json_repair.loads(
            self.json_source_content if 'source' in path else
            self.json_target_content
        )

        self.scheme.apply_scheme_json()

        # Check that source was applied correctly to target
        self.assertEqual(
            mock_get_json('source'), mock_set_json.call_args[0][0]
        )

    @patch('os.path.join', return_value='source.xml')
    @patch('app.utils.DCFileManager.get_config', return_value='target.xml')
    @patch('app.utils.DCFileManager.backup_config')
    @patch('defusedxml.ElementTree.parse')
    @patch('app.utils.SchemeFileManager.set_xml')
    def test_apply_scheme_xml(self, mock_set_xml, mock_parse, *_):
        """
        Tests the apply_scheme_xml method.
        """
        mock_parse.side_effect = lambda path: ET.ElementTree(
            defusedxmlET.fromstring(
                self.xml_source_content if 'source' in path else
                self.xml_target_content
            )
        )

        self.scheme.apply_scheme_xml()

        # Check that source was applied correctly to target
        self.assert_xml_equal(
            self.xml_source_content, mock_set_xml.call_args[0][0],
            self.scheme_xml_tags
        )

    @patch('os.path.join', return_value='source.xml')
    @patch('app.utils.DCFileManager.get_config', return_value='target.xml')
    @patch('defusedxml.ElementTree.parse')
    @patch('tkinter.messagebox._show')
    def test_verify_scheme_version_xml(self, mock_show, mock_parse, *_):
        """
        Tests the verify_scheme_version_xml method.
        """
        mock_parse.side_effect = lambda path: ET.ElementTree(
            defusedxmlET.fromstring(
                self.xml_source_content if 'source' in path else
                self.xml_target_content
            )
        )

        self.scheme.verify_scheme_version_xml()

        # Check that 'warning' message box was called once
        mock_show.assert_called_once()
        self.assertEqual(mock_show.call_args[0][2], 'warning')

    @patch('app.utils.DCFileManager.get_config', return_value='source.cfg')
    @patch('os.path.join', return_value='target.cfg')
    @patch('app.utils.SchemeFileManager.get_cfg')
    @patch('app.utils.SchemeFileManager.set_cfg')
    def test_create_scheme_cfg(self, mock_set_cfg, mock_get_cfg, *_):
        """
        Tests the create_scheme_cfg method.
        """
        mock_get_cfg.return_value = (
            configobj.ConfigObj(io.StringIO(self.cfg_source_content))
        )

        self.scheme_creator.create_scheme_cfg()

        # Check that source 'DarkMode' value was applied correctly to target
        self.assertEqual(
            mock_get_cfg()['DarkMode'],
            mock_set_cfg.call_args[0][0]['DarkMode']
        )

    @patch('app.utils.DCFileManager.get_config', return_value='source.json')
    @patch('os.path.join', return_value='target.json')
    @patch('app.utils.SchemeFileManager.get_json')
    @patch('app.utils.SchemeFileManager.set_json')
    def test_create_scheme_json(self, mock_set_json, mock_get_json, *_):
        """
        Tests the create_scheme_json method.
        """
        mock_get_json.return_value = (
            json_repair.loads(self.json_source_content)
        )

        with patch.object(self.scheme_creator, 'dark_mode', new=1):
            self.scheme_creator.create_scheme_json()

        # Check that source was applied correctly to target
        self.assertEqual(mock_get_json(), mock_set_json.call_args[0][0])
        
    @patch('app.utils.DCFileManager.get_config', return_value='source.xml')
    @patch('os.path.join', return_value='target.xml')
    @patch('defusedxml.ElementTree.parse')
    @patch('app.utils.SchemeFileManager.set_xml')
    def test_create_scheme_xml(self, mock_set_xml, mock_parse, *_):
        """
        Tests the create_scheme_xml method.
        """
        mock_parse.return_value = (
            ET.ElementTree(defusedxmlET.fromstring(self.xml_source_content))
        )

        self.scheme_creator.create_scheme_xml()

        # Check that source was applied correctly to target
        self.assert_xml_equal(
            self.xml_source_content, mock_set_xml.call_args[0][0],
            self.scheme_xml_tags
        )

    def assert_xml_equal(self, source_content, target_content, xml_tags):
        """
        Helper method to assert that XML files are equal.
        """
        source_config = (
            ET.ElementTree(defusedxmlET.fromstring(source_content))
        )
        target_config = (
            ET.ElementTree(defusedxmlET.fromstring(target_content))
        )

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