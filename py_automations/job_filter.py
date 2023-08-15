import datetime, calendar, logging, os
from data_modules import file_handler, data_organizer, json_config, log_builder
from data_modules.vca_handler import VCA_to_dict, read_vca, read_vca_by_job, filter_tag
from ntpath import join
from dataclasses import dataclass
from os.path import normpath, abspath

logger = logging.getLogger('job_filter')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes                  

==================================================================================================================================
'''

@dataclass
class FilterSettings:
    path_list : list
    extension : str
    tag_filter : dict


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
            path_list = [normpath(abspath(str(path_item))) for path_item in setting_dict['path_list']]
            extension = setting_dict['extension']
            tag_filter = setting_dict['tag_filter']
            return cls(path_list, extension, tag_filter)
        except Exception as error:
            raise error    

'''
==================================================================================================================================

        Template        Template        Template        Template        Template        Template        Template        Template             

==================================================================================================================================
'''
template = '''
{
    "path_list" : [
        "//192.168.5.103/lms/HOST_IMPORT/VCA/NOVO_LMS/READ"
    ],
    "extension : "vca",
    "tag_filter" : {
        "JOB" : "", 
        "CLIENT" : "",
        "LNAM" : "",
        "SPH" : {"R" : "", "L" : ""},
        "CYL" : {"R" : "", "L" : ""},
        "AX" : {"R" : "", "L" : ""},
        "ADD" : {"R" : "", "L" : ""},
        "MINEDG" : {"R" : "", "L" : ""},
        "MINCTR" : {"R" : "", "L" : ""},
        "MBASE" : {"R" : "", "L" : ""},
        "FTYP" : "" 
    }
}
'''


'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def week_date(date_value, days_to_subtract):
    
    new_date = date_value - datetime.timedelta(days=days_to_subtract)
    while calendar.weekday(new_date.year, new_date.month, new_date.day) >= 5:
        new_date = new_date - datetime.timedelta(days=1)
    return new_date


def values_merger(path_list: list, name_base_list: list, base_search_tag: str, *args, start_pos: int=0, end_pos: int=12):
    file_list = []
    for path in path_list:
        file_list = file_list + file_handler.listFilesInDirSubDir(path, 'vca')
    merged_list = []
    for value in name_base_list:
        merged_values = value
        file_found = file_handler.file_finder(file_list, value[base_search_tag.upper()], start_pos=start_pos, end_pos=end_pos)
        filtered_tags_value = {}
        filtered_tags_value[base_search_tag.upper()] = value[base_search_tag.upper()]
        if file_found:
            vca_converted = VCA_to_dict(file_handler.file_reader(file_found))
            filtered_tags_value.update(data_organizer.filter_tag(vca_converted, *args))
            merged_values[base_search_tag.upper()] = data_organizer.tags_dict_to_plain_dict(filtered_tags_value)
        else:
            merged_values[base_search_tag.upper()] = filtered_tags_value
        merged_list.append(merged_values)
    return merged_list


def vca_job_list_filter(path_list: list, extension: str, start_date: datetime.datetime.date, end_date: datetime.datetime.date, **kwargs) -> dict:
    '''
    List vca files in path list between two defined dates read vca data and extract values based on key, value (kwargs)
    '''
    try:
        vca_list = {}
        for path in path_list:
            vca_list.update(read_vca(path, extension, start_date, end_date))
        filtered_vca_list = {}
        for job_number, job_data in vca_list.items():
            filtered_vca_list[job_number] = filter_tag(job_data, **kwargs)
        return filtered_vca_list
    except Exception as error:
        logger.error(error)
        raise error


'''
==================================================================================================================================

        Main        Main        Main        Main        Main        Main        Main        Main        Main        Main        

