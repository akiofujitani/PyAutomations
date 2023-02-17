import datetime, data_organizer, win_handler, erp_volpe_handler, pyautogui, keyboard, file_handler, data_communication, json_config, os, calendar, logging
from ntpath import join
from time import sleep
import tkinter.messagebox
import logger as log

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


def machine_to_dict(status_name, machine):
    '''
    Convert machine object to dictionary
    '''
    machine_dict = {}
    machine_dict['STATUS'] = status_name
    machine_dict['MACHINE'] = machine.machine_name
    machine_dict.update(machine.lens_per_hour)
    return machine_dict


def machine_with_date(date, machine):
    '''
    
    '''
    machine_dict = {}
    machine_dict['DATE'] = datetime.datetime.strptime(date, '%Y%m%d').strftime('%d/%m/%Y')
    machine_dict['MACHINE'] = machine.machine_name
    machine_dict.update(machine.lens_per_hour)
    return machine_dict


def organized_values_to_simples_dict(organized_values=dict):
    '''
    Create list of simplified dictionaries to csv conversion
    '''
    simple_dict = []
    for status_name in organized_values.keys():
        for machine in organized_values[status_name]:
            simple_dict.append(machine_to_dict(status_name, machine))
    return simple_dict


def done_file_move(path=str, done_path=str, extension=str):
    file_list = file_handler.file_list(path, extension)
    for file in file_list:
        file_handler.file_move_copy(path, done_path, file)
    return


def simple_dict_by_status(productivity_dict=dict):
    '''
    Converts machine productivity dictionary by status to date
    '''
    simple_dict_by_status = {}
    for date_value in productivity_dict.keys():
        for status in productivity_dict[date_value].keys():
            if status not in simple_dict_by_status.keys():
                simple_dict_by_status[status] = []
            for machine in productivity_dict[date_value][status]:
                simple_dict_by_status[status].append(machine_with_date(date_value, machine))
    return simple_dict_by_status


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
    logger = log.logger(logging.getLogger())
    try:
        config = json_config.load_json_config('C:/Users/fausto.akio/Documents/Reports/config_volpe.json')
    except:
        print('Could not load config file')
        exit()


    extension_str = config['dc']['extension']
    file_name_pattern = config['dc']['file_name_pattern']
    sheets_date_pos = config['dc']['sheets_date_pos']
    sheets_id = config['dc']['sheets_id']
    status_jobtype_sheets_name = config['dc']['status_list']['sheets_name']

    # Selecting by job type
    # Free form or external (coating)

    for jobtype in config['dc']['job_type']:
        path = file_handler.check_create_dir(os.path.normpath(config['dc']['path_output'][jobtype]))
        path_done = file_handler.check_create_dir(os.path.normpath(config['dc']['path_done'][jobtype]))
        print(config['dc']['job_type'][jobtype])
        print(config['dc']['sheets_type_name'][jobtype])

        status_jobtype = config['dc']['status_list'][jobtype]
        sheets_name = config["dc"]["sheets_type_name"][f'date_source_{config["dc"]["sheets_type_name"][jobtype]}']
        sheets_date_plus_one = data_communication.get_last_date(f'{sheets_name} {config["dc"]["sheets_type_name"][jobtype]}', sheets_date_pos, config['dc']['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)


        # Defining start and end date
        if not sheets_date_plus_one == datetime.datetime.now().date():
            file_date = file_handler.file_list_last_date(path, extension_str, file_name_pattern, '%Y%m%d')
            if file_date == None:
                start_date = sheets_date_plus_one
            else:
                start_date = define_start_date(sheets_date_plus_one, file_date)

            print(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
            print(datetime.datetime.strftime(end_date, '%d/%m/%Y'))

            type_list = config['dc']['job_type'][jobtype]


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
                            print(f'Date {datetime.datetime.strftime(report_date_start, "%d/%m/%Y")} done.')
                        except Exception as error:
                            print(f'Error {error}')
                            if counter >= 5:
                                raise Exception('Error: Too many tries.')
                            erp_volpe_handler.volpe_back_to_main()
                            erp_volpe_handler.volpe_load_tab('Tab_lab', 'Icon_Prod_Unit.png')
                            erp_volpe_handler.volpe_open_window('Icon_Productivity_machine.png', 'Title_Machine_productivity.png')
                    # get_productivity(start_date, end_date, type_list, path, file_name_pattern)
                except Exception as error:
                    print('Automation error: {error}')
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
                            print(f'{file} done')
                    print("Done")
                except Exception as error:
                    print(f'Error in data processing {error}')

