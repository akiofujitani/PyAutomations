from time import sleep
import file_handler, json_config, datetime, tkinter, os, threading
import logger as log
from dataclasses import dataclass
from os.path import normpath, abspath
from os.path import split as path_split
from queue import Queue

logger = log.logger('file_mover_backup')

@dataclass
class Move_Settings:
    source: str
    destination: str
    extention: str
    days_from_today: int
    copy: bool 

@dataclass
class Configuration_Values:
    wait_time: int
    file_per_cicle: int
    month_name_list: list
    directory_list: list


    def min_to_seconds(self) -> int:
        return self.wait_time * 60


class ThreadEventException(Exception):
    '''Thread event exception'''
    pass


class Main_App(tkinter.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title('VCA Bot Volpe Mid')
        self.minsize(width=500, height=500)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_columnconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1, minsize=50)
        self.grid_columnconfigure(3, weight=0, minsize=50)

        start_button = tkinter.Button(self, text='Start', command=self.__click_button_start, width=25)
        start_button.grid(column=0, row=0, padx=(3), pady=(3), sticky='nesw')

        stop_button = tkinter.Button(self, text='Stop', command=self.__click_button_stop, width=25)
        stop_button.grid(column=1, row=0, padx=(3), pady=(3), sticky='nesw')

        config_button = tkinter.Button(self, text='Configuration', command=self.__click_button_config, width=25)
        config_button.grid(column=3, row=0, padx=(3), pady=(3), sticky='nesw')

        self.scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        self.scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        self.scrolled_text.grid(column=0, row=1, columnspan=4, sticky='nesw', padx=(3), pady=(3))
        self.log_queue = logger.queue_handler.log_queue
        self.after(100, self.poll_log_queue)


    def display(self, message):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tkinter.END, f'{message}\n')
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview(tkinter.END)  


    def poll_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get(block=False)
            self.display(message)
        self.after(100, self.poll_log_queue)


    def __click_button_start(self):
        logger.debug('Button start clicked')
        thread = threading.Thread(target=main, args=(event,), name='File_Mover')
        thread.start()


    def __click_button_stop(self):
        logger.debug('Button stop clicked')
        event.set()


    def __click_button_config(self):
        logger.debug('Button config clicked')


def __load_configuration(config_path=str) -> dict:
    try:
        config_template = """{
        "wait_time_min" : 15,
        "files_per_cicle" : 1500,
        "month_name" : [
            "01 January",
            "02 February",
            "03 March",
            "04 April",
            "05 May",
            "06 June",
            "07 July",
            "08 August",
            "09 September",
            "10 October",
            "11 November",
            "12 December"
            ],
            "directory_list" : [
                {
                    "source" : "./Source",
                    "destin" : "./Destin",
                    "extension" : "",
                    "days_from_today" : 0,
                    "copy" : "False"
                }
            ]
        }"""
        config = json_config.load_json_config(config_path, config_template)
        return Configuration_Values(int(config['wait_time_min']),
                int(config['files_per_cicle']),
                config['month_name'], 
                [Move_Settings(normpath(item['source']), 
                        normpath(item['destin']),
                        item['extension'],
                        int(item['days_from_today']),
                        eval(item['copy'])) for item in config['directory_list']])
    except Exception as error:
        logger.critical(f'Error loading configuration file. {error}')
        sleep(3)
        quit()


def main(event=threading.Event):
    config = __load_configuration('file_mover_backup.json')

    while True:
        for move_settings in config.directory_list:
            try:
                if event.is_set():
                    raise ThreadEventException('Event set')
                logger.debug(f'Listing files from {move_settings.source}')
                file_list = file_handler.listFilesInDirSubDir(move_settings.source, move_settings.extention)
                if len(file_list) > 0:
                    counter = 0
                    for file in file_list:
                        file_last_modification = file_handler.fileCreationDate(file)
                        if datetime.datetime.today().date() - datetime.timedelta(days=move_settings.days_from_today) > file_last_modification:
                            file_destination = f'{move_settings.destination}/{file_last_modification.year}/{config.month_name_list[int(file_last_modification.month) - 1]}/{"{:02d}".format(file_last_modification.day)}'
                            file_destination_path = normpath(file_destination)
                            source_path, file_name = path_split(abspath(file))
                            file_handler.file_move_copy(source_path, file_destination_path, file_name, move_settings.copy, True)
                        counter += 1
                        if counter >= config.file_per_cicle:
                            logger.info(f'Number {config.file_per_cicle} of files per cicle reached.')
                            logger.info(f'From {source_path} to {file_destination_path}')
                            break
                        if event.is_set():
                            logger.info(f'Counter at {counter}')
                            logger.info(f'Moving from {source_path} to {file_destination_path}')
                            raise ThreadEventException('Event set')
            except ThreadEventException as thread_end:
                logger.info('Thread finalized')
                event.clear()
                return
            except Exception as error:
                logger.warning(f'Error processing files {error}')
        logger.info(f'Waiting ... {config.min_to_seconds()}')
        sleep(config.min_to_seconds())


if __name__ == '__main__':
    event = threading.Event()
    thread = threading.Thread(target=main, args=(event,), name='File_Mover')
    thread.start()
    window = Main_App()
    window.mainloop()
    thread.join()

