import os
import sys
import shutil
import json
import configobj
import json_repair

class AppUtils:
    """
    Provides static methods that can be used throughout the application.
    """
    @staticmethod
    def get_asset_path(infile: str) -> str:
        """
        Gets absolute path to the application asset.
        Path will work for dev Python environment and PyInstaller compiled exe.

        Args:
            infile (str): The path to the asset file.

        Returns:
            str: The absolute path to the asset file.
        """
        try:
            base_path: str = sys._MEIPASS
        except Exception:
            base_path: str = (
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )

        return os.path.join(base_path, infile)

class DCFileManager:
    """
    Provides static methods for managing DC configuration files.
    """
    @staticmethod
    def get_config(dc_config: str) -> str:
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
        config_path = os.path.expandvars(dc_config)

        # Check if the config file exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                'Double Commander configuration file does not exist: '
                f'{config_path}'
            )

        return config_path

    @staticmethod
    def backup_config(file: str) -> None:
        """
        Creates a backup of the specified DC configuration file by copying it
        with a '.backup' extension.

        Args:
            file (str): The path to the file to be backed up.

        Raises:
            OSError: If an error occurs during the backup process.
        """
        try:
            shutil.copy(file, f'{file}.backup')
        except Exception as e:
            raise OSError(
                f'Failed to create backup.\n\n{str(e)}'
            ) from e

class SchemeFileManager:
    """
    Provides static methods for managing scheme files in various formats (cfg,
    json, xml).
    """
    @staticmethod
    def get_cfg(infile: str) -> configobj.ConfigObj:
        """
        Reads a cfg configuration file and returns its contents as a ConfigObj.

        Args:
            infile (str): The path to the cfg file.

        Returns:
            ConfigObj: The configuration object.

        Raises:
            ConfigObjError: If an error occurs while parsing the cfg file.
        """
        try:
            config = configobj.ConfigObj(infile)

            return config
        except configobj.ConfigObjError as e:
            raise configobj.ConfigObjError(
                f'Failed to parse the configuration.\n\n{str(e)}'
            ) from e

    @staticmethod
    def set_cfg(config: configobj.ConfigObj, outfile: str) -> None:
        """
        Writes a configuration object to a cfg file.

        Args:
            config (ConfigObj): The configuration object to write.
            outfile (str): The path to the output cfg file.

        Raises:
            OSError: If an error occurs while writing to the file.
        """
        try:
            with open(outfile, 'w', encoding='utf-8') as cfg_file:
                for key in config:
                    line = f'{key}={config[key]}\n'
                    cfg_file.write(line)
        except Exception as e:
            raise OSError(
                f'Failed to write configuration.\n\n{str(e)}'
            ) from e

    @staticmethod
    def get_json(infile: str) -> dict:
        """
        Reads, repairs and parses a json configuration file.

        Args:
            infile (str): The path to the json file.

        Returns:
            dict: The parsed json data.

        Raises:
            OSError: If an error occurs while reading the file.
            TypeError: If file does not contain valid json object data.
        """
        try:
            with open(infile, 'r') as json_file:
                file_content = json_file.read()
            json_data = json_repair.loads(file_content)

            # Ensure json_data is a dictionary
            if not isinstance(json_data, dict):
                raise TypeError(
                    'The configuration file {infile} does not contain valid '
                    'json object data.'
                )
 
            return json_data
        except Exception as e:
            raise OSError(
                f'Failed to read configuration.\n\n{str(e)}'
            ) from e

    @staticmethod
    def set_json(json_data: dict, outfile: str) -> None:
        """
        Writes json data to a file.

        Args:
            json_data (dict): The json data to write.
            outfile (str): The path to the output file.

        Raises:
            OSError: If an error occurs while writing to the file.
        """
        try:
            with open(outfile, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=2)
        except Exception as e:
            raise OSError(
                f'Failed to write configuration.\n\n{str(e)}'
            ) from e

    @staticmethod
    def set_xml(xml_data: str, outfile: str) -> None:
        """
        Writes xml data to a file.

        Args:
            xml_data (str): The xml data to write.
            outfile (str): The path to the output file.

        Raises:
            OSError: If an error occurs while writing to the file.
        """
        try:
            with open(outfile, 'w', encoding='utf-8') as xml_file:
                xml_file.write(xml_data)
        except Exception as e:
            raise OSError(
                f'Failed to write configuration.\n\n{str(e)}'
            ) from e

    @staticmethod
    def list_schemes(scheme_path: str, scheme_exts: list[str]) -> list[str]:
        """
        Lists all available schemes in the specified directory that meet the
        required extensions.

        Args:
            scheme_path (str): The path to the directory containing scheme
                               files.
            scheme_exts (list[str]): A list of required file extensions for
                                     each scheme.

        Returns:
            list[str]: A sorted list of available scheme names.

        Raises:
            FileNotFoundError: If the directory does not exist or required
                               files are missing.
        """
        # Verify the existence of the scheme directory
        if not os.path.exists(scheme_path):
            raise FileNotFoundError(
                f'The schemes directory does not exist: {scheme_path}'
            )

        # Retrieve all files in the directory
        files = [
            file for file in os.listdir(scheme_path) if os.path.isfile(
                os.path.join(scheme_path, file)
            )
        ]

        # Create a dictionary to group files by scheme name
        scheme_files = {}
        for file in files:
            name, ext = os.path.splitext(file)
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