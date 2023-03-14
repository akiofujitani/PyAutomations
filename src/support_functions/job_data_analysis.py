import datetime, file_handler, data_communication, data_organizer, json_config, Production_Details, logging, job_filter
import logger as log
from ntpath import join
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
            import_tag = [str(tag) for tag in setting_dict['import_tag']]
            export_tag = [str(tag) for tag in setting_dict['export_tag']]
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
    "import_tag" : [
        "JOB", 
        "CLIENT", 
        "LNAM", 
        "SPH", 
        "CYL", 
        "AX", 
        "ADD",
        "MINEDG",
        "MINCTR",
        "MBASE",
        "FTYPE" 
    ],
    "export_tag" : [
        "LNAM",
        "LDNAM",
        "SPH", 
        "CYL", 
        "AX", 
        "ADD",
        "MBASE",
        "OTHK",
        "THNP",
        "INSPRPRVA",
        "INSPRPRVM"
    ],
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


def filter_tag_list(job_data, *args):
    filtered_job_data = {}
    for key, job in job_data.items():
        temp_job = {}
        for arg in args:
            temp_job[arg] = job.get(arg, '')
        filtered_job_data[key] = temp_job
    return filtered_job_data


def filter_tag(job_data, *args):
    '''
    filter tags based on tag's list
    '''
    filtered_data = {}
    for arg in args:
        filtered_data[arg] = getattr(job_data, arg, '')
    return filtered_data



def warranty_add_quantity(warranty_list):
    updated_warranty_list = []
    for warranty in warranty_list:
        temp_values = warranty
        temp_values['QUANTITY'] = 2 if warranty['LADO DO OLHO'] == 'AMBOS' else 1
        updated_warranty_list.append(temp_values)
    return updated_warranty_list



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
        config_data = json_config.load_json_config('C:/PyAutomations_Reports/config_job_data.json', template)
        config = JobAnalysis.check_type_insertion(config_data)
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config

    logger.info('Load config')
    # Get last uploaded date

    try:
        sheets_date_plus_one = data_communication.get_last_date(config.sheets_name, 'A2:A', '28/02/2023', sheets_id=config.sheets_id) + datetime.timedelta(days=1)
    except Exception as error:
        logger.critical(f'Error loading table {config.sheets_name}')
        quit()


    # Defining start and end date

    while sheets_date_plus_one < datetime.datetime.now().date():
        try:
            vca_values = {}
            for path in config.import_path:
                vca_values.update(job_filter.read_vca(path, config.extension, sheets_date_plus_one, sheets_date_plus_one))
            filtered_vca_values = filter_tag_list(vca_values, *config.import_tag)
      
            file_date = None
            file_list = file_handler.file_list(path, extension)
            for file in file_list:
                file_date = file_handler.file_contents_last_date(file_handler.CSVtoList(join(path, file)), 'DT.PED GARANTIA')
                if sheets_date_plus_one > file_date:
                    file_handler.file_move_copy(path, path_done, file, False)
            if file_date == None or file_date > sheets_date_plus_one:
                start_date = sheets_date_plus_one
            else:
                start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)

            logger.info(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
            logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))
        except Exception as error:
            logger.critical(error)
            exit()

        # Data processing
        
        try:
            file_list = file_handler.file_list(path, extension)
            for file in file_list:
                partial_list = file_handler.CSVtoList(join(path, file))
                filtered_list = data_organizer.filter_by_values(partial_list, 'MOTIVO GARANTIA', *warranty_motives_list)
                updated_list = remove_from_dict(filtered_list, *remove_fields)
                sorted_list = warranty_add_quantity(sorted(updated_list, key=lambda value : value['DT.PED GARANTIA']))
                temp_list = []
                if len(filtered_list) > 0:
                    for field_name in warranty_job_fields:
                        temp_list = Production_Details.values_merger(path_export, sorted_list, field_name, *filter_tags_list)
                        logger.info(f'{field_name} filtering terminated')
                    plain_dict_list = data_organizer.dict_list_to_plain_dict(temp_list)
                    filled_dict_list = data_organizer.plain_dict_list_completer(plain_dict_list)
                    # filled_dict_list = data_organizer.convert_to_date(filled_dict_list, '%Y%m%d', '%d/%m/%Y', 'PEDIDO GARANTIA__ENTRYDATE', 'PEDIDO ORIGINAL__ENTRYDATE')
                    sheet = data_communication.transform_in_sheet_matrix(data_organizer.plain_dict_float_format(filled_dict_list))
                    data_communication.data_append_values(sheets_name , f'A:{data_organizer.num_to_col_letters(len(sheet[0]))}', sheet, sheets_id=sheets_id)
                    file_date = file_handler.file_contents_last_date(file_handler.CSVtoList(join(path, file)), 'DT.PED GARANTIA')
                    string_file_date = datetime.datetime.strftime(file_date, '%d/%m/%Y')
                    data_communication.data_update_values(sheets_name_date, sheets_date_pos, [[string_file_date]], sheets_id=sheets_id)
                    logger.info(f'{file} done')
                file_handler.file_move_copy(path, path_done, file, False)
            logger.info("Done")
        except Exception as error:
            logger.error(f'Error in data processing {error}')
