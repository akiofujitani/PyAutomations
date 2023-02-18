import logging, json_config, tkinter
from datetime import datetime
from os.path import exists, abspath, splitext
from os import makedirs
from dataclasses import dataclass
from ntpath import join
from tkinter.scrolledtext import ScrolledText
from queue import Queue
from logging.config import dictConfig

@dataclass
class LogConfig:
    version : int
    log_format : str
    logger_level : int
    console_level : int
    gui_level : int
    file_level : int
    path : str
    log_name : str
    log_extension : str


try:
    template = """{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "brief": {
            "format" : "[%(asctime)s - %(levelname)s] %(name)-12s %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S"
        },
        "precise": {
            "format": "[%(asctime)s - %(levelname)s] %(name)-12s %(funcName)-30s %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "brief",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "file_handler": {
            "class" : "logger.TimeStampedFileHandler",
            "formatter" : "precise",
            "level" : "DEBUG",
            "filename" : "./Log/Log.log"
        },
        "queue_handler" : {
            "class" : "logger.LogQueuer",
            "formatter" : "brief",
            "level" : "DEBUG"
        }
    },
    "root": {
        "handlers": [
            "console", "file_handler", "queue_handler"
        ],
        "level": "DEBUG"
    }
}"""
    config = json_config.load_json_config('logger_config.json', template)
except Exception as error:
    print(f'Config loading error {error}')
    exit()


def logger_setup(logger=logging.Logger | None, log_queue=Queue | None):
    dictConfig(config)
    if not logger == None:
        # logger = add_log_queuer(logger, log_queue)
        logger = add_handler(logger, LogQueuer, log_queue)


# def logger(current_logger=logging.Logger):
#     if len(current_logger.handlers) == 0:
#         current_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
#         formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logger_config.console_level)
#         console_handler.setFormatter(formatter)
#         log_file_handler = __new_file_handler(current_date, formatter)
#         current_logger.addHandler(console_handler)
#         current_logger.addHandler(log_file_handler)
#         current_logger.setLevel(logger_config.logger_level)
#     return current_logger


# def check_change_date(current_logger=logging.Logger):
#     current_date = datetime.now().date()
#     if not __current_file_handler_date(current_logger) == current_date:
#         for logger_handler in current_logger.handlers:
#             if isinstance(logger_handler, logging.FileHandler):
#                 current_date = datetime.strftime(current_date, "%Y%m%d")
#                 current_logger.handlers.remove(logger_handler)
#                 formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
#                 new_log_file_handler = __new_file_handler(current_date, formatter)
#                 current_logger.addHandler(new_log_file_handler)
#     return


# def __current_file_handler_date(current_logger=logging.Logger):
#     for handler in current_logger.handlers:
#         if isinstance(handler, logging.FileHandler):
#             current_file_handler = handler.baseFilename
#             path_splitted = current_file_handler.replace('\\', '/').split('/')
#             file_handler_date = datetime.strptime(path_splitted[-1].split('.')[0].split('_')[1], '%Y%m%d').date()
#             print(file_handler_date)
#             return file_handler_date


# def __new_file_handler(current_date, formatter):
#     if not exists(logger_config.path):
#         makedirs(logger_config.path)
#     log_file_handler = logging.FileHandler(join(logger_config.path, f'{logger_config.log_name}{current_date}.{logger_config.log_extension}'))
#     log_file_handler.setLevel(logger_config.file_level)
#     log_file_handler.setFormatter(formatter)
#     return log_file_handler


# def addHanlder(current_logger, handler=logging.Handler):
#     return current_logger.addHandler(handler)


# def removeHandler(current_logger=logging.Logger, handler=logging.Handler):
#     for current_handler in current_logger.handlers:
#         if isinstance(current_handler, type(handler)):
#             current_logger.handlers.remove(current_handler)


# class logger:
#     def __init__(self, current_logger=logging.Logger | None) -> None:
#         self.current_logger = current_logger
#         if len(self.current_logger.handlers) == 0:
#             self.current_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
#             self.formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
#             self.console_handler = logging.StreamHandler()
#             self.console_handler.setLevel(logger_config.console_level)
#             self.console_handler.setFormatter(self.formatter)
#             self.log_file_handler = self.__new_file_handler()

#             self.current_logger.addHandler(self.console_handler)
#             self.current_logger.addHandler(self.log_file_handler)
#             self.current_logger.setLevel(logger_config.logger_level)


#     def critical(self, message=str):
#         self.__check_change_date()
#         self.current_logger.critical(message)
    

