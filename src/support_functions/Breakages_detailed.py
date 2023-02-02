import win_handler, erp_volpe_handler, pyautogui, keyboard, datetime, calendar, file_handler, data_communication, data_organizer, json_config, os, logger
from ntpath import join
from time import sleep


logger = logger.logger('breakages_detailed')

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
        logger.error(f'Volpe - load_tab error in {error}')
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
                logger.warning('Window already maximized')
        return
    except Exception as error:
        logger.error('Volpe - open_window {error}')
        raise error


def volpe_save_report(file_name, save_path):
    '''
    Volpe automation
    Save productivity values to file name and path arguments
    '''
    pyautogui.moveTo(10, 10)
    win_handler.icon_click('Icon_save.png')
    sleep(0.5)
    for _ in range(5):
        keyboard.press_and_release('Down')
        sleep(0.5)
    pyautogui.press('enter')
    sleep(1)
    save_as_window = win_handler.image_search('Title_Save_as.png', confidence_value=0.7)
    if save_as_window:
        file_full_path = join(save_path, file_name)
        pyautogui.write(file_full_path)
        sleep(0.5)
        pyautogui.press(['tab', 'tab'])
        sleep(0.5)
        pyautogui.press('enter')
        sleep(1)
        msg_win_list = ['Question_mark.png', 'Exclamation_mark.png']
        for _ in range(3):
            for image in msg_win_list:
                try:
                    sleep(0.7)
                    win_handler.image_search(image)
                    sleep(0.3)
                    if image == 'Exclamation_mark.png':
                        win_handler.icon_click('Button_yes.png')
                    if image == 'Question_mark.png':
                        win_handler.icon_click('Button_No.png')
                except Exception as error:
                    logger.error(f'Image not found {error}')
        sleep(0.5)
    return


def volpe_load_report(start_date=datetime.datetime, 
            date_end=datetime.datetime,
            tab_name=str,
            date_from_image=str,
            date_until_image=str,
            report_load_wait=str,
            date_from_pos='Front',
            date_until_pos='Front',
            load_report_path='Images'):
    '''
    Volpe automation to load machine productivity report by date
    '''
    try:
        erp_volpe_handler.volpe_tab_select(tab_name, path=load_report_path)
        date_from = win_handler.image_search(date_from_image, path=load_report_path, confidence_value=0.95)
        win_handler.click_field(date_from, date_from_pos, distance=25)
        sleep(0.3)
        pyautogui.click()
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.5)
        pyautogui.write(datetime.datetime.strftime(start_date, '%d%m%Y'))
        sleep(0.5)
        date_until = win_handler.image_search(date_until_image, path=load_report_path, confidence_value=0.95)
        win_handler.click_field(date_until, date_until_pos, distance=25)
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
        logger.error(f'{image_search_error}')
        raise Exception(f'load_report error {image_search_error}')


'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def create_update_motive_list(breakage_list):
    logger.info('Creating motive list')
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

# Move to data organizer
def breakage_date_hour(values_dict=dict):
    key_name = 'Dt.Perda'
    updated_list = []
    for value in values_dict:
        date_time = datetime.datetime.strptime(value[key_name.upper()], '%d/%m/%Y %H:%M:%S')
        value.pop(key_name.upper())
        value[key_name.upper()] = datetime.datetime.strftime(date_time, '%d/%m/%Y')
        value['H.PERDA'] = datetime.datetime.strftime(date_time, '%H:%M:%S')
        updated_list.append(value)
    return updated_list


'''
==================================================================================================================================

        Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    Main    

==================================================================================================================================
'''


if __name__ == '__main__':
        # volpe_back_to_main()
    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/config_volpe.json')
    except:
        logger.critical('Could not load config file')
        exit()

    path = os.path.normpath(config['breakage']['path'])
    path_done = os.path.normpath(config['breakage']['path_done'])
    extension = config['breakage']['extension']
    file_name_pattern = config['breakage']['file_name_pattern']
    sheets_name = config['breakage']['sheets_name']
    sheets_date_pos = config['breakage']['sheets_date_pos']
    sheets_id = config['breakage']['sheets_id']


    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, 
                    sheets_date_pos, 
                    config['heat_map']['minimum_date'], sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    except Exception as error:
        logger.error(f'Error loading table {sheets_name}')
        quit()


    # Defining start and end date
    if not sheets_date_plus_one == datetime.datetime.now().date():
        file_list = file_handler.file_list(path, extension)
        file_date = None
        if len(file_list) > 0:
            for file in file_list:
                file_date = file_handler.file_contents_last_date(file_handler.CSVtoList(join(path, file)), 'DT.PERDA', time_format='%d/%m/%Y %H:%M:%S') + datetime.timedelta(days=1)
        if file_date == None:
            start_date = sheets_date_plus_one
        else:
            start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)

        logger.info(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
        logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))

        # Report extraction automation

        if start_date.date() <= (datetime.datetime.now().date() - datetime.timedelta(days=1)):
            erp_volpe_handler.volpe_back_to_main()
            volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            volpe_open_window('Icon_Detailed_breakages.png', 'Title_Detailed_Breakages.png')

            report_date_end = start_date
            while report_date_end < end_date:
                if end_date > data_organizer.add_months_to_date(start_date, 1):
                    report_start_date = start_date
                    report_date_end = datetime.datetime(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1])
                    start_date = report_date_end + datetime.timedelta(days=1)
                else:
                    report_start_date = start_date
                    report_date_end = end_date
                volpe_load_report(report_start_date, report_date_end, 'Report_options', 'until.png', 'until.png', 'Sheet_Header.png', date_from_pos='Back', load_report_path='Images/Detailed_Breakages')
                volpe_save_report(f'{file_name_pattern}{datetime.datetime.strftime(report_start_date, "%Y%m%d")}', path)

        # Data processing
        try:
            file_list = file_handler.file_list(path, extension)
            if len(file_list) > 0:
                breakage_list = []
                motive_list = []
                for file in file_list:
                    partial_list = file_handler.CSVtoList(join(path, file))
                    updated_list = remove_from_dict(partial_list, *config['breakage']['remove_fields'])
                    ready_list = sorted(breakage_date_hour(updated_list), key=lambda value : datetime.datetime.strptime(value['DT.PERDA'], '%d/%m/%Y'))
                    sheet = data_communication.transform_in_sheet_matrix(ready_list)
                    data_communication.data_append_values(sheets_name ,'A:Z', sheet, sheets_id=sheets_id)
                    file_handler.file_move_copy(path, path_done, file, False)
                    logger.info(f'{file} done')
            logger.info("Done")
        except Exception as error:
            logger.error(f'Error in data processing {error}')
