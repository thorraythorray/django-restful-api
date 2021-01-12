import logging
import os 

class logger:
    def __init__(self):
        self.log_path_suffix = ""
        self.log_level = ""
        self.log_name = ""
    def log(self):
        # if not os.path.exists(self.log_path):
        #     os.makedirs(self.log_path)
        logger = logging.getLogger(self.log_name)
        logger.setLevel(level = self.log_level)
        handler = logging.FileHandler(os.path.join(LOG_PATH, self.log_path_suffix))
        formatter = logging.Formatter('[%(levelname)s]%(asctime)s: %(name)s(%(funcName)s) - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger