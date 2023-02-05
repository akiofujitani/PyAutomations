import tkinter, json_config, file_mover_backup
from tkinter import ttk
import logger as log
from os.path import normpath
from time import sleep

logger = log.logger('gui_builder')

class Config_Window(tkinter.Tk):
    def __init__(self, config=file_mover_backup.Configuration_Values, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.config = config
        self.title('Configuration')
        self.minsize(width=400, height=300)
        self.rowconfigure(0, weight=1, )
        self.columnconfigure(0, weight=1)

        self.tab_control = ttk.Notebook(self)
        tab_main = ttk.Frame(self.tab_control)
        tab_file_settings = ttk.Frame(self.tab_control)

        self.tab_control.add(tab_main, text='Main')
        self.tab_control.add(tab_file_settings, text='File Settings')
        self.tab_control.grid(column=0, row=0, columnspan=4, sticky='nesw', padx=(5), pady=(5))

        ttk.Label(tab_main, text='Wait time', justify='left').grid(column=0, row=0, padx=(5), pady=(5, 0))
        ttk.Label(tab_main, text='Files per cicle', justify='left').grid(column=0, row=1, padx=(5), pady=(5, 0))
        ttk.Label(tab_main, text='Months naming', justify='left').grid(column=0, row=2, padx=(5), pady=(5, 0))

        wait_time_entry = ttk.Entry(tab_main, width=40, justify='center')
        wait_time_entry.grid(column=1, row=0, columnspan=2, sticky='nesw', padx=(5), pady=(5, 0))
        wait_time_entry.insert(tkinter.END, str(self.config.wait_time))
        files_per_cicle = ttk.Entry(tab_main, width=40, justify='center')
        files_per_cicle.grid(column=1, row=1, columnspan=2, sticky='nesw', padx=(5), pady=(5, 0))
        files_per_cicle.insert(tkinter.END, str(self.config.file_per_cicle))
        months_naming = ttk.Entry(tab_main, width=40, justify='left')
        months_naming.grid(column=1, row=2, columnspan=2, sticky='nesw', padx=(5), pady=(5, 0))
        months_naming.insert(tkinter.END, str(self.config.month_name_list))
        tab_main.columnconfigure(1, weight=1)

        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=1, padx=(5), pady=(0, 5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=1, padx=(5), pady=(0, 5))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)


    def __click_button_cancel(self):
        logger.debug('Cancel click')
        self.__on_window_close()


    def __click_button_save(self):
        logger.debug('Save click')


    def __on_window_close(self):
        logger.debug('On close click')
        self.destroy()


def __load_configuration(config_path=str) -> dict:
    '''
    Load configuration from .json file. If json file do not exists it will be created using the template values.
    '''
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
        return file_mover_backup.Configuration_Values(int(config['wait_time_min']),
                int(config['files_per_cicle']),
                config['month_name'], 
                [file_mover_backup.Move_Settings(normpath(item['source']), 
                        normpath(item['destin']),
                        item['extension'],
                        int(item['days_from_today']),
                        eval(item['copy'])) for item in config['directory_list']])
    except Exception as error:
        logger.critical(f'Error loading configuration file. {error}')
        sleep(3)
        quit()


if __name__ == '__main__':
    config = __load_configuration('file_mover_backup.json')
    window = Config_Window(config)
    window.mainloop()