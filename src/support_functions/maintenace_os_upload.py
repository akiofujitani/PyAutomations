import win_handler, erp_volpe_handler, pyautogui, keyboard, datetime, file_handler, json_config, pdf_splitting, pytesseract_image, os
from ntpath import join
from time import sleep


def convert_to_OS_list(file_list=list):
    OS_list = {}
    for file in file_list:
        name_split = file.split('.' if '_' not in file else '_')
        if name_split[0] in OS_list.keys():
            temp_list = OS_list[name_split[0]]
            temp_list.append(file)
            OS_list[name_split[0]] = temp_list
        else:
            OS_list[name_split[0]] = [file]
    return OS_list


def check_appontments(finalize_task=False):
    appointment_win = erp_volpe_handler.enter_appointments()
    sleep(0.5)
    try:
        win_handler.image_search('Appoint_Final.png', 
                            region=(erp_volpe_handler.region_definer(appointment_win.left, appointment_win.top)), 
                            path='Images/Maintenance_OS')
        print('OS finalized')
        result = True        
    except Exception as error:
        print(f'Task no finalized. {error}')
        if finalize_task:
            win_handler.icon_click('Finalize_task_button.png',  path='Images/Maintenance_OS')
            sleep(0.5)
            close_confirmation(3, 'Yes_button.png', 'Ok_button.png', path='Images/Maintenance_OS')
            return True
        result = False
    win_handler.icon_click('Volpe_Fechar.png',  path='Images/Maintenance_OS')
    sleep(0.5)
    return result


def select_table(window_image=str, table_header=str, pos_x=int, pos_y=int):
    try:
        prog_tec_win = win_handler.image_search(window_image)
        table_pos = win_handler.image_search(table_header, 
                        region=(erp_volpe_handler.region_definer(prog_tec_win.left, prog_tec_win.top)), 
                        path='Images/Maintenance_OS')
        win_handler.click_field(table_pos, distanceX=pos_x, distanceY=pos_y)
    except Exception as error:
        print('{error}.\n Could not select table')
        raise error


def finalize_unfinalize_os(status_number=int, cancel_motive=str):
    try:
        select_table('Windows_Prog_Tec_man.png', 'Volpe_Prog_tec_Main_row.png', 50, 100)
        sleep(0.5)
        pyautogui.press('s')
        sleep(0.5)
        win_handler.image_search('Status_os.png', path='Images/Maintenance_OS')
        pyautogui.press(str(status_number))
        sleep(0.3)
        pyautogui.press('Tab')
        sleep(0.3)
        match status_number:
            case 1:
                pyautogui.write(cancel_motive)
                sleep(0.5)
                pyautogui.press('Tab')
                sleep(0.5)
                pyautogui.write(datetime.datetime.strftime(datetime.datetime.now(), '%d%m%Y%H%m%S'))
                sleep(0.5)
                pyautogui.press('tab')
            case 2:
                pyautogui.write(datetime.datetime.strftime(datetime.datetime.now(), '%d%m%Y%H%m%S'))
                sleep(0.5)
                pyautogui.press('tab')  
        sleep(0.5)
        win_handler.icon_click('Icon_OK.png')
        sleep(1)
        close_confirmation(3, 'Yes_button.png', 'Ok_button.png', path='Images/Maintenance_OS')
        return
    except Exception as error:
        print(f'Could not find {error}')
        raise error


def close_confirmation(number_of_cicles, *args, path='images'):
    for i in range(number_of_cicles):
        for image in args:
            try:
                win_handler.icon_click(image, confidence_value=1, path=path)
                sleep(0.5)
            except Exception as error:
                print(f'{error} not found')
    return


def load_file(path, file):
    try:
        win_handler.image_search('title_Open.png')
        sleep(0.5)
        pyautogui.write(join(path, file))
        sleep(0.5)
        pyautogui.press(['tab', 'tab'])
        sleep(1)
        pyautogui.press('enter')
        sleep(0.5)
        return
    except Exception as error:
        print(f'Cound not find {error}')
        raise error


def uploaded_files_list():
    try:
        table_pos = win_handler.image_search('table_header_atacched_items.png', path='Images/Maintenance_OS')
        selec_pos = win_handler.image_search('Volpe_Table_selected.png', 
                                confidence_value=1.0, 
                                region=(erp_volpe_handler.region_definer(table_pos.left - 20, table_pos.top)), 
                                path='Images/Maintenance_OS') 
        repeated_value = ''
        old_value = ''
        files_list = []
        while not repeated_value:
            win_handler.click_field(selec_pos, distanceX=30)
            new_value = erp_volpe_handler.ctrl_d(selec_pos.left + 30, selec_pos.top)
            if not new_value == old_value:
                files_list.append(new_value)
                old_value = new_value
                keyboard.press_and_release('down')
                selec_pos = win_handler.image_search('Volpe_Table_selected.png', 
                                confidence_value=1.0, 
                                region=(erp_volpe_handler.region_definer(table_pos.left - 20, table_pos.top)), 
                                path='Images/Maintenance_OS') 
            else:
                repeated_value = True
        return files_list
    except Exception as error:
        print(f'No files uploaded {error}')
        return


def rename_files(source_path, destin_path, error_path, file):
    os_number = pytesseract_image.get_os_number(source_path, file)
    if os_number.__eq__('Not found') or len(os_number) < 4:
        file_handler.fileMoveRename(source_path, error_path, file, file)
    else:
        file_handler.fileMoveRename(source_path, destin_path, file, f'{os_number}.pdf')
    return


