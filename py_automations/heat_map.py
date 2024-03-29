import datetime, heat_map_classes, pyautogui, keyboard, os, logging, threading
from data_modules import win_handler, erp_volpe_handler, file_handler, data_communication, json_config
from data_modules import log_builder as log
from ntpath import join
from time import sleep

logger = logging.getLogger('heat_map')


'''
================================================================================================================

    Automations     Automations     Automations     Automations     Automations     Automations     Automations

================================================================================================================
'''


def expand_all(event: threading.Event, sheet_pos):
    '''
    Workaround to "Expand all" absense in Volpe machine productivity window
    Automation expands from botton to top (easier way) all values within "+" sign
    '''
    line_text = ''
    try:
        total = win_handler.image_search('Sheet_Total.png', path='Images/Machine_productivity')
    except Exception as error:
        logger.debug(f'Error "Total" search: {error}')
    if total:
        for _ in range(10):
            keyboard.press_and_release('Page Down')
            logger.debug('page down')
            sleep(0.2)
        while 'Total' not in line_text:
            if event.is_set():
                return
            selected_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(sheet_pos.left - 15, sheet_pos.top)))
            line_text = erp_volpe_handler.get_text_square(selected_pos.left + selected_pos.width, selected_pos.top, sheet_pos.width, selected_pos.height + 2)
            if '+' in line_text:
                pyautogui.doubleClick(selected_pos.left + 15, selected_pos.top + 6)
            elif '+' in erp_volpe_handler.ctrl_d(selected_pos.left + 15, selected_pos.top + 4):
                pyautogui.doubleClick(selected_pos.left + 15, selected_pos.top + 6)
            sleep(0.3)
            keyboard.press_and_release('Up')
            sleep(0.5)
    return


def machine_productivity_expand_all(event: threading.Event):
    '''
    Workaround to "Expand all" absense in Volpe machine productivity window
    Automation expands values one by one
    '''
    sleep(2)
    try:
        sheet_pos = win_handler.image_search('Sheet_header.png', path='Images/Machine_productivity')
        selected_pos = win_handler.image_search('Volpe_Table_selected.png', confidence_value=0.8, region=(erp_volpe_handler.region_definer(sheet_pos.left - 15, sheet_pos.top)))
        win_handler.click_field(selected_pos, 'Front')
        sleep(0.5)
        try:
            expand_all(event, sheet_pos)
            expand_all(event, sheet_pos)
        except Exception as error:
            if 'ImageNotFound: Volpe_Table_selected.png' not in error[0]:
                raise Exception('Error expanding table')
        logger.info('Expand all done')
        return
    except Exception as error:
        logger.error(f'expand_all {error}')


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


def organize_productivity_line(productivity_dict=dict):
    '''
    Convert machine productivity in dictionary delimeted by status with machines inside
    '''
    organized_values = {}
    machines_list = []
    new_machine = ''
    temp_parent_group = ''
    temp_name = ''
    counter = 0
    for line in productivity_dict:
        hour = get_time(line['AGRUPAMENTO'])
        if line['AGRUPAMENTO'] == 'Total':
            pass
        elif hour == False:
            counter = counter + 1
            if counter == 2:
                if len(machines_list) > 0:
                    organized_values[temp_parent_group] = machines_list
                    machines_list = []
                temp_parent_group = temp_name
                new_machine = heat_map_classes.machine(line['AGRUPAMENTO'])
                counter = 0
            else:
                if new_machine:
                    machines_list.append(new_machine)
                    new_machine = ''
                temp_name = line['AGRUPAMENTO']
        else:
            counter = 0
            if not new_machine:
                new_machine = heat_map_classes.machine(temp_name)
            new_machine.define_lens_per_hour(hour.strftime('%H:%M'), line['LENTES'])
    organized_values[temp_parent_group] = machines_list
    return organized_values


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


