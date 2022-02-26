import os
from typing import Dict

from dotenv import load_dotenv

from custom_error import *
from api import API


class Config:
    """
    This class is responsible for loading the configuration from the .env file.
    """

    def __init__(self):
        self.config = self.load_config()
        self.required_keys = ['token', 'azure_url', 'input_folder']
        self.verify_config()

    def load_config(self) -> Dict[str, str]:
        """
        Loads the configuration from the .env file.
        :return: Configuration as a dictionary.
        """
        load_dotenv()

        config = {}
        for key, value in os.environ.items():
            config[key] = value
        return config

    def get_config(self) -> Dict[str, str]:
        """
        Returns the configuration as a dictionary.
        :return: Configuration as a dictionary.
        """
        return self.config

    def get_token(self) -> str:
        """
        Returns the token env from config.
        :return: Token env.
        """
        return self.get_config().get('token') or ''

    def get_azure_url(self) -> str:
        """
        Returns the azure_url env from config.
        :return: azure_url env.
        """
        return self.get_config().get('azure_url') or ''

    def get_input_folder(self) -> str:
        """
        Returns the input folder env from config.
        :return: input_folder env.
        """
        return self.get_config().get('input_folder') or ''

    def verify_config(self) -> Dict[str, str]:
        """
        Verifies the configuration, if any of the required keys are missing, it will throw an error.w
        :return: Configuration as a dictionary.
        """
        config = self.get_config()

        missing_keys = []
        for key in self.required_keys:
            if key not in config:
                missing_keys.append(key)

        if len(missing_keys) > 0:
            raise MissingConfigurationError(
                f"Missing configuration keys: {', '.join(missing_keys)}")

        if (API.check_url(self.get_azure_url()) is False):
            raise AzureUrlError(
                f"Invalid Azure URL: {self.get_azure_url()}")

        return config
