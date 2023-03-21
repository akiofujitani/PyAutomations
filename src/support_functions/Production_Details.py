import file_handler, datetime, calendar, data_organizer, os, json_config, data_communication, logging, threading, keyboard
import logger as log
from vca_handler import VCA_to_dict, filter_tag


logger = logging.getLogger('production_details')


'''
==================================================================================================================================

        Template        Template        Template        Template        Template        Template        Template        Template        

==================================================================================================================================
    path_list = [os.path.normpath(path) for path in config['path_list']]
    tags_list = config['tags_list']
    sheets_name = config['sheets_name']
    sheets_date_pos = config['sheets_date_pos']
    sheets_id = config['sheets_id']
    minimum_date = config['minimum_date']
    extension = config['extension']
    date_tag_list = config['date_tag_list']
    sort_date = config['sort_date']

'''
template = '''
{
    "path_list" : [
        "//192.168.5.103/lms/HOST_EXPORT/VCA/read_app",
        "//192.168.5.8/Arquivo/LMS/HOST_EXPORT/2023"
    ],
    "tags_list" : {
        "JOB" : "",
        "_ENTRYDATE" : "",
        "CLIENT" : "",
        "LNAM" : {"R" : "", "L" : ""},
        "LDNAM" : {"R" : "", "L" : ""},
        "SPH" : {"R" : "", "L" : ""},
        "CYL" : {"R" : "", "L" : ""},
        "AX" : {"R" : "", "L" : ""},
        "ADD" : {"R" : "", "L" : ""},
        "LIND"  : {"R" : "", "L" : ""},
        "INSPRPRVA" : {"R" : "", "L" : ""},
        "INSPRPRVM" : {"R" : "", "L" : ""},
        "_CUSTOMER" : "",
        "CTHNA" : {"R" : "", "L" : ""},
        "CTHNP" : {"R" : "", "L" : ""},
        "_XCALC" : {"R" : "", "L" : ""},
        "MBASE" : {"R" : "", "L" : ""},
        "GBASE" : {"R" : "", "L" : ""},
        "GCROS" : {"R" : "", "L" : ""},
        "FRNT" : {"R" : "", "L" : ""}
    },
    "sheets_name" : "PRODUCTION",
    "sheets_date_pos" : "B:B",
    "sheets_id" : "1QHozuTGKXeqeB1RQ3Zt927d6_ovpON1llOUBGzF35w8",
    "minimum_date" : "01/01/2023",
    "extension" : "vca",
    "date_tag_list" : [
        "_ENTRYDATE"
    ],
    "sort_date" : "_ENTRYDATE"
}


'''



def read_vca(path, extension, start_date, end_date):
    file_list = file_handler.listFilesInDirSubDir(path, extension)
    date_filtered_list = file_handler.listByDate(file_list, start_date, end_date)
    values_dict = {}
    for file in date_filtered_list:
        try:
            with open(file, 'r', errors='replace') as contents:
                fileContents = contents.readlines()
                temp_vca_contents = VCA_to_dict(fileContents)
                values_dict[temp_vca_contents['JOB']] = temp_vca_contents
        except Exception as error:
            logger.error(error)
    return values_dict


def week_date(date_value, days_to_subtract):
    
    new_date = date_value - datetime.timedelta(days=days_to_subtract)
    while calendar.weekday(new_date.year, new_date.month, new_date.day) >= 5:
        new_date = new_date - datetime.timedelta(days=1)
    return new_date


def values_merger(path_list: list, base_list: list, base_search_tag: str, extension: str, start_pos: int=0, end_pos: int=12, **kwargs):
    try:
        file_list = []
        for path in path_list:
            logger.info(path)
            file_list = file_list + file_handler.listFilesInDirSubDir(os.path.normpath(path), extension)
        merged_list = []
        for value in base_list:
            merged_values = value
            file_found = file_handler.file_finder(file_list, value[base_search_tag.upper()], start_pos=start_pos, end_pos=end_pos)
            filtered_tags_value = {}
            filtered_tags_value[base_search_tag.upper()] = value[base_search_tag.upper()]
            if file_found:
                vca_converted = VCA_to_dict(file_handler.file_reader(file_found))
                filtered_tags_value.update(filter_tag(vca_converted, **kwargs))
                merged_values[base_search_tag.upper()] = data_organizer.tags_dict_to_plain_dict(filtered_tags_value)
            else:
                merged_values[base_search_tag.upper()] = data_organizer.tags_dict_to_plain_dict(kwargs)
            merged_list.append(merged_values)
            if len(merged_list) == len(base_list):
                return merged_list                
    except Exception as error:
        logger.error(error)
        raise error
    return merged_list