def convert_productivity(path=str, extension=str):
    '''
    List all machine productivity data files in path 
    Converts it to dictionary
    '''
    productivity_dict = {}
    file_list = file_handler.file_list(path, extension)
    if len(file_list) < 1:
        raise Exception(f'No files found in {path}')
    for file in file_list:
        csv_data = file_handler.CSVtoList(join(path, file))
        data_organized = organize_productivity_line(csv_data)
        productivity_date = file.split('.')[0].split('_')[2]
        productivity_dict[productivity_date] = data_organized
    return productivity_dict


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


def create_dummy_production(productivity_dict=dict):
    '''
    Create an entire list of machine with empty values for non weekdays.
    '''
    num_values = get_maximum_in_items(productivity_dict)
    for key in productivity_dict.keys():
        if len(productivity_dict[key]) == num_values:
            headers_list = productivity_dict[key].keys()
    dummy_dict = {}
    dummy_machine_list = []
    dummy_machine_list.append(heat_map_classes.machine('EMPTY'))
    for header in headers_list:
        dummy_dict[header] = dummy_machine_list
    return dummy_dict


def fill_values(productivity_dict=dict):
    '''
    Fill missing status with empty values for csv generation and simplier sheets append.
    '''
    status_number = get_maximum_in_items(productivity_dict)
    dummy_machine_list = create_dummy_production(productivity_dict)
    for key in productivity_dict.keys():
        if len(productivity_dict[key]) == 1:
            productivity_dict[key] = dummy_machine_list
        elif not len(productivity_dict[key]) == status_number:
            for dummy_key in dummy_machine_list.keys():
                if dummy_key not in productivity_dict[key].keys():
                    productivity_dict[key][dummy_key] = dummy_machine_list[dummy_key]
    return productivity_dict


def get_maximum_in_items(productivity_dict=dict):
    '''
    Get the maximum number of keys in dictionary
    '''
    maximum_values = set()
    for key in productivity_dict.keys():
        maximum_values.add(len(productivity_dict[key]))
    return sorted(maximum_values, reverse=True)[0]


def sum_values_by_status(productivity_dict=dict):
    '''
    Sum all the values per hour in machines inside each status.
    '''
    productivity_sum = {}

    for date_key in productivity_dict.keys():
        day_production = {}
        for status in productivity_dict[date_key].keys():
            new_machine = heat_map_classes.machine()
            for machine in productivity_dict[date_key][status]:
                hour_production_dict = machine.lens_per_hour
                for hour in hour_production_dict.keys():
                    new_machine.add_lens_per_hour(hour, hour_production_dict[hour])
            day_production[status] = [new_machine]
        productivity_sum[date_key] = day_production
    return productivity_sum


def clean_status_dict(status_dict, sheets_name, search_range, sheets_id):
    '''
    Clean and transform dict in matrix like values.
    '''
    last_row_date = data_communication.get_last_date(sheets_name, search_range, '31/05/2022', sheets_id=sheets_id)
    status_dict_first_date = datetime.datetime.strptime(status_dict[0]['DATE'], '%d/%m/%Y').date()
    date_difference = status_dict_first_date - last_row_date
    if not date_difference.days == 1:
        if date_difference < datetime.timedelta(days=1):
            for _ in range(abs(date_difference.days) + 1):
                status_dict.pop(0)
        else:
            temp_status_dict = status_dict
            status_dict = []
            between_date = last_row_date
            for _ in range(date_difference.days - 1):
                between_date = between_date + datetime.timedelta(days=1)
                status_dict.append(machine_with_date(between_date.strftime('%Y%m%d'), heat_map_classes.machine('COUNTER')))
            status_dict = status_dict + temp_status_dict
    if not len(status_dict) == 0:
        return data_communication.transform_in_sheet_matrix(status_dict)


def define_start_date(date_1, date_2):
    date_diff = date_1 - date_2
    start_date = date_1 - date_diff
    if start_date == date_1 or start_date == date_2:
        return start_date + datetime.timedelta(days=1)
    return start_date


