import datetime, logging
from data_modules import data_communication, data_organizer, json_config, vca_handler, log_builder
from data_modules.file_handler import listFilesInDirSubDirWithDate
from dataclasses import dataclass
from os.path import normpath, abspath


logger = logging.getLogger('warranty_detailed')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''

@dataclass
class MapperAnalisys:
    ins_path: list
    ins_extension: str
    sheets_id: str
    sheets_name: str
    sheets_range: str    
    mapper_tag: list
    

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
            ins_path = [normpath(abspath(str(path_item))) for path_item in setting_dict['ins_path']]
            ins_extension = setting_dict['ins_extension']
            sheets_id = setting_dict['sheets_id']
            sheets_name = setting_dict['sheets_name']
            sheets_range = setting_dict['sheets_range']
            mapper_tag = setting_dict['mapper_tag']
            return cls(ins_path, ins_extension, sheets_id, sheets_name, sheets_range, mapper_tag)
        except Exception as error:
            raise error

'''
==================================================================================================================================

        Template             Template        Template        Template        Template        Template        Template        

==================================================================================================================================
'''

template = '''
{
    "ins_path" : [
        "//192.168.5.2/Automapper/INSFiles/Read app"
        ],
    "ins_extension" : "txt",
    "sheets_id" : "1tGdGd_-ub-tWDvcsFMPmHyGom700eREDBwfvBU6Cnsg",
    "sheets_name" : "DATA",
    "sheets_range" : "A2:Z",
    "mapper_tag" : {
        "JOB" : "",
        "DDFMT" : {
            "N1": "", 
            "SIDE" : "", 
            "N2" : "", 
            "N3" : ""}, 
        "DD" : {
            "N1" : "",
            "CHAR" : "",
            "Error" : "",
            "NOT_OK" : "",
            "Value" : "",
            "Tol" : "",
            "N2" : ""
        }
    }
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
    log_builder.logger_setup(logger)
    
        # volpe_back_to_main()
    try:
        config_data = json_config.load_json_config('C:/PyAutomations_Reports/config_mapper.json', template)
        config = MapperAnalisys.check_type_insertion(config_data)
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config

    logger.info('Load config')

    # Get last uploaded date

    try:
        sheets_date_plus_one = data_communication.get_last_date(config.sheets_name, 'A2:A', minimum_date='01/05/2022', sheets_id=config.sheets_id) + datetime.timedelta(days=1)
    except Exception as error:
        logger.critical(f'Error loading table {config.sheets_name}')
        quit()


    # Defining start and end date

    date_value = sheets_date_plus_one
    try:
        lensmeter_files = []
        for path in config.ins_path:
            logger.info(f'Creating file list for {path}')
            ins_files = lensmeter_files + listFilesInDirSubDirWithDate(path, config.ins_extension)
    except Exception as error:
        logger.error(f'File listing error: {error}')
    while date_value <= datetime.datetime.now().date():
        try:
            logger.info(f"Getting files from {datetime.datetime.strftime(date_value, '%d/%m/%Y')}")

            # Filter file list
            ins_by_date = [file['FILE'] for file in ins_files if file['DATE'] == date_value]
            if not len(ins_by_date) == 0:

                logger.debug('Getting values based on date')
                ins = vca_handler.read_vca(ins_by_date, date_value, date_value, **config.mapper_tag)

                
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