==================================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)

    try:
        config_data = json_config.load_json_config('C:/PyAutomations_Reports/config_job_filter.json', template)
        config = FilterSettings.check_type_insertion(config_data)
    except:
        logger.critical('Could not load config file')
        exit()


    date_start = datetime.datetime.now().date() - datetime.timedelta(days=1)
    date_end =  datetime.datetime.now().date() - datetime.timedelta(days=1)

    logger.info(datetime.datetime.strftime(date_start, '%d/%m%Y'))
    logger.info(datetime.datetime.strftime(date_end, '%d/%m%Y'))

    filtered_vca_list = read_vca(config.path_list, config.extension, date_start, date_end, **config.tag_filter)

    vca_plain = data_organizer.dict_list_to_plain_dict(filtered_vca_list)
    float_format = data_organizer.plain_dict_float_format(vca_plain)

    print('Done')
    # export_data = read_vca(path_vca, extension, date_start, date_end)
    # export_data.update(read_vca(path_vca_backup, extension, date_start, date_end))

    # tags_list = ['JOB', 'CLIENT', 'LNAM', 'LDNAM', 'SPH', 'CYL', 'AX', 'ADD', 'LIND', 'INSPRPRVA','INSPRPRVM' ,'_CUSTOMER', 'ERDRIN', 'ERDRUP', 'ERNRIN', 'ERNRUP', 'ERSGIN', 'ERSGUP', 'CORRLEN', 'LTYP', 'LTYPEB', 'LTYPEF']
    tags_list = ['JOB', '_ENTRYDATE', 'CLIENT', 'LNAM', 'LDNAM', 'SPH', 'CYL', 'AX', 'ADD', 'CLIENT', 'LIND', 'INSPRPRVA', 'INSPRPRVM', '_CUSTOMER', 'CTHNA', 'CTHNP', '_XCALC' , 'MBASE', 'GBASE', 'GCROS', 'FRNT']

    filtered_data = []
    for job in export_data:
        tag_filtered = data_organizer.filter_tag(export_data[job], 'JOB', *tags_list)
        tag_filtered['JOB'] = job
        filtered_data.append(tag_filtered)

    plain_dict = data_organizer.dict_list_to_plain_dict(filtered_data)
    filled_plain_dict = data_organizer.plain_dict_list_filler(plain_dict)
    float_updated_dict = data_organizer.plain_dict_float_format(filled_plain_dict)

    date_from_to_str = f'{date_start.strftime("%Y%m%d")}_{date_end.strftime("%Y%m%d")}'
    filtered_name = f'Filtered_list_{date_from_to_str}'
    file_handler.listToCSV(float_updated_dict, join(r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\JobFilterPy', f'{filtered_name}.csv'))

    # advance_filtered = data_organizer.filter_tag_by_values(filtered_data, [{'Tag' : 'SPH', 'Operator' : '>=', 'Value' : 10},
    #                                     {'Tag' : 'SPH', 'Operator' : '<=', 'Value' : -12}, 
    #                                     {'Tag' : 'INSPRPRVM', 'Operator' : '>=', 'Value' : 6}, 
    #                                     {'Tag' : 'CYL', 'Operator' : '<=', 'Value' : -6}, 
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : 'SingleVision2NC_LP'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : 'DigitalBifocalRS28R'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : 'AlphaH65_LP'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : '3117'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : '01/08/'},
    #                                     {'Tag': 'LNAM', 'Operator' : '=', 'Value' : '4166'},
    #                                     {'Tag': 'LNAM', 'Operator' : '=', 'Value' : '4144'},
    #                                     {'Tag': 'LNAM', 'Operator' : '=', 'Value' : '4180'},
    #                                     {'Tag': '_CUSTOMER', 'Operator' : 'contains', 'Value' : 'POLY'},
    #                                     {'Tag': '_CUSTOMER', 'Operator' : 'contains', 'Value' : 'ITA Ot'},
    #                                     {'Tag': '_CUSTOMER', 'Operator' : 'contains', 'Value' : 'NATAL LENT'}])

    # plain_dict = data_organizer.dict_list_to_plain_dict(advance_filtered)
    # filled_plain_dict = data_organizer.plain_dict_list_filler(plain_dict)
    # float_updated_dict = data_organizer.plain_dict_float_format(filled_plain_dict)

    # advance_name = f'Advance_filter_{date_from_to_str}'
    # file_handler.listToCSV(float_updated_dict, join(r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\JobFilterPy', f'{advance_name}.csv'))

