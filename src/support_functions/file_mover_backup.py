from time import sleep
import file_handler, json_config, datetime, tkinter, threading, sys
import logger as log
from dataclasses import dataclass
from os.path import normpath, abspath
from os.path import split as path_split
from tkinter import messagebox

logger = log.logger('file_mover_backup')

@dataclass
class Move_Settings:
    source: str
    destination: str
    extention: str
    days_from_today: int
    copy: bool


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['source'] = self.source.replace('\\', '/')
        values_dict['destination'] = self.destination.replace('\\', '/')
        values_dict['extention'] = self.extention
        values_dict['days_from_today'] = self.days_from_today
        values_dict['copy'] = self.copy
        return values_dict

@dataclass
class Configuration_Values:
    wait_time: int
    file_per_cicle: int
    month_name_list: list
    directory_list: list


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['wait_time'] = self.wait_time
        values_dict['files_per_cicle'] = self.file_per_cicle
        values_dict['month_name_list'] = self.month_name_list
        values_dict['directory_list'] = [directory_value.convert_to_dict() for directory_value in self.directory_list]
        return values_dict


    def directory_list_add(self, move_settings=Move_Settings) -> None:
        self.directory_list.append(move_settings)


    def min_to_seconds(self) -> int:
        return self.wait_time * 60


class ThreadEventException(Exception):
    '''Thread event exception'''
    pass

class Main_App(tkinter.Tk):
    def __init__(self, title=str, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title(title)
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

        scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        scrolled_text.grid(column=0, row=1, columnspan=4, sticky='nesw', padx=(3), pady=(3))
        logger.addHanlder(log.TextHandler(scrolled_text))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)


    def __click_button_start(self):
        logger.debug('Button start clicked')
        if event.is_set():
            thread = threading.Thread(target=main, args=(event,), daemon=True,  name='File_Mover')
            thread.start()
            event.clear()


    def __click_button_stop(self):
        logger.debug('Button stop clicked')
        event.set()


    def __click_button_config(self):
        logger.debug('Button config clicked')


    def __on_window_close(self):
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            event.set()
            logger.info('Forcing kill thread if it is open')
            self.destroy()
            sys.exit()


def __load_configuration(config_path=str) -> dict:
    '''
    Load configuration from .json file. If json file do not exists it will be created using the template values.
    '''
    try:
        config_template = """{
        "wait_time" : 15,
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
                    "copy" : False
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
                logger.info(f'Listing files from {move_settings.source}')
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
                            logger.debug(f'File {counter} "{file_name}" moved')
                            logger.debug(f'From "{source_path}" to "{file_destination_path}"')
                        counter += 1
                        if counter >= config.file_per_cicle:
                            logger.info(f'Number {config.file_per_cicle} of files per cicle reached.')
                            break
                        if event.is_set():
                            logger.info(f'Counter at {counter}')
                            logger.info(f'Moving from "{source_path}" to "{file_destination_path}"')
                            raise ThreadEventException('Event set')
            except ThreadEventException:
                logger.info('Thread finalized')
                return
            except Exception as error:
                logger.warning(f'Error processing files {error}')
        wait_time = config.min_to_seconds()
        logger.info(f'Wait time ... {wait_time}')
        for second in range(wait_time):
            sleep(1)
            if second % 15 == 0 and not second == 0:
                logger.info(f'Time to next cicle {wait_time - second}')
            if event.is_set():
                logger.info(f'Wait time interrupted at {second}')
                return


if __name__ == '__main__':
    window = Main_App('File mover backup')
    event = threading.Event()
    thread = threading.Thread(target=main, args=(event,), daemon=True, name='File_Mover')
    thread.start()
    window.mainloop()


