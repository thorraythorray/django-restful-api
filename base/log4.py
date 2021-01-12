import logging
import os 
from etc.sys_config import LOG_PATH
from helper.log4 import logger

class log4(logger):
    def __init__(self):
        self.log_level = logging.INFO
        self.log_path_suffix = 'base.log'
        self.log_name = "alphax:base"

log4app = log4().log() 