#     def error(self, message=str):
#         self.__check_change_date()
#         self.current_logger.error(message)

    
#     def warning(self, message=str):
#         self.__check_change_date()
#         self.current_logger.warning(message)
    

#     def info(self, message=str):
#         self.__check_change_date()
#         self.current_logger.info(message)
    

#     def debug(self, message=str):
#         self.__check_change_date()
#         self.current_logger.debug(message)


#     def __check_change_date(self):
#         if not self.current_date == datetime.strftime(datetime.now().date(), "%Y%m%d"):
#             for logger_handler in self.current_logger.handlers:
#                 if isinstance(logger_handler, logging.FileHandler):
#                     self.current_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
#                     self.current_logger.handlers.remove(logger_handler)
#                     self.new_log_file_handler = self.__new_file_handler()
#                     self.current_logger.addHandler(self.new_log_file_handler)
    

#     def __new_file_handler(self):
#         if not exists(logger_config.path):
#             makedirs(logger_config.path)
#         self.log_file_handler = logging.FileHandler(join(logger_config.path, f'{logger_config.log_name}{self.current_date}.{logger_config.log_extension}'))
#         self.log_file_handler.setLevel(logger_config.file_level)
#         self.log_file_handler.setFormatter(self.formatter)
#         return self.log_file_handler


#     def addHandler(self, handler=logging.Handler):
#         self.current_logger.addHandler(handler)


#     def removeHandler(self, handler_class):
#         for handler in self.current_logger.handlers:
#             if isinstance(handler, handler_class):
#                 self.current_logger.handlers.remove(handler)
#         return
def add_handler(current_logger=logging.Logger, handler_class=logging.Handler, log_queue=None | Queue):
    formatter =''
    level = ''
    for handler in current_logger.handlers:
        if isinstance(handler, handler_class):
            formatter = handler.formatter
            level = handler.level
            current_logger.handlers.remove(handler)
    if not formatter and not level:
        formatter = current_logger.handlers[0].formatter
        level = current_logger.handlers[0].level
    if log_queue == None:
        log_handler = handler_class()
    else:
        log_handler = handler_class(log_queue)
    log_handler.setFormatter(formatter)
    log_handler.setLevel(level)
    current_logger.handlers.append(log_handler)
    return current_logger


def add_log_queuer(current_logger=logging.Logger, log_queue=Queue()):
    formatter =''
    level = ''
    for handler in current_logger.handlers:
        if isinstance(handler, LogQueuer):
            formatter = handler.formatter
            level = handler.level
            current_logger.handlers.remove(handler)
    if not formatter and not level:
        formatter = current_logger.handlers[0].formatter
        level = current_logger.handlers[0].level
    log_handler = LogQueuer(log_queue)
    log_handler.setFormatter(formatter)
    log_handler.setLevel(level)
    current_logger.handlers.append(log_handler)
    return current_logger
    

class TextHandler(logging.Handler):
    def __init__(self, text=ScrolledText):
        logging.Handler.__init__(self)
        formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
        logging.Handler.setFormatter(self, formatter)
        logging.Handler.setLevel(self, logger_config.gui_level)
        self.text = text
    

    def emit(self, record):
        message = self.format(record)
        def append():
            self.text.configure(state='normal')
            line_count = int(float(self.text.index('end')))
            if line_count > 300:
                self.text.delete('1.0', str("{:0.1f}".format(line_count - 299)))
            self.text.insert(tkinter.END, f'{message}\n')
            self.text.configure(state='disabled')
            self.text.yview(tkinter.END)        
        self.text.after(0, append)    

class LogQueuer(logging.Handler):
    def __init__(self, log_queue=Queue()) -> None:
        logging.Handler.__init__(self)
        self.log_queue = log_queue

    
    def emit(self, record):
        if self.log_queue.qsize() >= 100:
            self.log_queue.get(block=False)
        self.log_queue.put(self.format(record))


class TimeStampedFileHandler(logging.FileHandler):
    def __init__(self, filename: str, mode: str = "a", encoding: str | None = None, delay: bool = False, errors: str | None = None) -> None:
        filename, extension = splitext(filename)
        filename = abspath(f'{filename}_{datetime.strftime(datetime.now().date(), "%Y%m%d")}{extension}')
        super().__init__(filename, mode, encoding, delay, errors)


if __name__ == '__main__':
    logger_setup()
    loggers = logging.getLogger()

    loggers.debug('Test')
    loggers.info('Done')