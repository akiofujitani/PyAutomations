from dataclasses import dataclass
from ntpath import join
import logging, json_config
from datetime import datetime


@dataclass
class LogConfig:
    version : int
    log_format : str
    logger_level : int
    console_level : int
    file_level : int
    path : str
    log_name : str
    log_extension : str


def logger(module_name = __name__):
    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/logging_config.json')
    except Exception as error:
        print(f'Config loading error {error}')
        exit()
    logger_config = LogConfig(config['version'], 
                        config['log_format'],
                        config['logger_level'],
                        config['console_level'],
                        config['file_level'],
                        config['path'],
                        config['log_name'],
                        config['log_extension'])


    formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_config.console_level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(join(logger_config.path, f'{logger_config.log_name}{datetime.strftime(datetime.now().date(), "%Y%m%d")}.{logger_config.log_extension}'))
    file_handler.setLevel(logger_config.file_level)
    file_handler.setFormatter(formatter)

    current_logger = logging.getLogger(module_name)
    current_logger.addHandler(console_handler)
    current_logger.addHandler(file_handler)
    current_logger.setLevel(logger_config.logger_level)

    return current_logger


if __name__ == '__main__':
    demo = logger(__name__)
    demo.warning('warning')
    demo.info('info')
    print('Done')

