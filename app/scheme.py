from configobj import ConfigObj
from defusedxml.ElementTree import parse, tostring
from defusedxml.minidom import parseString
from os import path
from tkinter.messagebox import showwarning
from utils import DCFileManager, SchemeFileManager

class Scheme:
    """
    A class to apply color schemes to configuration files.

    Attributes:
        scheme (str): The name of the scheme.
        scheme_path (str): The file path where the scheme files are located.
        dc_configs (dict): A dictionary containing DC configuration file types
                           and their paths.
        dc_configs_backup (bool): A flag to backup DC  configuration before
                                  scheme apply.
        auto_dark_mode (bool): A flag to force auto dark mode if True.
        xml_tags (list): A list of XML tags to be modified in XML configuration
                         files.

    Methods:
        apply_scheme(): Applies the scheme to all configuration files
                        (cfg, json, xml).
        apply_scheme_cfg(): Applies the scheme specifically to the cfg
                            configuration file.
        apply_scheme_json(): Applies the scheme specifically to the json
                             configuration file.
        apply_scheme_xml(): Applies the scheme specifically to the xml
                            configuration file.
        verify_scheme(): Verifies the scheme version of all configuration files
                         (cfg, json, xml).
        verify_scheme_version_xml(): Verifies the scheme version of xml
                                     configuration file specifically.
    """
    def __init__(
        self, scheme: str, scheme_path: str, dc_configs: dict[str, str],
        dc_configs_backup: bool, auto_dark_mode: bool, xml_tags: list[str]
    ) -> None:
        """
        Constructs all the necessary attributes for the Scheme object.

        Args:
            scheme (str): The name of the scheme.
            scheme_path (str): The file path where the scheme files are
                               located.
            dc_configs (dict[str, str]): A dictionary containing DC
                                         configuration file types and their
                                         paths.
            dc_configs_backup (bool): A flag to backup DC  configuration before
                                      scheme apply.
            auto_dark_mode (bool): A flag to force auto dark mode if True.
            xml_tags (list[str]): A list of XML tags to be modified in xml
                                  configuration files.
        """
        self.scheme: str = scheme
        self.scheme_path: str = scheme_path
        self.dc_configs: dict[str, str] = dc_configs
        self.dc_configs_backup: bool = dc_configs_backup
        self.auto_dark_mode: bool = auto_dark_mode
        self.xml_tags: list[str] = xml_tags

    def apply_scheme(self) -> None:
        """
        Applies the scheme to all configuration files (cfg, json, xml).
        """
        self.apply_scheme_cfg()
        self.apply_scheme_json()
        self.apply_scheme_xml()

    def apply_scheme_cfg(self) -> None:
        """
        Applies the scheme specifically to the cfg configuration file.
        """
        source_file: str = path.join(self.scheme_path, f'{self.scheme}.cfg')
        target_file: str = DCFileManager.get_config(self.dc_configs['cfg'])
        source_config: ConfigObj = SchemeFileManager.get_cfg(source_file)
        target_config: ConfigObj = SchemeFileManager.get_cfg(target_file)

        # Set new 'DarkMode' value
        target_config['DarkMode'] = (
            '1' if self.auto_dark_mode else source_config['DarkMode']
        )

        # Backup current configuration
        if self.dc_configs_backup:
            DCFileManager.backup_config(target_file)

        # Save modified DC cfg config file
        SchemeFileManager.set_cfg(target_config, target_file)

    def apply_scheme_json(self) -> None:
        """
        Applies the scheme specifically to the json configuration file.
        """
        source_file: str = path.join(self.scheme_path, f'{self.scheme}.json')
        target_file: str = DCFileManager.get_config(self.dc_configs['json'])
        source_config: dict = SchemeFileManager.get_json(source_file)
        target_config: dict = SchemeFileManager.get_json(target_file)

        # Backup current configuration
        if self.dc_configs_backup:
            DCFileManager.backup_config(target_file)

        # Replace the style if name matches
        for i, style in enumerate(target_config['Styles']):
            if style['Name'] == source_config['Styles'][0]['Name']:
                target_config['Styles'][i] = source_config['Styles'][0]
                break

        # Replace the file colors
        target_config['FileColors'] = source_config['FileColors']

        # Save modified DC json config file
        SchemeFileManager.set_json(target_config, target_file)

    def apply_scheme_xml(self) -> None:
        """
        Applies the scheme specifically to the xml configuration file.
        """
        source_file: str = path.join(self.scheme_path, f'{self.scheme}.xml')
        target_file: str = DCFileManager.get_config(self.dc_configs['xml'])

        # Backup current configuration
        if self.dc_configs_backup:
            DCFileManager.backup_config(target_file)

        for item in self.xml_tags:
            # Create element tree object
            source_tree = parse(source_file)
            target_tree = parse(target_file)

            # Get root element
            target_root = target_tree.getroot()

            source_tag = source_tree.find(f'./{item}')
            target_tag = target_tree.find(f'./{item}')

            # Remove current tags and append new ones
            if source_tag is not None:
                if target_tag is not None:
                    target_root.remove(target_tag)
                target_root.append(source_tag)
            else:
                raise ValueError(
                    f'Tag \'{item}\' does not exist in the source xml '
                    'configuration data.'
                )

            # Prettify XML
            xml_str: str = tostring(target_root, encoding='utf-8')
            dom = parseString(xml_str)
            pretty_xml: str = dom.toprettyxml(indent='  ')
            pretty_xml = '\n'.join(
                [line for line in pretty_xml.split('\n') if line.strip()]
            )

            # Save modified DC xml config file
            SchemeFileManager.set_xml(pretty_xml, target_file)

    def verify_scheme(self) -> None:
        """
        Verifies the scheme version of all configuration files
        (cfg, json, xml).
        """
        self.verify_scheme_version_xml()

    def verify_scheme_version_xml(self) -> None:
        """
        Verifies the scheme version of xml configuration file specifically.
        """
        source_file: str = path.join(self.scheme_path, f'{self.scheme}.xml')
        target_file: str = DCFileManager.get_config(self.dc_configs['xml'])

        source_tree = parse(source_file)
        target_tree = parse(target_file)

        source_config_version: str | None = (
            source_tree.getroot().attrib.get('ConfigVersion')
        )
        target_config_version: str | None = (
            target_tree.getroot().attrib.get('ConfigVersion')
        )

        if source_config_version != target_config_version:
            showwarning(
                title='Warning',
                message=(
                    'XML configuration scheme version mismatch:\n\n'
                    f'Source scheme: {source_config_version}\n'
                    f'Target scheme: {target_config_version}\n\n'
                    'The apply process will continue.\n'
                    'In case of any issues, please verify your configuration '
                    'files.'
                )
            )