import logging

from app import init_log_config

init_log_config()
logging.info("info")
logging.error("error")
logging.critical("critical")
logging.debug("debug")
