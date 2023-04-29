import win32print, file_handler, json_config, logging, subprocess, sys
import logger as log
from json import loads
from dataclasses import dataclass
from os.path import normpath, join, exists, abspath
from os import remove
from time import sleep


logger = logging.getLogger('printer_manager')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''


@dataclass
class Configuration_Values:
    source_path: str
    done_path: str
    print_program: str
    print_command: str
    extension : str
    printer_list: list
    wait_time: int
    print_interval: int


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
        source_path = normpath(setting_dict['source_path'])
        done_path = normpath(setting_dict['done_path'])
        print_program = normpath(setting_dict['print_program'])
        print_command = setting_dict['print_command']
        extension = setting_dict['extension']
        printer_list = setting_dict['printer_list']
        wait_time = setting_dict['wait_time']
        print_interval = setting_dict['print_interval']
        return cls(source_path, done_path, print_program, print_command, extension, printer_list, wait_time, print_interval)


'''
==================================================================================================================================

        Template             Template        Template        Template        Template        Template        Template        

==================================================================================================================================
'''


template = '''
{
    "source_path" : "",
    "done_path" : "",
    "print_program" : "./FoxitReader.exe",
    "print_command" : "-t",
    "extension" : "pdf",
    "printer_list" : [
        "Microsoft Print to PDF"
    ],
    "wait_time" : 10,
    "print_interval" : 3
}

'''

'''
==================================================================================================================================

        Functions       Functions       Functions       Functions       Functions       Functions       Functions       Functions       

==================================================================================================================================
'''


def check_printers(printer_list_set: list) -> bool:
    '''
    Check printers
    '''
    printer_list_pc = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)]  # get printers
    compared_list = []
    for printer in printer_list_pc:
        if printer in printer_list_set:
            compared_list.append(printer)
    if len(compared_list) == len(printer_list_set):
        logger.debug('True')
        return True
    logger.debug('False')
    return False
    

def print_file(printer: str, print_program: str, print_command: str, file: str) -> None:
    '''
    Sent file to specific printer with command using cmd
    '''
    try:
        cmd = f'"{print_program}" {print_command} "{file}" "{printer}"'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
        logger.info(proc)
        return
    except Exception as error:
        logger.error(error)
        raise(error)


def get_jobs_in_printers(printer_list: list) -> dict:
    '''
    Get print jobs being done in each printer in printer list
    '''
    printer_and_jobs = {}
    try:
        for printer in printer_list:
            printer_values = win32print.GetPrinter(win32print.OpenPrinter(printer), 2)
            printer_and_jobs[printer] = printer_values['cJobs']
            logger.debug(f'Printer {printer} : {printer_values["cJobs"]}')
        return printer_and_jobs
    except Exception as error:
        logger.error(f'Get jobs {error}')
        raise error



def resource_path(relavite_path: str):
    '''
    Get absolute path to resource, works for dev and for PyInstaller
    '''
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath('.')
    return join(base_path, relavite_path)



'''
==================================================================================================================================

        Main        Main        Main        Main        Main        Main        Main        Main        Main        Main              

==================================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    try:
        config_dict = json_config.load_json_config('printer_manager.json', template)
        config = Configuration_Values.check_type_insertion(config_dict)
    except Exception as error:
        logger.critical(f'Config error: {error}')
        exit()
    
    logger.debug('Config loaded')

    if check_printers(config.printer_list):
        template_dict = loads(template)
        print_program = config.print_program if not config.print_program == normpath(template_dict['print_program']) else resource_path(config.print_program)
        last_used_printer = ''
        last_job_in_printers = {}
        file_done_list = []
        while True:
            try:
                file_list = file_handler.file_list(config.source_path, config.extension)
                if file_list:
                    for file in file_list:
                        if file not in file_done_list:
                            job_in_printers = get_jobs_in_printers(config.printer_list)
                            try:
                                if len(config.printer_list) > 1:
                                    for printer in config.printer_list:
                                        logger.debug(printer)
                                        if job_in_printers.get(printer, 0) == 0 and not last_used_printer == printer:
                                            logger.debug(f'Using {printer}')
                                            print_file(printer, print_program, config.print_command, join(config.source_path, file))
                                            last_used_printer = printer
                                            logger.debug(last_used_printer)
                                            logger.info(f'File {file} sent to printer {printer}')
                                            file_done_list.append(file)
                                            break
                                        if not job_in_printers.get(printer, 0) == 0 and job_in_printers.get(printer, 0) == last_job_in_printers.get(printer, 0):
                                            last_used_printer = ''
                                else:
                                    print_file(config.printer_list[0], print_program, config.print_command, join(config.source_path, file))
                                    file_done_list.append(file)
                                    logger.info(f'File {file} sent to printer {config.printer_list[0]}')
                            except Exception as error:
                                logger.warning(error)
                        sleep(config.print_interval)
                        last_job_in_printers = job_in_printers
                    if len(file_done_list) > 0:
                        for file in file_done_list:
                            removed_list = []
                            try:
                                if len(config.done_path) > 1:
                                    file_handler.file_move_copy(config.source_path, config.done_path, file, False)
                                else:
                                    file_full_path = join(config.source_path, file)
                                    if exists(join(file_full_path)):
                                        remove(file_full_path)
                                        logger.info(f'File {file} removed')
                                removed_list.append(file)
                            except Exception as error:
                                logger.warning(f'File process {error}')
                        if len(removed_list) > 0:
                            for file in removed_list:
                                file_done_list.remove(file)
                logger.info('Waiting...')    
                sleep(config.wait_time)
            except Exception as error:
                logger.error(error)
