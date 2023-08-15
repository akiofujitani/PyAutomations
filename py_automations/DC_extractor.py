import datetime, pyautogui, keyboard, os, calendar, logging
from data_modules import data_organizer, win_handler, erp_volpe_handler, file_handler, data_communication, json_config
from ntpath import join
from time import sleep
import tkinter.messagebox
from data_modules import log_builder as log
from datetime import datetime

logger = logging.getLogger('DC_extractor')

'''
================================================================================================================

    Automations     Automations     Automations     Automations     Automations     Automations     Automations

================================================================================================================
'''


def get_time(string_value):
    '''
    Convert Volpe our string ("HHhMM") to datetime returning false if not in correct format
    '''
    try:
        return datetime.datetime.strptime(string_value, '%Hh%M')
    except ValueError:
        return False


'''
==================================================================================================================

    Dataorganizers      Dataorganizers      Dataorganizers      Dataorganizers      Dataorganizers

==================================================================================================================
'''

def complete_date(dc_dict=dict, start_date=datetime.date, end_date=datetime.date) -> dict:
    pass


def done_file_move(path=str, done_path=str, extension=str):
    file_list = file_handler.file_list(path, extension)
    for file in file_list:
        file_handler.file_move_copy(path, done_path, file)
    return


def get_maximum_in_items(productivity_dict=dict):
    '''
    Get the maximum number of keys in dictionary
    '''
    maximum_values = set()
    for key in productivity_dict.keys():
        maximum_values.add(len(productivity_dict[key]))
    return sorted(maximum_values, reverse=True)[0]


def define_start_date(date_1, date_2):
    date_diff = date_1 - date_2
    start_date = date_1 - date_diff
    if start_date == date_1 or start_date == date_2:
        return start_date + datetime.timedelta(days=1)
    return start_date


'''
==================================================================================================================

    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    

==================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    try:
        config = json_config.load_json_config('c:/PyAutomations_Reports/dc_config.json')
    except:
        logger.error('Could not load config file')
        exit()


    extension_str = config['extension']
    file_name_pattern = config['file_name_pattern']
    sheets_date_pos = config['sheets_date_pos']
    sheets_id = config['sheets_id']
    status_jobtype_sheets_name = config['status_list']['sheets_name']

    # Selecting by job type
    # Free form or external (coating)

    for jobtype in config['job_type']:
        path = file_handler.check_create_dir(os.path.normpath(config['path_output'][jobtype]))
        path_done = file_handler.check_create_dir(os.path.normpath(config['path_done'][jobtype]))
        logger.info(config['job_type'][jobtype])
        logger.info(config['sheets_type_name'][jobtype])

        sheets_name = f'{config["sheets_name"]} {config["sheets_type_name"][jobtype]}'
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, sheets_date_pos, config['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)


        # Defining start and end date
        if not sheets_date_plus_one == datetime.datetime.now().date():
            file_date = file_handler.file_list_last_date(path, extension_str, file_name_pattern, '%Y%m%d')
            if file_date == None:
                start_date = sheets_date_plus_one
            else:
                start_date = define_start_date(sheets_date_plus_one, file_date)

            logger.info(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
            logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))

            type_list = config['job_type'][jobtype]


            # Running Volpe automation if needed

            if not start_date.date() == datetime.datetime.now().date():
                error_counter = 0
                try:
                    erp_volpe_handler.volpe_back_to_main()
                    erp_volpe_handler.volpe_load_tab('Tab_lab', 'Icon_Prod_Unit.png')
                    erp_volpe_handler.volpe_open_window('Icon_DC.png', 'Title_Delivery_control.png')
                    erp_volpe_handler.type_selector('Title_Delivery_control.png', 'Images/Delivery_control', *type_list)
                    counter = 0
                    report_date_end = start_date
                    while report_date_end < end_date:
                        if end_date > data_organizer.add_months_to_date(start_date, 1):
                            report_date_start = start_date
                            report_date_end = datetime.datetime(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1])
                            start_date = report_date_end + datetime.timedelta(days=1)
                        else:
                            report_date_start = start_date
                            report_date_end = end_date
                        try:
                            erp_volpe_handler.volpe_load_report(report_date_start,
                                                report_date_end, 
                                                'Report_options',
                                                'Procced.png',
                                                'Date_from.png',
                                                'Date_until.png',
                                                'Sheet_header.png',
                                                date_from_dist=30,
                                                date_until_dist=30,
                                                load_report_path='Images/Delivery_control')
                            erp_volpe_handler.volpe_save_report(f'{file_name_pattern}{datetime.datetime.strftime(report_date_start, "%Y%m%d")}', path)
                            logger.debug(f'Date {datetime.datetime.strftime(report_date_start, "%d/%m/%Y")} done.')
                        except Exception as error:
                            logger.warning(f'Error {error}')
                            if counter >= 5:
                                raise Exception('Error: Too many tries.')
                            erp_volpe_handler.volpe_back_to_main()
                            erp_volpe_handler.volpe_load_tab('Tab_lab', 'Icon_Prod_Unit.png')
                            erp_volpe_handler.volpe_open_window('Icon_Productivity_machine.png', 'Title_Machine_productivity.png')
                    # get_productivity(start_date, end_date, type_list, path, file_name_pattern)
                except Exception as error:
                    logger.error('Automation error: {error}')
                    erp_volpe_handler.volpe_back_to_main()



                # Data processing
                try:
                    file_list = file_handler.file_list(path, extension_str)
                    if len(file_list) > 0:
                        report_list = []
                        for file in file_list:
                            report_list = file_handler.CSVtoList(join(path, file))
                            ready_list = sorted(report_list, key=lambda value : datetime.datetime.strptime(value['DT.COMBINADA'], '%d/%m/%Y'))
                            sheet = data_communication.transform_in_sheet_matrix(ready_list)
                            data_communication.data_append_values(sheets_name ,'A:M', sheet, sheets_id=sheets_id)
                            file_handler.file_move_copy(path, path_done, file, False)
                            logger.info(f'{file} done')
                    logger.info("Done")
                except Exception as error:
                    logger.error(f'Error in data processing {error}')