def complete_date_in_list(status_dict=dict, status_list_by_job_type=list):
    '''
    Get status values and complete missing dates.
    '''

    #get first and last date
    start_date = None
    end_date = None
    for value in status_dict.values():
        first_date = datetime.datetime.strptime(value[0]['DATE'], '%d/%m/%Y').date()
        last_date = datetime.datetime.strptime(value[-1]['DATE'], '%d/%m/%Y').date()
        if start_date == None or first_date < start_date:
            start_date = first_date
        if end_date == None or last_date > end_date:
            end_date = last_date
    date_diff = (end_date - start_date) + datetime.timedelta(days=1)

    # Merge status
    status_set = set(status_dict.keys()).union(set(status_list_by_job_type))

    temp_list = {}
    for status in status_set:
        for_loop_date = start_date
        temp_date_list = []
        if status in status_dict.keys():
            date_list = [datetime.datetime.strptime(value['DATE'], '%d/%m/%Y').date() for value in status_dict[status]]
            for _ in range(date_diff.days):
                if for_loop_date in date_list:
                    for value in status_dict[status]:
                        if for_loop_date == datetime.datetime.strptime(value['DATE'], '%d/%m/%Y').date():
                            temp_date = value
                else:
                    temp_date = machine_with_date(for_loop_date.strftime('%Y%m%d'), heat_map_classes.machine('COUNTER'))
                temp_date_list.append(temp_date)
                for_loop_date = for_loop_date + datetime.timedelta(days=1)
        else:
            for_loop_date = start_date
            for _ in range(date_diff.days):
                temp_date_list.append(machine_with_date(for_loop_date.strftime('%Y%m%d'), heat_map_classes.machine('COUNTER')))
                for_loop_date = for_loop_date + datetime.timedelta(days=1)
        temp_list[status] = temp_date_list
    return temp_list





