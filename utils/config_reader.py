"""
config_reader.py - Reads configuration from config.ini file
"""

import configparser
import os

class ConfigReader:
    """Singleton class to read configuration from config.ini"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._config = configparser.ConfigParser()
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
            cls._config.read(config_path)
        return cls._instance
    
    @property
    def base_url(self) -> str:
        return self._config.get('settings', 'base_url')
    
    @property
    def browser(self) -> str:
        return self._config.get('settings', 'browser').lower()
    
    @property
    def headless(self) -> bool:
        return self._config.get('settings', 'headless').lower() == 'true'
    
    @property
    def implicit_wait(self) -> int:
        return int(self._config.get('settings', 'implicit_wait'))
    
    @property
    def explicit_wait(self) -> int:
        return int(self._config.get('settings', 'explicit_wait'))
    
    @property
    def valid_username(self) -> str:
        return self._config.get('credentials', 'valid_username')
    
    @property
    def valid_password(self) -> str:
        return self._config.get('credentials', 'valid_password')
    
    @property
    def invalid_username(self) -> str:
        return self._config.get('credentials', 'invalid_username')
    
    @property
    def invalid_password(self) -> str:
        return self._config.get('credentials', 'invalid_password')
    
    @property
    def locked_username(self) -> str:
        return self._config.get('credentials', 'locked_username')
    
    @property
    def screenshot_path(self) -> str:
        return self._config.get('paths', 'screenshot_path')


# Create a single instance for easy import
config = ConfigReader()
