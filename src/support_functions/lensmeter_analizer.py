import datetime, data_communication, data_organizer, json_config, logging, vca_handler
import logger as log
from file_handler import listFilesInDirSubDirWithDate
from dataclasses import dataclass
from os.path import normpath, abspath


logger = logging.getLogger('warranty_detailed')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''

@dataclass
class LensmeterAnalisys:
    lensmeter_path: list
    export_path: list
    lensmeter_tag: list
    export_tag: list
    lensmeter_extension: str
    export_extension : str
    sheets_id: str
    sheets_name: str
    sheets_range: str
    

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
            lensmeter_path = [normpath(abspath(str(path_item))) for path_item in setting_dict['lensmeter_path']]
            export_path = [normpath(abspath(str(path_item))) for path_item in setting_dict['export_path']]
            lensmeter_tag = setting_dict['lensmeter_tag']
            export_tag = setting_dict['export_tag']
            lensmeter_extension = str(setting_dict['lensmeter_extension'])
            export_extension = str(setting_dict['export_extension'])
            sheets_id = str(setting_dict['sheets_id'])
            sheets_name = str(setting_dict['sheets_name'])
            sheets_range = str(setting_dict['sheets_range'])
            return cls(lensmeter_path, export_path, lensmeter_tag, export_tag, lensmeter_extension, export_extension, sheets_id, sheets_name, sheets_range)
        except Exception as error:
            raise error

'''
==================================================================================================================================

        Template             Template        Template        Template        Template        Template        Template        

==================================================================================================================================
'''

template = '''
{
    "lensmeter_path" : [
        "//192.168.5.8/Arquivo/Lensometro/Controle_Final",
        "//192.168.5.2/Dados/Controle Final/production/lab/arquivos lensometro/conferencia final/read app"
    ],
    "export_path" : [
        "//192.168.5.103/lms/HOST_EXPORT/VCA/read_app",
        "//192.168.5.8/Arquivo/LMS/HOST_EXPORT"
    ],
    "lensmeter_tag" : {
        "JOB" : "", 
        "INSSPH" : {"R" : "", "L" : ""},
        "INSCYL" : {"R" : "", "L" : ""},
        "INSAX" : {"R" : "", "L" : ""},
        "INSADD" : {"R" : "", "L" : ""},
        "INSPRPRVH" : {"R" : "", "L" : ""},
        "INSPRPRVV" : {"R" : "", "L" : ""},
        "INSCOPRVH" : {"R" : "", "L" : ""},
        "INSCOPRVV" : {"R" : "", "L" : ""},
        "INSNRSPH" : {"R" : "", "L" : ""},
        "INSNRCYL" : {"R" : "", "L" : ""},
        "INSNRAX" : {"R" : "", "L" : ""}
    },
    "export_tag" : {
        "SPH" : {"R" : "", "L" : ""},
        "CYL" : {"R" : "", "L" : ""},
        "AX" : {"R" : "", "L" : ""},
        "ADD" : {"R" : "", "L" : ""},
        "INSSPH" : {"R" : "", "L" : ""},
        "INSCYL" : {"R" : "", "L" : ""},
        "INSAX" : {"R" : "", "L" : ""},
        "INSADD" : {"R" : "", "L" : ""},
        "INSPRPRVM" : {"R" : "", "L" : ""},
        "INSPRPRVA" : {"R" : "", "L" : ""},
        "LNAM" : {"R" : "", "L" : ""},
        "LDNAM" : {"R" : "", "L" : ""},
        "MBASE" : {"R" : "", "L" : ""},
        "FRNT" : {"R" : "", "L" : ""},
        "LIND" : {"R" : "", "L" : ""}
    },
    "lensmeter_extension" : "txt",
    "export_extension" : "vca",
    "sheets_id" : "17igRNSjZToXRhrLAnnUJMQ3MlCRPNsszcCE__4rCz-s",
    "sheets_name" : "DATA",
    "sheets_range" : "A2:Z"
}
'''

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def add_date(dict_list: list, date_insertion: datetime.datetime.date) -> list:
    new_list = []
    for dict_value in dict_list:
        temp_dict = {}
        temp_dict['DATE'] = datetime.datetime.strftime(date_insertion, '%d/%m/%Y')
        temp_dict.update(dict_value)
        new_list.append(temp_dict)
    return new_list 



'''
==================================================================================================================================

        Main        Main        Main        Main        Main        Main        Main        Main        Main        Main        

==================================================================================================================================
'''

if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)
    
        # volpe_back_to_main()
    try:
        config_data = json_config.load_json_config('C:/PyAutomations_Reports/config_lensmeter.json', template)
        config = LensmeterAnalisys.check_type_insertion(config_data)
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config

    logger.info('Load config')

    # Get last uploaded date

    try:
        sheets_date_plus_one = data_communication.get_last_date(config.sheets_name, 'A2:A', minimum_date='31/08/2022', sheets_id=config.sheets_id) + datetime.timedelta(days=1)
    except Exception as error:
        logger.critical(f'Error loading table {config.sheets_name}')
        quit()


    # Defining start and end date

    date_value = sheets_date_plus_one
    try:
        lensmeter_files = []
        for path in config.lensmeter_path:
            logger.info(f'Creating file list for {path}')
            lensmeter_files = lensmeter_files + listFilesInDirSubDirWithDate(path, config.lensmeter_extension)
        export_list =[]
        for path in config.export_path:
            logger.info(f'Creating file list for {path}')
            export_list = export_list + listFilesInDirSubDirWithDate(path, config.export_extension)
    except Exception as error:
        logger.error(f'File listing error: {error}')
    while date_value <= datetime.datetime.now().date():
        try:
            logger.info(f"Getting files from {datetime.datetime.strftime(date_value, '%d/%m/%Y')}")

            # Filter file list
            lensmeter_by_date = [file['FILE'] for file in lensmeter_files if file['DATE'] == date_value]
            if not len(lensmeter_by_date) == 0:
                export_by_date = [file['FILE'] for file in export_list if file['DATE'] >= date_value - datetime.timedelta(days=40) and file['DATE'] <= date_value]

                logger.debug('Getting values based on date')
                lensmeter = vca_handler.read_vca(lensmeter_by_date, date_value, date_value, **config.lensmeter_tag)
                vca_export = vca_handler.read_vca_by_job(export_by_date, lensmeter.keys(), 0, 12, **config.export_tag)
                
                logger.debug('Meging values')
                lensmeter_vca_export = vca_handler.merge_read_vca(lensmeter, vca_export, 'LENS', 'EXP', config.export_tag)
                plain_dict = data_organizer.plain_dict_float_format(data_organizer.dict_list_to_plain_dict(lensmeter_vca_export.values()))
                plain_dict_with_date = add_date(plain_dict, date_value)
                
                logger.debug('Uploading values to database')
                values_in_sheet = data_communication.transform_in_sheet_matrix(plain_dict_with_date)
                data_communication.data_append_values(config.sheets_name, config.sheets_range, values_in_sheet, config.sheets_id)
            logger.info(f"Date {datetime.datetime.strftime(date_value, '%d/%m/%Y')} done")
            date_value = date_value + datetime.timedelta(days=1)
        except Exception as error:
            logger.critical(error)
            exit()

