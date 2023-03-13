import file_handler, vca_handler, vca_handler_frame_size, json_config, threading, logging
from time import sleep
from tkinter import messagebox
from ntpath import join
from os.path import normpath
import logger as log
from dataclasses import dataclass
from os.path import normpath, abspath


logger = logging.getLogger('vca_bot_volpe_mid')


config_template = '''
{
    "wait_time" : "5",  
    "vca_path" : "C:/LMS/HOST_IMPORT/VCA/IMPORT_TEMP",
    "vca_done" : "C:/LMS/HOST_IMPORT/VCA/NOVO_LMS",
    "vca_new_file": "C:/LMS/HOST_IMPORT/VCA/359",
    "vca_error" : "C:/LMS/HOST_IMPORT/VCA/IMPORT_TEMP/ERROR",
    "extension" : "vca",
    "directory_list" : [
        {
            "source" : "C:/LMS/HOST_EXPORT/VCA/read",
            "destination_copy" : "C:/LMS/HOST_EXPORT/VCA/NOVO_LMS",
            "destination_move" : "C:/LMS/HOST_EXPORT/VCA/MID_READ",
            "extension" : "vca"
        }
    ]
}
'''


@dataclass
class Move_Settings:
    source: str
    destination_copy: str
    destination_move: str
    extension: str


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, setting_dict=dict):
        try:
            source = normpath(abspath(str(setting_dict['source'])))
            destination_copy = normpath(abspath(str(setting_dict['destination_copy'])))
            destination_move = normpath(abspath(str(setting_dict['destination_move'])))
            extension = str(setting_dict['extension'])
            return cls(source, destination_copy, destination_move, extension)
        except Exception as error:
            raise error


    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['source'] = self.source.replace('\\', '/')
        values_dict['destination'] = self.destination.replace('\\', '/')
        values_dict['extension'] = self.extension
        values_dict['copy'] = self.copy
        return values_dict

@dataclass
class Configuration_Values:
    wait_time: int
    vca_path: str
    vca_done: str
    vca_new_file: str
    vca_error: str
    extension : str
    directory_list : list


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, config_file_path=str, template=str):
        try:
            config = json_config.load_json_config(config_file_path, template)
            wait_time = int(config['wait_time'])
            vca_path = normpath(abspath(str(config['vca_path'])))
            vca_done = normpath(abspath(str(config['vca_done'])))
            vca_new_file = normpath(abspath(str(config['vca_new_file'])))
            vca_error = normpath(abspath(str(config['vca_error'])))
            extension = str(config['extension'])
            directory_list = [Move_Settings.check_type_insertion(item) for item in config['directory_list']]
            return cls(wait_time, vca_path, vca_done, vca_new_file, vca_error, extension, directory_list)
        except Exception as error:
            raise error


    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['wait_time'] = self.wait_time
        values_dict['vca_path'] = self.vca_path
        values_dict['vca_done'] = self.vca_done
        values_dict['vca_new_file'] = self.vca_new_file
        values_dict['vca_error'] = self.vca_error
        values_dict['extension'] = self.extension
        values_dict['directory_list'] = [directory_value.convert_to_dict() for directory_value in self.directory_list]
        return values_dict


    def directory_list_add(self, move_settings=Move_Settings) -> None:
        self.directory_list.append(move_settings)


    def min_to_seconds(self) -> int:
        return self.wait_time * 60


class ThreadEventException(Exception):
    '''Thread event exception'''
    pass


def __resize_both_sides(trcfmt=dict, hbox=int, vbox=int) -> dict:
    try:
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
    except Exception as error:
        logger.error(error)
        raise error


def vca_file_process():
    try:
        config = Configuration_Values.check_type_insertion('config.json', config_template)
    except Exception as error:
        logger.critical(error)
        messagebox.showerror('VCA Bot Volpe/Middleware', f'Error loading configuration json file due \n{error}')
        quit()

    try:
        while True:
            # VCA converter
            vca_list = file_handler.file_list(config.vca_path, config.extension)
            if len(vca_list) > 0:
                logger.info(f'List for {config.vca_path} contains {len(vca_list)}')
                for vca_file in vca_list:
                    try:
                        vca_data = file_handler.file_reader(join(config.vca_path, vca_file))
                        job_vca = vca_handler.VCA_to_dict(vca_data)
                        logger.info(f'{job_vca["JOB"]}\n')
                        if 'TRCFMT' not in job_vca.keys() or not int(job_vca['TRCFMT']['R']['TRCFMT'][1]) == 400:
                            file_handler.file_move_copy(config.vca_path, config.vca_done, vca_file, True)
                            sleep(0.5)
                            file_handler.file_move_copy(config.vca_path, config.vca_new_file, vca_file, False)
                            logger.info(f'File {vca_file} copied/moved without changes')
                        else:
                            trace_format_resized = __resize_both_sides(job_vca['TRCFMT'], job_vca['HBOX'], job_vca['VBOX'])
                            job_vca['TRCFMT'] = trace_format_resized
                            vca_contents_string = vca_handler.dict_do_VCA(job_vca)
                            file_handler.file_move_copy(config.vca_path, config.vca_done, vca_file, False)
                            file_handler.file_writer(config.vca_new_file, vca_file, vca_contents_string)
                            logger.debug(vca_contents_string)
                            logger.info(f'File {vca_file} copied/moved changing frame values')
                    except Exception as error:
                        logger.error(f'Error {error} in file {vca_file}')
                        file_handler.file_move_copy(config.vca_path, config.vca_error, vca_file, False)

            # File mover
            if len(config.directory_list) > 0:
                for move_group in config.directory_list:
                    try:
                        file_list = file_handler.file_list(move_group.source, move_group.extension)
                        if len(file_list) > 0:
                            logger.info(f'File list for {move_group.source} contains {len(file_list)}')
                            for file in file_list:
                                file_handler.file_move_copy(move_group.source, move_group.destination_copy, file, True)
                                sleep(0.3)
                                file_handler.file_move_copy(move_group.source, move_group.destination_move, file, False)
                                sleep(0.3)
                    except Exception as error:
                        logger.error(f'Error processing files {error}')
            logger.info(f'Waiting... {config.wait_time} seconds')
            sleep(config.wait_time)
    except Exception as error:
        logger.critical(error)
        quit()


def main(event=threading.Event):
    vca_file_process(event)


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    vca_file_process()