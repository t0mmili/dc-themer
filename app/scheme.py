from defusedxml.ElementTree import parse, tostring
from defusedxml.minidom import parseString
from os import path
from utils import DCFileManager, SchemeFileManager

class Scheme:
    def __init__(self, scheme, scheme_path, dc_configs, auto_dark_mode, xml_tags):
        self.scheme = scheme
        self.scheme_path = scheme_path
        self.dc_configs = dc_configs
        self.auto_dark_mode = auto_dark_mode
        self.xml_tags = xml_tags

    def apply_scheme(self):
        self.apply_scheme_cfg()
        self.apply_scheme_json()
        self.apply_scheme_xml()

    def apply_scheme_cfg(self):
        source_file = path.join(self.scheme_path, f'{self.scheme}.cfg')
        target_file = DCFileManager.get_config(self.dc_configs['cfg'])
        source_config = SchemeFileManager.get_cfg(source_file)
        target_config = SchemeFileManager.get_cfg(target_file)

        # Set new 'DarkMode' value
        target_config['DarkMode'] = '1' if self.auto_dark_mode else source_config['DarkMode']

        # Backup current configuration
        DCFileManager.backup_config(target_file)

        # Save modified DC cfg config file
        SchemeFileManager.set_cfg(target_config, target_file)

    def apply_scheme_json(self):
        source_file = path.join(self.scheme_path, f'{self.scheme}.json')
        target_file = DCFileManager.get_config(self.dc_configs['json'])
        source_config = SchemeFileManager.get_json(source_file)
        target_config = SchemeFileManager.get_json(target_file)

        # Backup current configuration
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

    def apply_scheme_xml(self):
        source_file = path.join(self.scheme_path, f'{self.scheme}.xml')
        target_file = DCFileManager.get_config(self.dc_configs['xml'])

        # Backup current configuration
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
            target_root.remove(target_tag)
            target_root.append(source_tag)

            # Prettify XML
            xml_str = tostring(target_root, encoding='utf-8')
            dom = parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent='  ')
            pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

            # Save modified DC xml config file
            SchemeFileManager.set_xml(pretty_xml, target_file)