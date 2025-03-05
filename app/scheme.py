import os
from tkinter.messagebox import showwarning
import configobj
import defusedxml.ElementTree as defusedxmlET
import defusedxml.minidom as defusedxmlMD
from app.utils import DCFileManager, SchemeFileManager

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
            dc_configs_backup (bool): A flag to backup DC configuration before
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
        source_file: str = os.path.join(self.scheme_path, f'{self.scheme}.cfg')
        target_file: str = DCFileManager.get_config(self.dc_configs['cfg'])
        source_config: configobj.ConfigObj = (
            SchemeFileManager.get_cfg(source_file)
        )
        target_config: configobj.ConfigObj = (
            SchemeFileManager.get_cfg(target_file)
        )

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
        source_file: str = (
            os.path.join(self.scheme_path, f'{self.scheme}.json')
        )
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
        source_file: str = os.path.join(self.scheme_path, f'{self.scheme}.xml')
        target_file: str = DCFileManager.get_config(self.dc_configs['xml'])

        # Backup current configuration
        if self.dc_configs_backup:
            DCFileManager.backup_config(target_file)

        # Create element tree object
        source_tree = defusedxmlET.parse(source_file)
        target_tree = defusedxmlET.parse(target_file)

        # Get target root element
        target_root = target_tree.getroot()

        for item in self.xml_tags:
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
        xml_str: bytes = defusedxmlET.tostring(
            target_root, encoding='utf-8'
        )
        dom = defusedxmlMD.parseString(xml_str.decode('utf-8'))
        pretty_xml: bytes = dom.toprettyxml(indent='  ', encoding='utf-8')
        pretty_xml = b'\n'.join(
            [line for line in pretty_xml.split(b'\n') if line.strip()]
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
        source_file: str = os.path.join(self.scheme_path, f'{self.scheme}.xml')
        target_file: str = DCFileManager.get_config(self.dc_configs['xml'])

        source_tree = defusedxmlET.parse(source_file)
        target_tree = defusedxmlET.parse(target_file)

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

class SchemeCreator:
    """
    A class to create color schemes from configuration files.

    Attributes:
        scheme (str): The name of the scheme.
        scheme_path (str): The file path where the scheme files are located.
        dc_cfg_config_path (str): The path to the DC cfg configuration file.
        dc_json_config_path (str): The path to the DC json configuration file.
        dc_xml_config_path (str): The path to the DC xml configuration file.
        dark_mode (int): The dark mode flag (1 - auto, 2 - on, 3 - off).

    Methods:
        create_scheme(): Creates the scheme to all configuration files
                         (cfg, json, xml).
        create_scheme_cfg(): Creates the scheme specifically to the cfg
                             configuration file.
        create_scheme_json(): Creates the scheme specifically to the json
                              configuration file.
        create_scheme_xml(): Creates the scheme specifically to the xml
                             configuration file.
    """
    def __init__(
        self, scheme: str, scheme_path: str, dc_cfg_config_path: str,
        dc_json_config_path: str, dc_xml_config_path: str, dark_mode: int
    ) -> None:
        """
        Constructs all the necessary attributes for the SchemeCreator object.

        Args:
            scheme (str): The name of the scheme.
            scheme_path (str): The file path where the scheme files are
                               located.
            dc_cfg_config_path (str): The path to the DC cfg configuration
                                      file.
            dc_json_config_path (str): The path to the DC json configuration
                                       file.
            dc_xml_config_path (str): The path to the DC xml configuration
                                      file.
            dark_mode (int): The dark mode flag (1 - auto, 2 - on, 3 - off).
        """
        self.scheme: str = scheme
        self.scheme_path: str = scheme_path
        self.dc_cfg_config_path: str = dc_cfg_config_path
        self.dc_json_config_path: str = dc_json_config_path
        self.dc_xml_config_path: str = dc_xml_config_path
        self.dark_mode: int = dark_mode

    def create_scheme(self) -> None:
        """
        Creates the scheme from all configuration files (cfg, json, xml).
        """
        self.create_scheme_cfg()
        self.create_scheme_json()
        # self.create_scheme_xml()

    def create_scheme_cfg(self) -> None:
        """
        Creates the scheme specifically from the cfg configuration file.
        """
        source_file: str = DCFileManager.get_config(self.dc_cfg_config_path)
        target_file: str = os.path.join(self.scheme_path, f'{self.scheme}.cfg')
        source_config: configobj.ConfigObj = (
            SchemeFileManager.get_cfg(source_file)
        )
        target_config = configobj.ConfigObj()

        # Preserve only DarkMode key
        target_config['DarkMode'] = source_config['DarkMode']
        self.dark_mode = int(str(target_config['DarkMode']))

        # Save cfg scheme file
        SchemeFileManager.set_cfg(target_config, target_file)

    def create_scheme_json(self) -> None:
        """
        Creates the scheme specifically from the json configuration file.
        """
        source_file: str = DCFileManager.get_config(self.dc_json_config_path)
        target_file: str = os.path.join(
            self.scheme_path, f'{self.scheme}.json'
        )
        source_config: dict = SchemeFileManager.get_json(source_file)
        target_config = {}

        # Attach Style(s) properties
        match self.dark_mode:
            case 1:
                target_config['Styles'] = source_config['Styles']
            case 2:
                target_config['Styles'] = [
                    style for style in source_config['Styles']
                        if style['Name'] == "Dark"
                ]
            case 3:
                target_config['Styles'] = [
                    style for style in source_config['Styles']
                        if style['Name'] == "Light"
                ]
            case _:
                raise ValueError(f'Invalid dark mode value: {self.dark_mode}')

        # Attach FileColors property
        target_config['FileColors'] = source_config['FileColors']

        # Save json scheme file
        SchemeFileManager.set_json(target_config, target_file)

    def create_scheme_xml(self) -> None:
        """
        Creates the scheme specifically from the xml configuration file.
        """
        pass