import file_handler, vca_handler, vca_handler_frame_size, json_config, tkinter
import logger as log
from time import sleep
from ntpath import join
from os.path import normpath


logger = log.logger('vca_bot_volpe_mid')


def __resize_both_sides(trcfmt=dict, hbox=int, vbox=int) -> dict:
    resized_trcfmt = {}
    temp_trcfmt = {}
    for side, value in trcfmt.items():
        shape_resized = vca_handler_frame_size.frame_resize(value['R'], hbox[side], vbox[side])
        temp_trcfmt['R'] = list(shape_resized.values())
        temp_trcfmt['TRCFMT'] = ['1', str(len(shape_resized)), 'E', side, 'F']
        resized_trcfmt[side] = temp_trcfmt
        temp_trcfmt = {}
        if len(trcfmt) == 1:
            other_side = 'R' if side == 'R' else 'L'
            temp_trcfmt['R'] = list(vca_handler_frame_size.shape_mirror(shape_resized).values())
            temp_trcfmt['TRCFMT'] = ['1', len(shape_resized), 'E', other_side, 'F']
            resized_trcfmt[other_side] = temp_trcfmt
        logger.info(f'Side {side} done')      
    return resized_trcfmt


class Main_App(tkinter.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title('VCA Bot Volpe Mid')
        self.minsize(width=500, height=500)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_columnconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1, minsize=50)

        start_button = tkinter.Button(self, text='Start', command=self.__click_button_start, width=25)
        start_button.grid(column=0, row=0, padx=(3), pady=(3), sticky='nesw')

        stop_button = tkinter.Button(self, text='Stop', command=self.__click_button_stop, width=25)
        stop_button.grid(column=1, row=0, padx=(3), pady=(3), sticky='nesw')

        scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        scrolled_text.grid(column=0, row=1, columnspan=4, sticky='nesw', padx=(3), pady=(3))
        text_handler = log.TextHandler(scrolled_text)
        logger.addHanlder(text_handler)


    def __click_button_start(self):
        logger.debug('Button start clicked')


    def __click_button_stop(self):
        logger.debug('Button stop clicked')

if __name__ == '__main__':
    try:
        config = json_config.load_json_config('config.json')
    except Exception as error:
        logger.critical(error)
        tkinter.messagebox.showerror('VCA Bot Volpe/Middleware', f'Error loading configuration json file due \n{error}')
        quit()

    window = Main_App()
    window.mainloop()


    path = normpath(config['path'])
    path_done = normpath(config['path_done'])
    path_new = normpath(config['path_new_file'])
    sleep_time = int(config['sleep_time'])


    try:
        while True:
            vca_list = file_handler.file_list(path, config['extension'])
            if len(vca_list) > 0:
                for vca_file in vca_list:
                    try:
                        vca_data = file_handler.file_reader(join(path, vca_file))
                        job_vca = vca_handler.VCA_to_dict(vca_data)
                        logger.info(f'{job_vca["JOB"]}\n')
                        if 'TRCFMT' not in job_vca.keys() or not int(job_vca['TRCFMT']['R']['TRCFMT'][1]) == 400:
                            file_handler.file_move_copy(path, path_done, vca_file, True)
                            sleep(0.5)
                            file_handler.file_move_copy(path, path_new, vca_file, False)
                        else:
                            trace_format_resized = __resize_both_sides(job_vca['TRCFMT'], job_vca['HBOX'], job_vca['VBOX'])
                            job_vca['TRCFMT'] = trace_format_resized
                            vca_contents_string = vca_handler.dict_do_VCA(job_vca)
                            file_handler.file_move_copy(path, path_done, vca_file, False)
                            file_handler.file_writer(path_new, vca_file, vca_contents_string)
                            logger.info(vca_contents_string)
                    except Exception as error:
                        logger.error(f'Error {error} in file {vca_file}')

            if len(config['move_groups']) > 0:
                for move_group in config['move_groups']:
                    extension = normpath(move_group['source_destin_extention'])
                    source_directory = normpath(move_group['source_directory'])
                    destin_directory = normpath(move_group['destin_directory'])
                    file_copy = eval(move_group['copy'])
                    try:
                        file_list = file_handler.file_list(source_directory, extension)
                        if len(file_list) > 0:
                            for file in file_list:
                                file_handler.file_move_copy(source_directory, destin_directory, file, file_copy)
                                sleep(0.1)
                    except Exception as error:
                        logger.error(f'Error processing files {error}')

            logger.info(f'Waiting... {sleep_time} seconds')
            sleep(sleep_time)
    except Exception as error:
        logger.critical(error)
        tkinter.messagebox.showerror('VCA Bot Volpe/Middleware', f'Error in routine execution\n{error}')
        quit()