if __name__ == '__main__':
    try:
        config = json_config.load_json_config('maintenance_config.json')
    except:
        print('Could not find or read config file')
        exit()


    # Get raw pdfs, split and rename

    path_raw = os.path.normpath(config['split_ocr']['raw'])
    path_ocr_error = os.path.normpath(config['split_ocr']['error'])
    path_rename = os.path.normpath(config['split_ocr']['rename'])
    path_ready = os.path.normpath(config['split_ocr']['ready'])
    path_split_done = os.path.normpath(config['split_ocr']['done'])
    path_raw_extension = os.path.normpath(config['split_ocr']['extension'])
    
    raw_file_list = file_handler.file_list(path_raw, path_raw_extension)
    for raw_file in raw_file_list:
        pdf_splitting.pdf_split(join(path_raw, raw_file), path_rename, 'Temp_num')
        file_handler.file_move_copy(path_raw, path_split_done, raw_file, False)


    splitted_file_list = file_handler.file_list(path_rename, path_raw_extension)
    if len(splitted_file_list) > 0:
        for file in splitted_file_list:
            rename_files(path_rename, path_ready, path_ocr_error, file)


    # Load paths from configuration

    path_upload = os.path.normpath(config['volpe_upload']['upload'])
    path_error = os.path.normpath(config['volpe_upload']['error'])
    path_done = os.path.normpath(config['volpe_upload']['done'])
    extension = os.path.normpath(config['volpe_upload']['extension'])

    # Get list to upload

    pdf_upload_list = file_handler.file_list(path_upload, extension)
    os_list = convert_to_OS_list(pdf_upload_list)
    print(f'{len(os_list)} OSs to upload')

    # Start automation
    try:
        erp_volpe_handler.volpe_load_tab('Tab_Maintenance', 'Icon_calendar.png')
        erp_volpe_handler.volpe_open_window('Icon_Prog_Tec_man.png', 'Maintenance_Prog_tech.png')
        win_handler.activate_window('Volpe')
        maintenance_path = 'Images/Maintenance_OS'
        error_count = 0
        critical_error = 0
        for os in os_list.keys():
            try:
                erp_volpe_handler.prog_maint_open_fill_os(os, path=maintenance_path)
                sleep(1)
                result = check_appontments()
                if not result:
                    finalize_unfinalize_os(7)
                    sleep(1)
                    check_appontments(True)
                    sleep(1)
                    finalize_unfinalize_os(2)
                    sleep(0.5)
                select_table('Windows_Prog_Tec_man.png', 'Volpe_Prog_tec_Main_row.png', 50, 100)
                sleep(0.5)
                pyautogui.press('enter')
                sleep(0.5)
                try:
                    message_win_pos = win_handler.image_search('Exclamation_mark_blue.png')
                    sleep(0.5)
                    win_handler.icon_click('OK_button_upper.png', confidence_value=1, region_value=(erp_volpe_handler.region_definer(message_win_pos.left, message_win_pos.top)))
                except:
                    print('No warning window found')
                maintnance_os_pos = win_handler.image_search('title_maintenance_OS_zoom.png', path=maintenance_path)
                sleep(0.5)
                try:
                    win_handler.icon_click('Icon_Clip.png', region_value=(erp_volpe_handler.region_definer(maintnance_os_pos.left, maintnance_os_pos.top)), path=maintenance_path)
                except Exception as error:
                    print(f'Cound not find {error}')
                    win_handler.icon_click('Icon_Clip_paper.png', region_value=(erp_volpe_handler.region_definer(maintnance_os_pos.left, maintnance_os_pos.top)), path=maintenance_path)
                sleep(0.5)
                atacched_items_win = win_handler.image_search('title_atacched_items.png', path=maintenance_path)
                print(os)
                erp_volpe_handler.volpe_tab_select('tab_atach', path=maintenance_path)
                files_list = uploaded_files_list()
                if not files_list:
                    for file in os_list[os]:
                        win_handler.icon_click('Include_button.png', path=maintenance_path)
                        sleep(0.5)
                        atached_win_pos = win_handler.image_search('title_Anexo.png', path=maintenance_path)
                        win_handler.icon_click('Icon_dots.png', path=maintenance_path)
                        sleep(1)
                        load_file(path_upload, file)
                        sleep(1)
                        win_handler.icon_click('Ok_button.png', path=maintenance_path)
                        file_handler.file_move_copy(path_upload, path_done, file, False)
                else:
                    for file in os_list[os]:
                        if file in files_list:
                            file_handler.file_move_copy(path_upload, path_error, file, False)
                        else:
                            file_handler.file_move_copy(path_upload, path_done, file, False)
                close_confirmation(4, 'Ok_button.png', path=maintenance_path)
                print('Done')
            except Exception as error:
                close_confirmation(4, 'Cancel_button.png', 'Ok_button.png', 'OK_button_upper.png', path=maintenance_path)
                error_count = error_count + 1
                if error_count == 4:
                    print(f'Too many errors: {error}. \nReseting Volpe interface.')
                    erp_volpe_handler.volpe_back_to_main()
                    erp_volpe_handler.volpe_load_tab('Tab_Maintenance', 'Icon_calendar.png')
                    erp_volpe_handler.volpe_open_window('Icon_Prog_Tec_man.png', 'Maintenance_Prog_tech.png')
                    error_count = 0
                    critical_error = critical_error + 1
                    if critical_error == 3:
                        raise Exception(f'Critical error {error}')
    except Exception as error:
        print(f'Error in automation {error}')
        exit()
    # print('Done')