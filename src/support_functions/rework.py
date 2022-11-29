import win_handler, erp_volpe_handler, pyautogui, keyboard, datetime, calendar, file_handler, data_communication, data_organizer, json_config, os
from ntpath import join
from time import sleep
from copy import deepcopy

'''
==================================================================================================================================

        Volpe Automation        Volpe Automation        Volpe Automation        Volpe Automation        Volpe Automation

==================================================================================================================================
'''


def volpe_load_tab(tab_name, load_check_image):
    try:
        win_handler.activate_window('Volpe')
        erp_volpe_handler.volpe_tab_select(tab_name)
        win_handler.loading_wait(load_check_image)
        sleep(0.3)
        return
    except Exception as error:
        print('Volpe - load_tab error in {error}')
        raise error


def volpe_open_window(icon_name, window_name, path='Images', maximize=True):
    try:
        win_handler.icon_click(icon_name)
        sleep(0.5)
        win_pos = win_handler.image_search(window_name, path=path)
        sleep(0.5)
        if maximize:
            try:    
                win_handler.icon_click('Volpe_Maximize.png', confidence_value=0.7, region_value=(erp_volpe_handler.region_definer(win_pos.left - 15, win_pos.top - 15)))
                sleep(0.5)
            except:
                print('Window already maximized')
        return
    except Exception as error:
        print('Volpe - open_window {error}')
        raise error


def volpe_save_report(file_name, save_path):
    '''
    Volpe automation
    Save productivity values to file name and path arguments
    '''
    pyautogui.moveTo(10, 10)
    win_handler.icon_click('Icon_save.png')
    sleep(0.5)
    for i in range(5):
        keyboard.press_and_release('Down')
        sleep(0.5)
    pyautogui.press('enter')
    sleep(1)
    save_as_window = win_handler.image_search('Title_Save_as.png')
    if save_as_window:
        file_full_path = join(save_path, file_name)
        pyautogui.write(file_full_path)
        sleep(0.5)
        pyautogui.press(['tab', 'tab'])
        sleep(0.5)
        pyautogui.press('enter')
        sleep(1)
        msg_win_list = ['Question_mark.png', 'Exclamation_mark.png']
        for i in range(3):
            for image in msg_win_list:
                try:
                    sleep(0.7)
                    win_handler.image_search(image)
                    sleep(0.3)
                    if image == 'Exclamation_mark.png':
                        win_handler.icon_click('Yes_button.png')
                    if image == 'Question_mark.png':
                        win_handler.icon_click('No_button.png')
                except Exception as error:
                    print(f'Image not found {error}')
                    if i == 2:
                        break
        sleep(0.5)
    return


def volpe_load_report(date_start=datetime.datetime, 
            date_end=datetime.datetime,
            tab_name=str,
            date_from_image=str,
            date_until_image=str,
            report_load_wait=str,
            date_from_pos='Front',
            date_from_dist=25,
            date_until_pos='Front',
            date_until_dist=25,
            load_report_path='Images'):
    '''
    Volpe automation to load machine productivity report by date
    '''
    try:
        erp_volpe_handler.volpe_tab_select(tab_name, path=load_report_path)
        date_from = win_handler.image_search(date_from_image, path=load_report_path, confidence_value=0.95)
        win_handler.click_field(date_from, date_from_pos, distance=date_from_dist)
        sleep(0.3)
        pyautogui.click()
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.5)
        pyautogui.write(datetime.datetime.strftime(date_start, '%d%m%Y'))
        sleep(0.5)
        date_until = win_handler.image_search(date_until_image, path=load_report_path, confidence_value=0.95)
        win_handler.click_field(date_until, date_until_pos, distanceX=date_until_dist)
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.3)
        pyautogui.write(datetime.datetime.strftime(date_end, '%d%m%Y'))
        sleep(0.5)
        win_handler.icon_click('Procced.png', path=load_report_path)
        sleep(0.3)
        win_handler.loading_wait(report_load_wait, path=load_report_path)
        return
    except Exception as image_search_error:
        print(f'{image_search_error}')
        raise Exception(f'load_report error {image_search_error}')


