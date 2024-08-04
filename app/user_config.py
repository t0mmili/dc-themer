from json import dump
from json_repair import loads
from os import path
from tkinter.messagebox import showerror

class UserConfigManager:
    def __init__(
        self, default_user_config, user_config_path
    ):
        self.default_user_config = default_user_config
        self.user_config_path = user_config_path

    def exists(self):
        """
        Verifies a user configuration file exists.
        """
        return path.isfile(
            self.user_config_path
        ) and self.user_config_path.endswith('.json')
    
    def create_default(self):
        '''
        Writes a default user configuration json data to file.
        '''
        try:
            with open(
                self.user_config_path, 'w', encoding='utf-8'
            ) as json_file:
                dump(
                    self.default_user_config, json_file, ensure_ascii=False,
                    indent=2
                )
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

    def get_config(self):
        """
        Reads, repairs and parses a json user configuration file.
        """
        try:
            with open(self.user_config_path, 'r') as json_file:
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
    def verify(current_version, read_version):
        """
        Verifies existing user configuration version.
        """
        if read_version != current_version:
            raise RuntimeError(
                'Configuration file version mismatch.\n'
                'Please refer to the release notes for more information about '
                'application configuration breaking changes.'
            )