def production_details(event: threading.Event, config: dict) -> None:
    path_list = [os.path.normpath(path) for path in config['path_list']]
    tags_list = config['tags_list']
    sheets_name = config['sheets_name']
    sheets_date_pos = config['sheets_date_pos']
    sheets_id = config['sheets_id']
    minimum_date = config['minimum_date']
    extension = config['extension']
    date_tag_list = config['date_tag_list']
    sort_date = config['sort_date']


    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, 
                    sheets_date_pos, 
                    minimum_date, sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    except Exception as error:
        logger.info(f'Error loading table {sheets_name}')
        return

    if event.is_set():
        logger.info('Event set')
        return

    logger.info(datetime.datetime.strftime(sheets_date_plus_one, '%d/%m/%Y'))
    logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))

    if not sheets_date_plus_one == datetime.datetime.now().date():
        start_date = sheets_date_plus_one
        date_end = start_date
        while date_end < end_date:
            if end_date > data_organizer.add_months_to_date(start_date, 1):
                date_start = start_date
                date_end = datetime.datetime(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1])
                start_date = date_end + datetime.timedelta(days=1)
            else:
                date_start = start_date
                date_end = end_date

            logger.info(f'Getting data from: {datetime.datetime.strftime(date_start, "%d/%m/%Y")} to {datetime.datetime.strftime(date_end, "%d/%m/%Y")}')

            if event.is_set():
                logger.info('Event set')
                return


            export_data = {}
            for path in path_list:
                try:
                    export_data.update(read_vca(path, extension, date_start, date_end))
                except Exception as error:
                    logger.error(error)

            filtered_data = {}
            for job_number, job in export_data.items():
                tag_filtered = filter_tag(job, **tags_list)
                filtered_data[job_number] = tag_filtered

            if event.is_set():
                logger.info('Event set')
                return

            plain_dict = data_organizer.dict_list_to_plain_dict(filtered_data.values())
            filled_plain_dict = data_organizer.plain_dict_list_filler(plain_dict)
            float_updated_dict = data_organizer.plain_dict_float_format(filled_plain_dict)
            date_converted_dict = data_organizer.convert_to_date(float_updated_dict, '%Y%m%d', '%d/%m/%Y', *date_tag_list)
            ready_list = sorted(date_converted_dict, key=lambda value : datetime.datetime.strptime(value[sort_date], '%d/%m/%Y'))
            sheet = data_communication.transform_in_sheet_matrix(ready_list)
            data_communication.data_append_values(sheets_name ,'A:Z', sheet, sheets_id=sheets_id)

            if event.is_set():
                logger.info('Event set')
                return
    event.set()
    logger.info('Done')


def main(event: threading.Event, config: dict) -> None:
    if event.is_set():
        return
    production_details(event, config)
    return


def quit_func():
    logger.info('Quit pressed')
    event.set()
    return


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)
    # date_target = week_date(datetime.datetime.now().date(), 1)

    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/production_config.json', template)
    except Exception as error:
        logger.critical(f'Could not load config file due {error}')
        exit()
    
    event = threading.Event()
    keyboard.add_hotkey('esc', quit_func)

    for _ in range(3):
        main(event, config)
        if event.is_set():
            break

    logger.info('Production Details Done')


    # date_from_to_str = f'{date_start.strftime("%Y%m%d")}_{date_end.strftime("%Y%m%d")}'
    # filtered_name = f'Filtered_list_{date_from_to_str}'
    # file_handler.listToCSV(float_updated_dict, join(r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\JobFilterPy', f'{filtered_name}.csv'))

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