def volpe_back_to_main():
    win_handler.activate_window('Volpe')
    button_list = ['Volpe_Close.png', 'Volpe_Close_Inactive.png', 'No_button.png', 'Ok_button.png']
    win_pos = win_handler.get_window_size()
    for i in range(5):
        for button in button_list:
            try:
                sleep(0.7)
                win_handler.icon_click(button, region_value=(erp_volpe_handler.region_definer(win_pos.left, win_pos.top + 20)))
            except Exception as error:
                print(f'Image not found {error}')
    keyboard.press_and_release('ctrl+e')
    return


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


def get_rework_list_template(table_sheet=str, position=str, column_number=int):
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
        print(f'Could not load values from {table_sheet}\n{error}') 


def check_update_values_list(values_list=list, table_sheet=str, position=str, column_number=int):
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
        print('Could not check or update values due {error}')
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


'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


if __name__ == '__main__':

    # volpe_back_to_main()
    try:
        config = json_config.load_json_config('config_volpe.json')
    except:
        print('Could not load config file')
        exit()

    path = os.path.normpath(config['rework']['path'])
    path_done = os.path.normpath(config['rework']['path_done'])
    extension = config['rework']['extension']
    file_name_pattern = config['rework']['file_name_pattern']
    sheets_name = config['rework']['sheets_name']
    sheets_id = config['rework']['sheets_id']

    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, 'A:A', config['heat_map']['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    except Exception as error:
        print(f'Error loading table {sheets_name}')
        quit()


    # Defining start and end date
    if not sheets_date_plus_one == datetime.datetime.now().date():
        file_date = file_handler.file_list_last_date(path, extension, file_name_pattern, '%Y%m%d')
        if file_date == None:
            start_date = sheets_date_plus_one
        else:
            start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)

        print(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
        print(datetime.datetime.strftime(end_date, '%d/%m/%Y'))

        # Report extraction automation
        try:
            # erp_volpe_handler.volpe_back_to_main()
            erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            volpe_open_window('Icon_Rework_Motive.png', 'Title_Rework_Motive.png')
            
            counter = 0
            report_date_start = start_date
            report_date_end = start_date
            while report_date_end < end_date:
                try:
                    volpe_load_report(report_date_start, 
                                report_date_end, 
                                'Report_options', 
                                'Production_date.png', 
                                'until.png', 
                                'Sheet_header.png', 
                                date_from_dist=50, 
                                date_until_dist=35,
                                load_report_path='Images/Rework_motives')
                    volpe_save_report(f'REWORK_{datetime.datetime.strftime(report_date_start, "%Y%m%d")}', path)
                    print(f'Date {datetime.datetime.strftime(report_date_start, "%d/%m/%Y")} done.')
                    report_date_start = report_date_start + datetime.timedelta(days=1)
                    report_date_end = report_date_end + datetime.timedelta(days=1)
                except Exception as error:
                    print(f'Error {error}')
                    if counter >= 10:
                        raise Exception('Error: Too many tries.')
                    volpe_back_to_main()
                    volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
                    volpe_open_window('Icon_Rework_Motive.png', 'Title_Rework_Motive.png')
                    counter = counter + 1
        except Exception as error:
            print(f'General error: {error}')
            exit()

        # Data processing

        file_list = file_handler.file_list(path, extension)
        rework_list = []
        motive_list = set()
        for file in file_list:
            partial_list = file_handler.CSVtoList(join(path, file))
            file_date = data_organizer.retrieve_file_name_date(file, 'REWORK_', '%Y%m%d')
            rework_list.append({'DATE' : file_date, 'REWORK' : partial_list})
            for line in partial_list:
                motive_list.add(line['MOTIVO RETRABALHO'])
            file_handler.file_move_copy(path, path_done, file, False)
            print(f'{file} done')
        
        check_update_values_list(list(motive_list), 'Rework_Data', 'A:A', 0)
        rework_dict = get_rework_list_template('Rework_Data', 'C:C', 0)
        rework_organized = convert_rework_list(rework_list, rework_dict)

        result = data_communication.data_append_values('REWORK' , 'A:Z', data_communication.transform_in_sheet_matrix(rework_organized), sheets_id=sheets_id)
        print('Almost')
        print("Done")