def main(event: threading.Event, config: dict):
    extension_str = config['extension']
    file_name_pattern = config['file_name_pattern']
    sheets_date_pos = config['sheets_date_pos']
    sheets_id = config['sheets_id']
    status_jobtype_sheets_name = config['status_list']['sheets_name']
    number_of_tries = int(config['number_of_tries'])

    # Selecting by job type
    # Free form or external (coating)

    for jobtype in config['job_type']:
        if event.is_set():
            logger.info('Event set')
            return

        # Configuration load
        path = file_handler.check_create_dir(os.path.normpath(config['path_output'][jobtype]))
        path_done = file_handler.check_create_dir(os.path.normpath(config['path_done'][jobtype]))
        logger.debug(config['job_type'][jobtype])
        logger.debug(config['sheets_type_name'][jobtype])

        status_jobtype = config['status_list'][jobtype]
        sheets_name = config["sheets_type_name"][f'date_source_{config["sheets_type_name"][jobtype]}']

        error_counter = 0
        while error_counter <= number_of_tries:
            error_counter += 1
            if event.is_set():
                logger.info('Event set')
                return
            
            #Date definer
            sheets_date_plus_one = data_communication.get_last_date(f'{sheets_name} {config["sheets_type_name"][jobtype]}', sheets_date_pos, config['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
            end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)

            if not sheets_date_plus_one == datetime.datetime.now().date():
                start_date = sheets_date_plus_one
                file_date = file_handler.file_list_last_date(path, extension_str, file_name_pattern, '%Y%m%d')
                if file_date:
                    start_date = define_start_date(sheets_date_plus_one, file_date)

                logger.debug(f"Start date {datetime.datetime.strftime(start_date, '%d/%m/%Y')}")
                logger.debug(f"End date {datetime.datetime.strftime(end_date, '%d/%m/%Y')}")

                type_list = config['job_type'][jobtype]


                # Running Volpe automation if needed

                if not start_date == datetime.datetime.now().date():
                    try:
                        erp_volpe_handler.volpe_back_to_main()
                        erp_volpe_handler.volpe_load_tab('Tab_lab', 'Icon_Prod_Unit.png')
                        erp_volpe_handler.volpe_open_window('Icon_Productivity_machine.png', 'Title_Machine_productivity.png')
                        erp_volpe_handler.type_selector('Machine_productivity.png', 'Images/Machine_productivity', *type_list)
                        counter = 0
                        report_date_start = start_date
                        report_date_end = start_date
                        while report_date_end <= end_date:
                            try:
                                if event.is_set():
                                    logger.info('Event set')
                                    return
                                erp_volpe_handler.volpe_load_report(report_date_start,
                                                    report_date_end, 
                                                    'Report_options',
                                                    'Procced.png',
                                                    'Date_from.png',
                                                    'Date_until.png',
                                                    'Sheet_header.png',
                                                    date_from_dist=30,
                                                    date_until_dist=30,
                                                    load_report_path='Images/Machine_productivity')
                                machine_productivity_expand_all(event)
                                erp_volpe_handler.volpe_save_report(f'{file_name_pattern}{datetime.datetime.strftime(report_date_start, "%Y%m%d")}', path)
                                logger.info(f'Date {datetime.datetime.strftime(report_date_start, "%d/%m/%Y")} done.')
                                report_date_start = report_date_start + datetime.timedelta(days=1)
                                report_date_end = report_date_end + datetime.timedelta(days=1)
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
                        try:
                            erp_volpe_handler.volpe_back_to_main()
                        except Exception as error:
                            logger.error(error)


                # Filtering and organizing values in csv
                if len(file_handler.file_list(path, extension_str)) > 0:
                    if event.is_set():
                        logger.info('Event set')
                        return
                    try:
                        status_list_by_jobtype = data_communication.column_to_list(data_communication.get_values(status_jobtype_sheets_name , status_jobtype, sheets_id=sheets_id))
                        
                        productivity_dict = convert_productivity(path, extension_str)
                        filled_productiviry_dict = fill_values(productivity_dict)
                        flatten_productivity = sum_values_by_status(filled_productiviry_dict)
                        status_dict = simple_dict_by_status(flatten_productivity)
                        completed_list = complete_date_in_list(status_dict, status_list_by_jobtype)

                        # Storing data in sheets of csv file if error
                        count_status = 0
                        status_list_by_jobtype = data_communication.column_to_list(data_communication.get_values(status_jobtype_sheets_name , status_jobtype, sheets_id=sheets_id))
                        for status in completed_list.keys():
                            if status in status_list_by_jobtype:
                                count_status = count_status + 1
                                logger.info(f'{status} started')
                                range_value = 'A:Z'
                                range_name = f'{status} {config["sheets_type_name"][jobtype]}'
                                try:
                                    status_dict_matrix = clean_status_dict(completed_list[status], range_name, range_value, sheets_id)
                                    if len(status_dict_matrix) > 0:
                                        data_communication.data_append_values(range_name, range_value, status_dict_matrix, sheets_id=sheets_id)
                                    for item in completed_list[status]:
                                        values = list(item.values())
                                        logger.debug(values)
                                except Exception as error:
                                    logger.warning(f'Could not store values for {status}')
                                    file_name = f'{count_status:02d}_{status}'
                                    file_handler.listToCSV(completed_list[status], join(path_done, f'{file_name.replace("/", ".") if "/" in file_name else file_name}.csv'))
                                    logger.error(f'{status} saved to CSV due {error}')
                                logger.debug(f'{status} done')
                        done_file_move(path, path_done, extension_str)
                        logger.info('Done')
                    except Exception as error:
                        logger.error(f'Error {error} ocurred')


def quit_func():
    logger.info('Quit pressed')
    event.set()
    return

'''
==================================================================================================================

    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    

==================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/heat_map.json')
    except:
        logger.critical('Could not load config file')
        exit()

    event = threading.Event()
    keyboard.add_hotkey('space', quit_func)


    for _ in range(3):
        if event.is_set():
            break
        thread = threading.Thread(target=main, args=(event, config, ), name='heat_map')
        thread.start()
        thread.join()

    logger.debug('Done')


    

