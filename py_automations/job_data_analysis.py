import datetime, logging
from data_modules import data_communication, data_organizer, json_config, vca_handler, log_builder
from data_modules.file_handler import listFilesInDirSubDir
from dataclasses import dataclass
from os.path import normpath, abspath


logger = logging.getLogger('warranty_detailed')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''

@dataclass
class JobAnalysis:
    import_path: list
    export_path: list
    import_tag: list
    export_tag: list
    extension: str
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
            import_path = [normpath(abspath(str(path_item))) for path_item in setting_dict['import_path']]
            export_path = [normpath(abspath(str(path_item))) for path_item in setting_dict['export_path']]
            import_tag = setting_dict['import_tag']
            export_tag = setting_dict['export_tag']
            extension = str(setting_dict['extension'])
            sheets_id = str(setting_dict['sheets_id'])
            sheets_name = str(setting_dict['sheets_name'])
            sheets_range = str(setting_dict['sheets_range'])
            return cls(import_path, export_path, import_tag, export_tag, extension, sheets_id, sheets_name, sheets_range)
        except Exception as error:
            raise error

'''
==================================================================================================================================

        Template             Template        Template        Template        Template        Template        Template        

==================================================================================================================================
'''

template = '''
{
    "import_path" : [
        "//192.168.5.103/lms/HOST_IMPORT/VCA/NOVO_LMS/READ"
    ],
    "export_path" : [
        "//192.168.5.103/lms/HOST_EXPORT/VCA/NOVO_LMS/READ"    
    ],
    "import_tag" : {
        "JOB" : "", 
        "CLIENT" : "",
        "LNAM" : {"R" : "", "L" : ""},
        "SPH" : {"R" : "", "L" : ""},
        "CYL" : {"R" : "", "L" : ""},
        "AX" : {"R" : "", "L" : ""},
        "ADD" : {"R" : "", "L" : ""},
        "MINEDG" : {"R" : "", "L" : ""},
        "MINCTR" : {"R" : "", "L" : ""},
        "MBASE" : {"R" : "", "L" : ""},
        "FTYP" : {"R" : "", "L" : ""} 
    },
    "export_tag" : {
        "LNAM" : {"R" : "", "L" : ""},
        "LDNAM" : {"R" : "", "L" : ""},
        "INSSPH" : {"R" : "", "L" : ""}, 
        "INSCYL" : {"R" : "", "L" : ""}, 
        "INSAX" : {"R" : "", "L" : ""}, 
        "INSADD" : {"R" : "", "L" : ""},
        "MBASE" : {"R" : "", "L" : ""},
        "OTHK" : {"R" : "", "L" : ""},
        "THNP" : {"R" : "", "L" : ""},
        "INSPRPRVA" : {"R" : "", "L" : ""},
        "INSPRPRVM" : {"R" : "", "L" : ""},
        "PRVA" : {"R" : "", "L" : ""},
        "PRVM" : {"R" : "", "L" : ""}
    },
    "extension" : "vca",
    "sheets_id" : "1PgHZmrIOkttinhAa7ZLbNJTk-1y1ds9iOf0j_W4fCy4",
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
    log_builder.logger_setup(logger)
    
        # volpe_back_to_main()
    try:
        config_data = json_config.load_json_config('C:/PyAutomations_Reports/config_job_data.json', template)
        config = JobAnalysis.check_type_insertion(config_data)
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config

    logger.info('Load config')

    # Get last uploaded date

    try:
        sheets_date_plus_one = data_communication.get_last_date(config.sheets_name, 'A2:A', '20/10/2024', sheets_id=config.sheets_id)
    except Exception as error:
        logger.critical(f'Error loading table {config.sheets_name}')
        quit()


    try:
        import_files = []
        for path in config.import_path:
            logger.info(f'Creating file list for {path}')
            import_files = import_files + listFilesInDirSubDir(path, config.extension)
        export_list = []
        for path in config.export_path:
            logger.info(f'Creating file list for {path}')
            export_list = export_list + listFilesInDirSubDir(path, config.extension)
    except Exception as error:
        logger.error(f'File listing error: {error}')

    # Defining start and end date
    date_value = sheets_date_plus_one
    while date_value < datetime.datetime.now().date():
        try:
            logger.info(datetime.datetime.strftime(date_value, '%d/%m/%Y'))           
            vca_import = vca_handler.read_vca(import_files, date_value, date_value, **config.import_tag)
            vca_export = vca_handler.read_vca_by_job(export_list, vca_import.keys(), 0, 12, **config.export_tag)
            if len(vca_import) > 0:
                vca_import_export = vca_handler.merge_read_vca(vca_import, vca_export, 'IMP', 'EXP', config.export_tag)
                plain_dict = data_organizer.plain_dict_float_format(data_organizer.dict_list_to_plain_dict(vca_import_export.values()))
                plain_dict_with_date = add_date(plain_dict, date_value)
                values_in_sheet = data_communication.transform_in_sheet_matrix(plain_dict_with_date)
                data_communication.data_append_values(config.sheets_name, config.sheets_range, values_in_sheet, config.sheets_id)
            date_value = date_value + datetime.timedelta(days=1)
        except Exception as error:
            logger.critical(error)
            exit()

