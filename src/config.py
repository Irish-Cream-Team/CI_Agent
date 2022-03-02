import os
from typing import Dict

from dotenv import load_dotenv

from custom_error import *


class Config:
    """
    This class is responsible for loading the configuration from the .env file.
    """

    @staticmethod
    def _load_config() -> Dict[str, str]:
        """
        Loads the configuration from the .env file.
        :return: Configuration as a dictionary.
        """
        load_dotenv()
        config = {}
        for key, value in os.environ.items():
            config[key] = value
        
        Config.verify_config(config)
        return config

    @staticmethod
    def get_config() -> Dict[str, str]:
        """
        Returns the configuration as a dictionary.
        :return: Configuration as a dictionary.
        """
        return Config._load_config()

    @staticmethod
    def get_token(config: Dict[str, str]) -> str:
        """
        Returns the token env from config.
        :return: Token env.
        """
        return config['token']

    @staticmethod
    def get_azure_url(config: Dict[str, str]) -> str:
        """
        Returns the azure_url env from config.
        :return: azure_url env.
        """
        return config.get('azure_url') or ''

    @staticmethod
    def get_input_folder(config: Dict[str, str]) -> str:
        """
        Returns the input folder env from config.
        :return: input_folder env.
        """
        return config.get('input_folder') or ''

    @staticmethod
    def verify_config(config: Dict[str, str]) -> Dict[str, str]:
        """
        Verifies the configuration, if any of the required keys are missing, it will throw an error.w
        :return: Configuration as a dictionary.
        """
        required_keys = ['token', 'azure_url', 'input_folder']

        missing_keys = []
        for key in required_keys:
            if key not in config:
                missing_keys.append(key)

        if len(missing_keys) > 0:
            raise MissingConfigurationError(
                f"Missing configuration keys: {', '.join(missing_keys)}")
        return config
