from configobj import ConfigObj, ConfigObjError
from json import dump
from json_repair import loads
from os import listdir, path
from shutil import copy
from tkinter.messagebox import showerror

class DCFileManager:
    @staticmethod
    def get_config(dc_config):
      # Define path to the config file
      config_path = path.expandvars(dc_config)

      # Check if the config file exists
      if path.exists(config_path):
          return config_path
      else:
          raise FileNotFoundError(f'Double Commander config file does not exist:\n{config_path}')

    @staticmethod
    def backup_config(file):
        try:
            copy(file, f'{file}.backup')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred while backing up the file:\n{str(e)}')

class SchemeFileManager:
    @staticmethod
    def get_cfg(infile):
        try:
            config = ConfigObj(infile)
        except ConfigObjError as e:
            showerror(title='Error', message=f'An error occurred while parsing the configuration file:\n{str(e)}')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred:\n{str(e)}')
        else:
            return config

    @staticmethod
    def set_cfg(config, outfile):
        try:
            with open(outfile, 'w', encoding='utf-8') as cfg_file:
                for key in config:
                    line = f'{key}={config[key]}\n'
                    cfg_file.write(line)
        except IOError as e:
            showerror(title='Error', message=f'An error occurred while writing to the file:\n{str(e)}')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred:\n{str(e)}')

    @staticmethod
    def get_json(infile):
        try:
            with open(infile, 'r') as json_file:
                file_content = json_file.read()
        except IOError as e:
            showerror(title='Error', message=f'An error occurred while reading the file:\n{str(e)}')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred:\n{str(e)}')
        else:
            json_data = loads(file_content)

            return json_data

    @staticmethod
    def set_json(json_data, outfile):
        try:
            with open(outfile, 'w', encoding='utf-8') as json_file:
                dump(json_data, json_file, ensure_ascii=False, indent=2)
        except IOError as e:
            showerror(title='Error', message=f'An error occurred while writing to the file:\n{str(e)}')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred:\n{str(e)}')

    @staticmethod
    def set_xml(xml_data, outfile):
        try:
            with open(outfile, 'w', encoding='utf-8') as xml_file:
                xml_file.write(xml_data)
        except IOError as e:
            showerror(title='Error', message=f'An error occurred while writing to the file:\n{str(e)}')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred:\n{str(e)}')

    @staticmethod
    def list_schemes(scheme_path, scheme_exts):
        # Verify the existence of the scheme directory
        if not path.exists(scheme_path):
            raise FileNotFoundError(f'The schemes directory does not exist: {scheme_path}')

        # Retrieve all files in the directory
        files = [file for file in listdir(scheme_path) if path.isfile(path.join(scheme_path, file))]

        # Create a dictionary to group files by scheme name
        scheme_files = {}
        for file in files:
            name, ext = path.splitext(file)
            if ext[1:] in scheme_exts:   # Remove dot from extension
                if name not in scheme_files:
                    scheme_files[name] = []
                scheme_files[name].append(ext[1:])

        # Validate that each scheme has all required extensions
        missing_files = {}
        for name, ext in scheme_files.items():
            missing_extensions = set(scheme_exts) - set(ext)
            if missing_extensions:
                missing_files[name] = [f'{name}.{ext}' for ext in missing_extensions]

        # Throw an error if any missing files are found
        if missing_files:
            error_message = 'Missing required scheme files:\n'
            for name, files in missing_files.items():
                error_message += f'\'{name}\' expected files {files}\n'
            raise FileNotFoundError(error_message)

        return sorted(scheme_files.keys())