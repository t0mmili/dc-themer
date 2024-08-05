from configobj import ConfigObj, ConfigObjError
from json import dump
from json_repair import loads
from os import listdir, path
from shutil import copy
from tkinter.messagebox import showerror

class DCFileManager:
    """
    Provides static methods for managing DC configuration files.
    """
    @staticmethod
    def get_config(dc_config):
        """
        Retrieves the path to the specified DC configuration file.

        Args:
            dc_config (str): The path to the configuration file.

        Returns:
            str: The absolute path to the configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
        """
        # Define path to the config file
        config_path = path.expandvars(dc_config)

        # Check if the config file exists
        if not path.exists(config_path):
            raise FileNotFoundError(
                'Double Commander configuration file does not exist:'
                f'\n{config_path}'
            )

        return config_path

    @staticmethod
    def backup_config(file):
        """
        Creates a backup of the specified DC configuration file by copying it
        with a '.backup' extension.

        Args:
            file (str): The path to the file to be backed up.

        Raises:
            Exception: If an error occurs during the backup process.
        """
        try:
            copy(file, f'{file}.backup')
        except Exception as e:
            showerror(
                title='Error',
                message=(
                    'An unexpected error occurred while backing up the file:'
                    f'\n{str(e)}'
                )
            )

class SchemeFileManager:
    """
    Provides static methods for managing scheme files in various formats (cfg,
    json, xml).
    """
    @staticmethod
    def get_cfg(infile):
        """
        Reads a cfg configuration file and returns its contents as a ConfigObj.

        Args:
            infile (str): The path to the cfg file.

        Returns:
            ConfigObj: The configuration object.

        Raises:
            ConfigObjError: If an error occurs while parsing the cfg file.
            Exception: If an unexpected error occurs.
        """
        try:
            config = ConfigObj(infile)
        except ConfigObjError as e:
            showerror(
                title='Error',
                message=(
                    'An error occurred while parsing the configuration file:'
                    f'\n{str(e)}'
                )
            )
        except Exception as e:
            showerror(
                title='Error',
                message=f'An unexpected error occurred:\n{str(e)}'
            )
        else:
            return config

    @staticmethod
    def set_cfg(config, outfile):
        """
        Writes a configuration object to a cfg file.

        Args:
            config (ConfigObj): The configuration object to write.
            outfile (str): The path to the output cfg file.

        Raises:
            IOError: If an error occurs while writing to the file.
            Exception: If an unexpected error occurs.
        """
        try:
            with open(outfile, 'w', encoding='utf-8') as cfg_file:
                for key in config:
                    line = f'{key}={config[key]}\n'
                    cfg_file.write(line)
        except IOError as e:
            showerror(
                title='Error',
                message=(
                    f'An error occurred while writing to the file:\n{str(e)}'
                )
            )
        except Exception as e:
            showerror(
                title='Error',
                message=f'An unexpected error occurred:\n{str(e)}'
            )

    @staticmethod
    def get_json(infile):
        """
        Reads, repairs and parses a json configuration file.

        Args:
            infile (str): The path to the json file.

        Returns:
            dict: The parsed json data.

        Raises:
            IOError: If an error occurs while reading the file.
            Exception: If an unexpected error occurs.
        """
        try:
            with open(infile, 'r') as json_file:
                file_content = json_file.read()
        except IOError as e:
            showerror(
                title='Error',
                message=f'An error occurred while reading the file:\n{str(e)}'
            )
        except Exception as e:
            showerror(
                title='Error',
                message=f'An unexpected error occurred:\n{str(e)}'
            )
        else:
            json_data = loads(file_content)

            return json_data

    @staticmethod
    def set_json(json_data, outfile):
        """
        Writes json data to a file.

        Args:
            json_data (dict): The json data to write.
            outfile (str): The path to the output file.

        Raises:
            IOError: If an error occurs while writing to the file.
            Exception: If an unexpected error occurs.
        """
        try:
            with open(outfile, 'w', encoding='utf-8') as json_file:
                dump(json_data, json_file, ensure_ascii=False, indent=2)
        except IOError as e:
            showerror(
                title='Error',
                message=(
                    f'An error occurred while writing to the file:\n{str(e)}'
                )
            )
        except Exception as e:
            showerror(
                title='Error',
                message=f'An unexpected error occurred:\n{str(e)}'
            )

    @staticmethod
    def set_xml(xml_data, outfile):
        """
        Writes xml data to a file.

        Args:
            xml_data (str): The xml data to write.
            outfile (str): The path to the output file.

        Raises:
            IOError: If an error occurs while writing to the file.
            Exception: If an unexpected error occurs.
        """
        try:
            with open(outfile, 'w', encoding='utf-8') as xml_file:
                xml_file.write(xml_data)
        except IOError as e:
            showerror(
                title='Error',
                message=(
                    f'An error occurred while writing to the file:\n{str(e)}'
                )
            )
        except Exception as e:
            showerror(
                title='Error',
                message=f'An unexpected error occurred:\n{str(e)}'
            )

    @staticmethod
    def list_schemes(scheme_path, scheme_exts):
        """
        Lists all available schemes in the specified directory that meet the
        required extensions.

        Args:
            scheme_path (str): The path to the directory containing scheme
                               files.
            scheme_exts (list): A list of required file extensions for each
                                scheme.

        Returns:
            list: A sorted list of available scheme names.

        Raises:
            FileNotFoundError: If the directory does not exist or if required
                               scheme files are missing.
        """
        # Verify the existence of the scheme directory
        if not path.exists(scheme_path):
            raise FileNotFoundError(
                f'The schemes directory does not exist: {scheme_path}'
            )

        # Retrieve all files in the directory
        files = [
            file for file in listdir(scheme_path) if path.isfile(
                path.join(scheme_path, file)
            )
        ]

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
                missing_files[name] = [
                    f'{name}.{ext}' for ext in missing_extensions
                ]

        # Throw an error if any missing files are found
        if missing_files:
            error_message = 'Missing required scheme files:\n'
            for name, files in missing_files.items():
                error_message += f'\'{name}\' expected files {files}\n'
            raise FileNotFoundError(error_message)

        return sorted(scheme_files.keys())