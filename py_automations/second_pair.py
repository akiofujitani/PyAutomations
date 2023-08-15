import datetime, pyautogui, logging
from data_modules import data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, log_builder
from threading import Event, Thread
from dataclasses import dataclass
from time import sleep

logger = logging.getLogger('second_pair')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''


config_template = '''
{
    "sheets_id" :  "1zEtjvUprM80XZqwZHtj7cMcSAUCLHwvj2jh2F3BCPHU",
    "sheets_name" : "MDO",
    "sheets_pos" : "A:Z",
    "sheets_name_done" : "DONE",
    "sheets_pos_done" : "A:D"
}
'''


@dataclass
class Configuration_Values:
    sheets_id :  str
    sheets_name : str
    sheets_pos : str
    sheets_name_done : str
    sheets_pos_done : str


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
    def check_type_insertion(cls, config_values: dict):
        try:
            sheets_id =  config_values['sheets_id']
            sheets_name = config_values['sheets_name']
            sheets_pos = config_values['sheets_pos']
            sheets_name_done = config_values['sheets_name_done']
            sheets_pos_done = config_values['sheets_pos_done']
            return cls(sheets_id, sheets_name, sheets_pos, sheets_name_done, sheets_pos_done)
        except Exception as error:
            raise error



def main_automation(config: Configuration_Values, event: Event):
    try:
        pass
    except Exception as error:
        logger.error(f'Error {error}')
        raise error


if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)


    try:
        config_dict = json_config.load_json_config('./second_pair_confg.json', config_template)
        config = Configuration_Values.check_type_insertion(config_dict)
    except Exception as error:
        logger.critical(f'Config error {error}')
        exit()





    logger.debug('Config loaded')