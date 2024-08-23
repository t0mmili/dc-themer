from json import dump
from json_repair import loads
from os import path

class UserConfigManager:
    """
    Manages the user configuration for the application.

    Attributes:
        default_user_config (dict): The default configuration settings.
        user_config_path (str): The file path for the user configuration file.
    """
    def __init__(
        self, default_user_config: dict, user_config_path: str
    ) -> None:
        self.default_user_config: dict = default_user_config
        self.user_config_path: str = user_config_path

    def exists(self) -> bool:
        """
        Checks if the user configuration file exists and is a json file.

        Returns:
            bool: True if the file exists and is a json file, False otherwise.
        """
        return path.isfile(
            self.user_config_path
        ) and self.user_config_path.endswith('.json')

    def create_default(self) -> None:
        """
        Creates a default user configuration file from the provided default
        data.

        Raises:
            OSError: If an error occurs while writing to the file.
        """
        try:
            with open(
                self.user_config_path, 'w', encoding='utf-8'
            ) as json_file:
                dump(
                    self.default_user_config, json_file, ensure_ascii=False,
                    indent=2
                )
        except OSError as e:
            raise OSError(
                'Failed to write default configuration to '
                f'{self.user_config_path}:\n{str(e)}'
            )

    @staticmethod
    def get_config(infile) -> dict:
        """
        Reads the user configuration file, repairs it if necessary, and parses
        the json data.

        Returns:
            dict: The parsed json data from the configuration file.

        Raises:
            OSError: If an error occurs while reading the file.
            TypeError: If file does not contain valid json object data.
        """
        try:
            with open(infile, 'r') as json_file:
                file_content = json_file.read()
            json_data = loads(file_content)

            # Ensure json_data is a dictionary
            if not isinstance(json_data, dict):
                raise TypeError(
                    f'The configuration file {infile} does not contain valid '
                    'json object data.'
                )
 
            return json_data
        except OSError as e:
            raise OSError(
                f'Failed to read configuration from {infile}:\n{str(e)}'
            )

    @staticmethod
    def verify(current_version, read_version) -> None:
        """
        Checks if the existing user configuration version matches the expected
        version.

        Args:
            current_version (str): The expected version of the configuration.
            read_version (str): The version read from the configuration file.

        Raises:
            RuntimeError: If there is a version mismatch between the current
                          and read version.
        """
        if read_version != current_version:
            raise RuntimeError(
                'Configuration file version mismatch.\n'
                'Please refer to the release notes for more information about '
                'application configuration breaking changes.'
            )