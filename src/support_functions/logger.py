import logging, json_config, tkinter
from datetime import datetime
from os.path import exists
from os import makedirs
from dataclasses import dataclass
from ntpath import join
from tkinter.scrolledtext import ScrolledText
from queue import Queue

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
        "version" : 1,
        "log_format" : "[%(asctime)s -%(levelname)s] %(name)s - %(message)s",
        "logger_level" : 10,
        "console_level" : 10,
        "gui_level" : 20,
        "file_level" : 20,
        "path" : "Log/",
        "log_name" : "Log_",
        "log_extension" : "log",
        "critical" : 50,
        "error" : 40,
        "warning" : 30,
        "info" : 20,
        "debug" : 10,
        "notset" : 0
    }
    """
    config = json_config.load_json_config('logging_config.json', template)
    logger_config = LogConfig(config['version'], 
                            config['log_format'],
                            config['logger_level'],
                            config['console_level'],
                            config['gui_level'],
                            config['file_level'],
                            config['path'],
                            config['log_name'],
                            config['log_extension'])
except Exception as error:
    print(f'Config loading error {error}')
    exit()


def logger(current_logger=logging.Logger):
    if len(current_logger.handlers) == 0:
        current_date = datetime.strftime(datetime.now().date(), "%Y%m%d")
        formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_config.console_level)
        console_handler.setFormatter(formatter)
        log_file_handler = __new_file_handler(current_date, formatter)
        current_logger.addHandler(console_handler)
        current_logger.addHandler(log_file_handler)
        current_logger.setLevel(logger_config.logger_level)
    return current_logger


def check_change_date(current_logger=logging.Logger):
    current_date = datetime.now().date()
    if not __current_file_handler_date(current_logger) == current_date:
        for logger_handler in current_logger.handlers:
            if isinstance(logger_handler, logging.FileHandler):
                current_date = datetime.strftime(current_date, "%Y%m%d")
                current_logger.handlers.remove(logger_handler)
                formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
                new_log_file_handler = __new_file_handler(current_date, formatter)
                current_logger.addHandler(new_log_file_handler)
    return


def __current_file_handler_date(current_logger=logging.Logger):
    for handler in current_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            current_file_handler = handler.baseFilename
            path_splitted = current_file_handler.replace('\\', '/').split('/')
            file_handler_date = datetime.strptime(path_splitted[-1].split('.')[0].split('_')[1], '%Y%m%d').date()
            print(file_handler_date)
            return file_handler_date


def __new_file_handler(current_date, formatter):
    if not exists(logger_config.path):
        makedirs(logger_config.path)
    log_file_handler = logging.FileHandler(join(logger_config.path, f'{logger_config.log_name}{current_date}.{logger_config.log_extension}'))
    log_file_handler.setLevel(logger_config.file_level)
    log_file_handler.setFormatter(formatter)
    return log_file_handler


def addHanlder(current_logger, handler=logging.Handler):
    return current_logger.addHandler(handler)


def removeHandler(current_logger=logging.Logger, handler=logging.Handler):
    for current_handler in current_logger.handlers:
        if isinstance(current_handler, type(handler)):
            current_logger.handlers.remove(current_handler)


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
        formatter = logging.Formatter(logger_config.log_format, datefmt='%Y/%m/%d %H:%M:%S')
        logging.Handler.setFormatter(self, formatter)
        logging.Handler.setLevel(self, logger_config.gui_level)
        self.log_queue = log_queue

    
    def emit(self, record):
        if self.log_queue.qsize() >= 100:
            self.log_queue.get(block=False)
        self.log_queue.put(self.format(record))