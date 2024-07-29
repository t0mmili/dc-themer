from configobj import ConfigObj
from defusedxml.ElementTree import parse, tostring
from defusedxml.minidom import parseString
from os import listdir, path
from shutil import copy

class Scheme:
    def __init__(self, scheme, scheme_path, dc_configs, xml_tags):
        self.scheme = scheme
        self.scheme_path = scheme_path
        self.dc_configs = dc_configs
        self.xml_tags = xml_tags

    def apply_scheme(self):
        # self.apply_scheme_cfg()
        self.apply_scheme_json()
        # self.apply_scheme_xml()

    def apply_scheme_cfg(self):
        source_file = path.join(self.scheme_path, f'{self.scheme}.cfg')
        target_file = DoubleCommander.get_config(self.dc_configs['cfg'])
        source_config = self.get_cfg(source_file)
        target_config = self.get_cfg(target_file)

        # Set new 'DarkMode' value
        target_config['DarkMode'] = source_config['DarkMode']

        # Backup current configuration
        copy(target_file, f'{target_file}.backup')

        # Save modified DC cfg file
        self.set_cfg(target_config, target_file)

    def apply_scheme_json(self):
        source_file = path.join(self.scheme_path, f'{self.scheme}.json')
        target_file = DoubleCommander.get_config(self.dc_configs['json'])

    def apply_scheme_xml(self):
        source_file = path.join(self.scheme_path, f'{self.scheme}.xml')
        target_file = DoubleCommander.get_config(self.dc_configs['xml'])

        # Backup current configuration
        copy(target_file, f'{target_file}.backup')

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
            with open(target_file, 'w', encoding='utf-8') as xml_file:
                xml_file.write(pretty_xml)

    def get_cfg(self, infile):
        config = ConfigObj(infile)

        return config

    def set_cfg(self, config, outfile):
        with open(outfile, 'w', encoding='utf-8') as cfg_file:
            for key in config:
                line = f'{key}={config[key]}\n'
                cfg_file.write(line)

    @staticmethod
    def list_schemes(scheme_path, scheme_exts):
        # Check if scheme directory exist
        if not path.exists(scheme_path):
            raise FileNotFoundError(f'The schemes dir does not exist:\n{scheme_path}')

        # List all files and directories in the specified folder
        files = listdir(scheme_path)

        # Extract scheme names by removing extensions
        scheme_names = set(path.splitext(file)[0] for file in files)

        # Check if each unique name has all required files
        for name in scheme_names:
            expected_files = set()

            for ext in scheme_exts:
                expected_files.add(f'{name}.{ext}')

            if not expected_files.issubset(files):
                raise FileNotFoundError(f'Missing required files for {name} scheme.\nExpected files: {expected_files}')

        return sorted(list(scheme_names))

class DoubleCommander:
    @staticmethod
    def get_config(dc_config):
      # Define path to DC config file
      config_path = path.expandvars(dc_config)

      # Check if the config file exists
      if path.exists(config_path):
          return config_path
      else:
          raise FileNotFoundError(f'Double Commander config file does not exist:\n{config_path}')