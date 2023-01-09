from shutil import ExecError
import win_handler, erp_volpe_handler, pyautogui, keyboard, datetime, calendar, file_handler, data_communication, data_organizer, json_config, os
from ntpath import join
from time import sleep


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
                        pyautogui.press('s')
                    if image == 'Question_mark.png':
                        pyautogui.press('n')
                except Exception as error:
                    print(f'Image not found {error}')
        sleep(0.5)
    return


def volpe_load_report(start_date=datetime.datetime, 
            date_end=datetime.datetime,
            tab_name=str,
            confirm_button=str,
            date_from_image=str,
            date_until_image=str,
            report_load_wait=str,
            date_from_pos='Front',
            date_until_pos='Front',
            reference_pos_image=None,
            load_report_path='Images'):
    '''
    Volpe automation to load machine productivity report by date
    '''

    try:
        if not tab_name == None:
            erp_volpe_handler.volpe_tab_select(tab_name, path=load_report_path)
        if not reference_pos_image == None:
            reference_pos = win_handler.image_search(reference_pos_image, path=load_report_path, confidence_value=0.95)    
        date_from = win_handler.image_search(date_from_image, 
                            path=load_report_path, 
                            confidence_value=0.95,
                            region=(erp_volpe_handler.region_definer(reference_pos.left - 15, reference_pos.top - 15)) if reference_pos else '')
        win_handler.click_field(date_from, date_from_pos, distance=25)
        sleep(0.3)
        pyautogui.click()
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.5)
        pyautogui.write(datetime.datetime.strftime(start_date, '%d%m%Y'))
        sleep(0.5)
        date_until = win_handler.image_search(date_until_image, 
                            path=load_report_path, 
                            confidence_value=0.95, region=(erp_volpe_handler.region_definer(reference_pos.left - 15, reference_pos.top - 15)) if reference_pos else '')
        win_handler.click_field(date_until, date_until_pos, distance=25)
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.3)
        pyautogui.write(datetime.datetime.strftime(date_end, '%d%m%Y'))
        sleep(0.5)
        win_handler.icon_click(confirm_button, path=load_report_path)
        sleep(0.3)
        win_handler.loading_wait(report_load_wait, path=load_report_path)
        sleep(1)
        return
    except Exception as image_search_error:
        print(f'{image_search_error}')
        raise Exception(f'load_report error {image_search_error}')


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


def warranty_add_quantity(warranty_list):
    updated_warranty_list = []
    for warranty in warranty_list:
        temp_values = warranty
        temp_values['QUANTITY'] = 2 if warranty['LADO DO OLHO'] == 'AMBOS' else 1
        updated_warranty_list.append(temp_values)
    return updated_warranty_list


if __name__ == '__main__':
    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/config_volpe.json')
    except:
        print('Could not load config file')
        exit()

    path = file_handler.check_create_dir(os.path.normpath(config['warranty']['path']))
    path_done = file_handler.check_create_dir(os.path.normpath(config['warranty']['path_done']))
    extension = config['warranty']['extension']
    file_name_pattern = config['warranty']['file_name_pattern']
    sheets_name = config['warranty']['sheets_name']
    sheets_date_pos = config['warranty']['sheets_date_pos']
    sheets_id = config['warranty']['sheets_id']

    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, sheets_date_pos, config['heat_map']['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    except Exception as error:
        print(f'Error loading table {sheets_name}')
        quit()


    # Defining start and end date
    if not sheets_date_plus_one == datetime.datetime.now().date():
        try:
            temp_list = []
            file_date = None
            file_list = file_handler.file_list(path, extension)
            if len(file_list) > 0:
                for file in file_list:
                    temp_list = temp_list + file_handler.CSVtoList(join(path, file))
                file_date = file_handler.file_contents_last_date(temp_list, 'DT.PED GARANTIA')
                if sheets_date_plus_one > file_date:
                    file_handler.file_move_copy(path, path_done, file, False)
            if file_date == None:
                start_date = sheets_date_plus_one
            else:
                start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)
            
            start_date = start_date
            print(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
            print(datetime.datetime.strftime(end_date, '%d/%m/%Y'))
        except Exception as error:
            print(error)
            exit()
        # Report extraction automation

        if start_date.date() < end_date.date():
            erp_volpe_handler.volpe_back_to_main()
            volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            volpe_open_window('Icon_Warranty_control.png', 'Title_Warranty_Control.png')

            report_date_end = start_date
            while report_date_end < end_date:
                if end_date > add_months_to_date(start_date, 1):
                    report_start_date = start_date
                    report_date_end = datetime.datetime(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1])
                    start_date = report_date_end + datetime.timedelta(days=1)
                else:
                    report_start_date = start_date
                    report_date_end = end_date
                # image search for reference position.
                volpe_load_report(report_start_date, report_date_end, None,
                                        'Button_consult.png',
                                        'Date_from.png', 
                                        'Date_until.png', 
                                        'Volpe_Table_selected.png', 
                                        date_from_pos='Front',
                                        date_until_pos='Front', 
                                        load_report_path='Images/Warranty_Control', 
                                        reference_pos_image='Warranty_job.png')
                volpe_save_report(f'{file_name_pattern}{datetime.datetime.strftime(report_start_date, "%Y%m%d")}', path)
                erp_volpe_handler.volpe_back_to_main()

        # Data processing
        try:
            file_list = file_handler.file_list(path, extension)
            breakage_list = []
            for file in file_list:
                partial_list = file_handler.CSVtoList(join(path, file))
                updated_list = remove_from_dict(partial_list, *config['warranty']['remove_fields'])
                sorted_list = warranty_add_quantity(sorted(updated_list, key=lambda value : datetime.datetime.strptime(value['DT.PED GARANTIA'], '%d/%m/%Y')))
                sheet = data_communication.transform_in_sheet_matrix(sorted_list)
                data_communication.data_append_values(sheets_name ,'A:M', sheet, sheets_id=sheets_id)
                file_handler.file_move_copy(path, path_done, file, False)
                print(f'{file} done')
            print("Done")
        except Exception as error:
            print(f'Error in data processing {error}')
