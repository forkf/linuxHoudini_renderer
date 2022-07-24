"""Application constants are defined here."""
import logging
import os.path

logging.basicConfig(
    format="[%(asctime)s - %(filename)s:%(funcName)s()] %(message)s"
)
LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.DEBUG)


HBATCH_LOCATION = "{}/bin/hbatch"


_PATH = os.path.dirname
_JOIN = os.path.join
APP_DIR = _PATH(__file__)
CFG_DIR = _JOIN(APP_DIR, ".config")
print(CFG_DIR)
CFG_FILE = _JOIN(CFG_DIR, 'app_config.json')
