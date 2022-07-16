"""Common utility function for application are placed here."""

import json
import os
from script.constants import LOGGER, CFG_DIR, CFG_FILE, HBATCH_LOCATION
from script.ui_utils import FileBrowser


def get_config_data():
    """Read configuration file.

    Returns:
        dict: Returns dictionary data from configuration file.
    """

    if os.path.exists(CFG_FILE):
        with open(CFG_FILE, 'r') as cfg_read:
            config_data = json.load(cfg_read)
            return config_data
    return None


def check_configs():
    """Performs check for configuration file.
    If not exists then new one will be created.

    Returns:
        dict: Returns dictionary data from configuration file.
    """
    if not os.path.exists(CFG_DIR):
        LOGGER.debug('Configuration directory not found. Creating new one ...')
        os.makedirs(CFG_DIR)

    if not os.path.exists(CFG_FILE):
        LOGGER.debug('Configuration file missing. Generating new one ...')
        with open(CFG_FILE, 'w+') as write_cfg:
            _app_data = {
                "houdini_installed_directory": ""
            }
            json.dump(_app_data, write_cfg, indent=4)
        LOGGER.debug('Configuration file generated successfully.')

    with open(CFG_FILE, 'r') as read_cfg:
        config_data = json.load(read_cfg)
        LOGGER.debug('Returning config data : %s', config_data)
        return config_data


def pick_houdini_directory():
    """Fetch application configuration file.

    Returns:
        dict: Returns dictionary data from configuration file.
    """
    pick_directory = FileBrowser(
        caption="Select houdini installed directory"
    )
    pick_directory.show()
    config_path = pick_directory.get_file.path()

    if config_path:
        if os.path.exists(config_path):
            with open(CFG_FILE, 'r') as read_config:
                config_data = json.load(read_config)

            with open(CFG_FILE, 'w+') as write_config:
                hbatch = HBATCH_LOCATION.format(config_path)

                if not os.path.exists(hbatch):
                    return False

                config_data.update(
                    {
                        "houdini_installed_directory": config_path,
                        "hbatch_location": HBATCH_LOCATION.format(config_path),
                        "hou_location": "{}/houdini/python2.7libs/".format(config_path)
                    }
                )

                json.dump(config_data, write_config, indent=4)

                return config_data
        else:
            LOGGER.warning("Directory doesn't exists : %s", config_path)
            return False
    else:
        return False
