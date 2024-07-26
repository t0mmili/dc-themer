from defusedxml.ElementTree import parse, tostring
from defusedxml.minidom import parseString
from os import listdir, path
from shutil import copy

class Scheme:
    @staticmethod
    def apply_scheme(scheme, scheme_path, dc_config, tags):
        source_file = path.join(scheme_path, scheme)
        target_file = DoubleCommander.get_config(dc_config)

        # Backup current configuration
        copy(target_file, f'{target_file}.backup')

        for item in tags:
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

            # Save modified DC config file
            with open(target_file, 'w', encoding='utf-8') as xml_file:
                xml_file.write(pretty_xml)

    @staticmethod
    def list_schemes(scheme_path, scheme_ext):
        # Check if scheme directory exist
        if not path.exists(scheme_path):
            raise FileNotFoundError('The schemes dir does not exist.')

        # List all files and directories in the specified folder
        entries = listdir(scheme_path)

        # Filter out directories and non-XML files
        xml_files = [entry for entry in entries if path.isfile(path.join(scheme_path, entry)) and entry.endswith(f'.{scheme_ext}')]
 
        return xml_files

class DoubleCommander:
    @staticmethod
    def get_config(dc_config):
      # Define path to DC config file
      config_path = path.join(path.expandvars(dc_config), 'doublecmd.xml')

      # Check if the config file exists
      if path.exists(config_path):
          return config_path
      else:
          raise FileNotFoundError(f'Double Commander config file does not exist:\n{config_path}')