import datetime, heat_map_classes, win_handler, erp_volpe_handler, pyautogui, keyboard, file_handler, data_communication, json_config, os, collections
from ntpath import join
from time import sleep


'''
================================================================================================================

    Automations     Automations     Automations     Automations     Automations     Automations     Automations

================================================================================================================
'''


def type_selector(window_name, path, *args) -> None:
    '''
    Select production type, will be moved to erp_volpe_hadler
    '''
    try:
        win_pos = win_handler.image_search(window_name, path=path)
        sleep(0.5)
        win_handler.icon_click('Three_dots_Button.png', path=path, region_value=(erp_volpe_handler.region_definer(win_pos.left, win_pos.top)))
        sleep(0.5)
        selec_type_win_pos = win_handler.image_search('title_select_type.png', path=path)
        win_handler.icon_click('discard_all_button.png', path=path, region_value=(erp_volpe_handler.region_definer(selec_type_win_pos.left, selec_type_win_pos.top)))
        discard_pos = win_handler.image_search('discard.png', path=path, region=(erp_volpe_handler.region_definer(selec_type_win_pos.left, selec_type_win_pos.top)))
        win_handler.click_field(discard_pos, 'Bellow')
        occult_inactive = win_handler.image_search('Occult_inactive.png', path=path)
        win_handler.click_field(occult_inactive, 'Bellow', distance=0)
        pos_x = discard_pos.left + 30
        pos_y = discard_pos.top + discard_pos.height + 5
        fields_list = []
        while not len(fields_list) == len(args):
            value = erp_volpe_handler.ctrl_d(pos_x, pos_y)
            sleep(0.5)
            if value in args:
                print('Match')
                fields_list.append(value)
                pyautogui.press('enter')
                sleep(0.2)
            else:
                keyboard.press_and_release('down')
                pos_y = pos_y + discard_pos.height + 3 if pos_y + discard_pos.height + 3 < occult_inactive.top - 10 else pos_y
                sleep(0.2)
        sleep(0.5)
        win_handler.icon_click('Select_button.png', path=path, region_value=(erp_volpe_handler.region_definer(selec_type_win_pos.left, selec_type_win_pos.top)))
        return
    except Exception as error:
        print(f'Error selecting type {error}')
        raise error


def expand_all(sheet_pos):
    '''
    Workaround to "Expand all" absense in Volpe machine productivity window
    Automation expands from botton to top (easier way) all values within "+" sign
    '''
    line_text = ''
    for _ in range(10):
        keyboard.press_and_release('Page Down')
        print('page down')
        sleep(0.2)
    while 'Total' not in line_text:
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


def machine_productivity_expand_all():
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
            expand_all(sheet_pos)
            expand_all(sheet_pos)
        except Exception as error:
            if 'ImageNotFound: Volpe_Table_selected.png' not in error[0]:
                raise Exception('Error expanding table')
        print('Expand all done')
        return
    except Exception as error:
        print(f'expand_all {error}')


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


def clean_status_dict(status_dict, sheets_name, search_range):
    '''
    Clean and transform dict in matrix like values.
    '''
    last_row_date = data_communication.get_last_date(sheets_name, search_range, '31/05/2022', sheets_id=sheets_id)
    status_dict_first_date = datetime.datetime.strptime(status_dict[0]['DATE'], '%d/%m/%Y')
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


def complete_date_in_list(status_dict):
    '''
    Get status values and complete missing dates.
    '''
    temp_list = {}
    for status in status_dict.keys():
        date_list = [datetime.datetime.strptime(date['DATE'], '%d/%m/%Y') for date in status_dict[status]]
        start_date = date_list[0]
        end_date = date_list[len(date_list) - 1]
        for_loop_date = start_date
        temp_date_list = []
        date_diff = end_date.date() - start_date.date()
        for _ in range(date_diff.days):
            if for_loop_date in date_list:
                for date_values in status_dict[status]:
                    if for_loop_date == datetime.datetime.strptime(date_values['DATE'], '%d/%m/%Y'):
                        temp_date = date_values
                        break
            else:
                temp_date = machine_with_date(for_loop_date.strftime('%Y%m%d'), heat_map_classes.machine('COUNTER'))
            temp_date_list.append(temp_date)
            for_loop_date = for_loop_date + datetime.timedelta(days=1)
        temp_list[status] = temp_date_list
    return temp_list



