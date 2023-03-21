import erp_volpe_handler, datetime, calendar, file_handler, data_communication, data_organizer, json_config, os, logging, threading, keyboard
import logger as log 
from ntpath import join
from copy import deepcopy

logger = logging.getLogger('rework')


'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def add_months_to_date(date=datetime.datetime, num_of_months=int):
    for i in range(num_of_months):
        date = date + datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1])
    return date


def create_update_motive_list(breakage_list):
    print('Creating motive list')
    movite_list = []

    for breakage in breakage_list:
        if not breakage["MOTIVO RETRABALHO"] in [motive[0] for motive in movite_list]:
            movite_list.append([breakage['MOTIVO RETRABALHO'], breakage['SETOR']])
    return movite_list


def add_unique(main_list, sub_list, index_value):
    unique_list = []
    values_by_index = [value[0] for value in main_list]
    for item in sub_list:
        if item[index_value] not in values_by_index:
            unique_list.append(item)
    return unique_list


def remove_from_dict(values_dict=dict, *args):
    updated_dict = []
    for value in values_dict:
        for arg in args:
            value.pop(arg.upper())
        updated_dict.append(value)
    return updated_dict


def get_rework_list_template(table_sheet: str, position: str, column_number: int, sheets_id: str):
    try:
        rework_sheet = data_communication.get_values(table_sheet, position, sheets_id=sheets_id)
        rework_list = []
        for line in rework_sheet['values']:
            if len(line) > 0:
                rework_list.append(line[column_number])
        rework_dict = {}
        for rework_name in rework_list:
            rework_dict[rework_name] = 0
        return rework_dict
    except Exception as error:
        logger.error(f'Could not load values from {table_sheet}\n{error}') 


def check_update_values_list(values_list: list, table_sheet: str, position: str, column_number: int, sheets_id: str):
    try:
        rework_breakage_matrix = data_communication.get_values(table_sheet, position, sheets_id=sheets_id)
        rework_breakage_list = [line[column_number] for line in rework_breakage_matrix['values']]
        values_to_update = []
        for value in values_list:
            if value not in rework_breakage_list:
                values_to_update.append(value)
        if len(values_to_update) > 0:
            data_communication.data_append_values(table_sheet, position, data_communication.transform_list_in_coloumn(values_to_update), sheets_id=sheets_id)
        return
    except Exception as error:
        logger.error('Could not check or update values due {error}')
        raise error


def list_by_key(values_list=list, key_name=str):
    list_by_key = set()
    for value_dict in values_list:
        list_by_key.add(value_dict[key_name])
    return list_by_key


def convert_rework_list(rework_list, template):
    rework_organized = []
    for rework_day in rework_list:
        rework_day_values = deepcopy(template)
        rework_day_organized = {}
        rework_day_organized['DATE'] = datetime.datetime.strftime(rework_day['DATE'], '%d/%m/%Y')
        for rework in rework_day['REWORK']:
            if rework['MOTIVO RETRABALHO'] in template.keys():
                rework_day_values[rework['MOTIVO RETRABALHO']] = int(rework['QT. RETRABALHO'])
        rework_day_organized.update(rework_day_values)
        rework_organized.append(rework_day_organized)
    return rework_organized


def rework_automation(event: threading.Event, config: dict):
    path = os.path.normpath(config['rework']['path'])
    path_done = os.path.normpath(config['rework']['path_done'])
    extension = config['rework']['extension']
    file_name_pattern = config['rework']['file_name_pattern']
    sheets_name = config['rework']['sheets_name']
    sheets_id = config['rework']['sheets_id']

    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, 'A:A', config['heat_map']['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    except Exception as error:
        logger.critical(f'Error loading table {sheets_name}')
        return


    if event.is_set():
        logger.info('Event set')
        return
    # Defining start and end date
    file_date = file_handler.file_list_last_date(path, extension, file_name_pattern, '%Y%m%d')
    if file_date == None:
        start_date = sheets_date_plus_one
    else:
        start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)

    logger.info(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
    logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))

    if not start_date == datetime.datetime.now().date():
        # Report extraction automation
        try:
            erp_volpe_handler.volpe_back_to_main()
            erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            erp_volpe_handler.volpe_open_window('Icon_Rework_Motive.png', 'Title_Rework_Motive.png')
            logger.info('Volpe rework started')

            if event.is_set():
                logger.info('Event set')
                return

            counter = 0
            report_date_start = start_date
            report_date_end = start_date
            while report_date_end <= end_date:
                try:
                    erp_volpe_handler.volpe_load_report(report_date_start, 
                                report_date_end, 
                                'Report_options',
                                'Procced.png',
                                'Production_date.png', 
                                'until.png', 
                                'Sheet_header.png',
                                date_from_dist=50, 
                                date_until_dist=35,
                                load_report_path='Images/Rework_motives')
                    if event.is_set():
                        logger.info('Event set')
                        return
                    erp_volpe_handler.volpe_save_report(f'REWORK_{datetime.datetime.strftime(report_date_start, "%Y%m%d")}', path)
                    logger.info(f'Date {datetime.datetime.strftime(report_date_start, "%d/%m/%Y")} done.')
                    report_date_start = report_date_start + datetime.timedelta(days=1)
                    report_date_end = report_date_end + datetime.timedelta(days=1)
                except Exception as error:
                    logger.warning(f'Error {error}')
                    if counter >= 10:
                        raise Exception('Error: Too many tries.')
                    erp_volpe_handler.volpe_back_to_main()
                    erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
                    erp_volpe_handler.volpe_open_window('Icon_Rework_Motive.png', 'Title_Rework_Motive.png')
                    counter = counter + 1
                if event.is_set():
                    logger.info('Event set')
                    return
        except Exception as error:
            logger.critical(f'General error: {error}')
            exit()

        # Data processing

    file_list = file_handler.file_list(path, extension)
    if len(file_list) > 0:
        try:
            rework_list = []
            motive_list = set()
            if event.is_set():
                logger.info('Event set')
                return
            for file in file_list:
                partial_list = file_handler.CSVtoList(join(path, file))
                file_date = data_organizer.retrieve_file_name_date(file, 'REWORK_', '%Y%m%d')
                rework_list.append({'DATE' : file_date, 'REWORK' : partial_list})
                for line in partial_list:
                    motive_list.add(line['MOTIVO RETRABALHO'])
                logger.info(f'{file} done')
            
            check_update_values_list(list(motive_list), 'Rework_Data', 'A:A', 0, sheets_id)
            rework_dict = get_rework_list_template('Rework_Data', 'C:C', 0, sheets_id)
            rework_organized = convert_rework_list(rework_list, rework_dict)

            if event.is_set():
                logger.info('Event set')
                return
            logger.debug('Sending to database')
            result = data_communication.data_append_values('REWORK' , 'A:Z', data_communication.transform_in_sheet_matrix(rework_organized), sheets_id=sheets_id)

            for file in file_list:
                file_handler.file_move_copy(path, path_done, file, False)

            logger.info(f"Done {result}")    
        except Exception as error:
            logger.error(error)
            event.set()
            return


def main(event: threading.Event, config: dict):
    rework_automation(event, config)
    return


def quit_func():
    logger.info('Quit pressed')
    event.set()
    return


'''
==================================================================================================================================

        Main        Main        Main        Main        Main        Main        Main        Main        Main        Main        

==================================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/config_volpe.json')
    except:
        logger.critical('Could not load config file')
        exit()

    event = threading.Event()
    keyboard.add_hotkey('esc', quit_func)

    for _ in range(3):
        main(event, config)
        if event.is_set():
            break

    logger.info('Done')

    
