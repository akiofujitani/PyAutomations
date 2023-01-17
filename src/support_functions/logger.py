from dataclasses import dataclass
from ntpath import join
import logging, json_config
from datetime import datetime


@dataclass
class LogConfig:
    version : int
    log_format : str
    console_level : str
    file_level : str
    path : str
    log_name : str
    log_extension : str


class LoggerDemoConsole():
    def __init__(self, log_config=LogConfig) -> None:
        self.formatter = logging.Formatter(log_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

        # Console logging
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

        # File logging
        self.file_handler = logging.FileHandler(join(log_config.path, f'{log_config.log_name}{datetime.strftime(datetime.now().date(), "%Y%m%d")}.{log_config.log_extension}'))
        self.file_handler.setLevel(log_config.file_level)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)


    def getLogger(self):
        self.logger = logging.getLogger(__name__)


    def debug(self, msg=str):
        self.logger.debug(msg)
    

    def info(self, msg=str):
        self.logger.info(msg)
    

    def warning(self, msg=str):
        self.logger.warning(msg)
    

    def error(self, msg=str):
        self.logger.error(msg)
    

    def critical(self, msg=str):
        self.logger.critical(msg)


def logger():
    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/logging_config.json')
    except Exception as error:
        print('Config loading error {error}')
        exit()
    logger = LogConfig(config['version'], 
                        config['log_format'],
                        config['console_level'],
                        config['file_level'],
                        config['path'],
                        config['log_name'],
                        config['log_extension'])
    return LoggerDemoConsole(logger)


if __name__ == '__main__':

    demo = logger()
    demo.info('test')