'''
==================================================================================================================

    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    

==================================================================================================================
'''


if __name__ == '__main__':
    try:
        config = json_config.load_json_config('C:/Users/fausto.akio/Documents/Reports/config_volpe.json')
    except:
        print('Could not load config file')
        exit()


    extension_str = config['heat_map']['extension']
    file_name_pattern = config['heat_map']['file_name_pattern']
    sheets_date_pos = config['heat_map']['sheets_date_pos']
    sheets_id = config['heat_map']['sheets_id']
    status_jobtype_sheets_name = config['heat_map']['status_list']['sheets_name']

    # Selecting by job type
    # Free form or external (coating)

    for jobtype in config['heat_map']['job_type']:
        path = file_handler.check_create_dir(os.path.normpath(config['heat_map']['path_output'][jobtype]))
        path_done = file_handler.check_create_dir(os.path.normpath(config['heat_map']['path_done'][jobtype]))
        print(config['heat_map']['job_type'][jobtype])
        print(config['heat_map']['sheets_type_name'][jobtype])

        status_jobtype = config['heat_map']['status_list'][jobtype]
        sheets_name = config["heat_map"]["sheets_type_name"][f'date_source_{config["heat_map"]["sheets_type_name"][jobtype]}']
        sheets_date_plus_one = data_communication.get_last_date(f'{sheets_name} {config["heat_map"]["sheets_type_name"][jobtype]}', sheets_date_pos, config['heat_map']['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
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

            type_list = config['heat_map']['job_type'][jobtype]


            # Running Volpe automation if needed

            if not start_date.date() == datetime.datetime.now().date():
                error_counter = 0
                try:
                    erp_volpe_handler.volpe_back_to_main()
                    erp_volpe_handler.volpe_load_tab('Tab_lab', 'Icon_Prod_Unit.png')
                    erp_volpe_handler.volpe_open_window('Icon_Productivity_machine.png', 'Title_Machine_productivity.png')
                    type_selector('Machine_productivity.png', 'Images/Machine_productivity', *type_list)
                    counter = 0
                    report_date_start = start_date
                    report_date_end = start_date
                    while report_date_end < end_date:
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
                                                load_report_path='Images/Machine_productivity')
                            machine_productivity_expand_all()
                            erp_volpe_handler.volpe_save_report(f'{file_name_pattern}{datetime.datetime.strftime(report_date_start, "%Y%m%d")}', path)
                            print(f'Date {datetime.datetime.strftime(report_date_start, "%d/%m/%Y")} done.')
                            report_date_start = report_date_start + datetime.timedelta(days=1)
                            report_date_end = report_date_end + datetime.timedelta(days=1)
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


                # Filtering and organizing values in csv
                try:
                    productivity_dict = convert_productivity(path, extension_str)
                    filled_productiviry_dict = fill_values(productivity_dict)
                    flatten_productivity = sum_values_by_status(filled_productiviry_dict)
                    status_dict = simple_dict_by_status(flatten_productivity)
                    completed_list = complete_date_in_list(status_dict)

                    # Storing data in sheets of csv file if error
                    count_status = 0
                    status_list_by_jobtype = data_communication.column_to_list(data_communication.get_values(status_jobtype_sheets_name , status_jobtype, sheets_id=sheets_id))
                    for status in status_dict.keys():
                        if status in status_list_by_jobtype:
                            count_status = count_status + 1
                            print(f'{status} started')
                            range_value = 'A:Z'
                            range_name = f'{status} {config["heat_map"]["sheets_type_name"][jobtype]}'
                            try:
                                status_dict_matrix = clean_status_dict(status_dict[status], range_name, range_value)
                                if len(status_dict_matrix) > 0:
                                    data_communication.data_append_values(range_name, range_value, status_dict_matrix, sheets_id=sheets_id)
                                for item in status_dict[status]:
                                    values = list(item.values())
                                    print(values)
                            except Exception as error:
                                print(f'Could not store values for {status}')
                                file_name = f'{count_status:02d}_{status}'
                                file_handler.listToCSV(status_dict[status], join(path_done, f'{file_name.replace("/", ".") if "/" in file_name else file_name}.csv'))
                                print(f'{status} saved to CSV due {error}')
                            print(f'{status} done')
                    done_file_move(path, path_done, extension_str)
                    print('Done')
                except Exception as error:
                    print(f'Error {error} ocurred')

