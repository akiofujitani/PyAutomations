import datetime, file_handler, data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, pyautogui, keyboard
from ntpath import join
from time import sleep

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''

def remove_from_dict(values_dict=dict, *args):
    updated_dict = []
    for value in values_dict:
        for arg in args:
            value.pop(arg.upper())
        updated_dict.append(value)
    return updated_dict


def registry_load_by_description(description):
    try:
        descr_pos = win_handler.image_search('Description.png', path='Images/Registry')
        win_handler.click_field(descr_pos, 'Bellow', 15)
        sleep(0.3)
        pyautogui.click()
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.5)
        pyautogui.write(f"'%{description}")
        win_handler.icon_click('Button_Consult.png', path='Images/Registry')
    except Exception as error:
        raise error
    return


def open_white_label_descr():
    try:
        pyautogui.rightClick()
        sleep(0.3)
        pyautogui.press('l')
        sleep(0.3)
        for _ in range(3):
            keyboard.press_and_release('up')
            sleep(0.3)
        pyautogui.press('enter')
        sleep(0.5)
        descr_by_customer_win = win_handler.image_search('Description_by_customer.png', path='Images/Registry')
        descr_by_customer_sheet_pos = win_handler.image_search('Description_by_customer_sheet_header.png', region=(erp_volpe_handler.region_definer(descr_by_customer_win.left - 15, descr_by_customer_win.top)), path='Images/Registry')
        win_handler.click_field(descr_by_customer_sheet_pos, 'Bellow', distance=30)
        sleep(0.5)
    except Exception as error:
        print(f'Erro opening windows {error}')
        raise error


def insert_white_label_values(description=str, code=str, engraving=str):
    try:
        pyautogui.press('i')
        sleep(0.3)
        include_descr_pos = win_handler.image_search('Include_description.png', path='Images/Registry')
        sleep(0.3)
        pyautogui.write(code)
        sleep(0.3)
        pyautogui.press('tab')
        sleep(0.3)
        pyautogui.write(description)
        sleep(0.3)
        pyautogui.press('tab')
        sleep(0.3)
        pyautogui.write(engraving)
        #Test purpuses...
        win_handler.icon_click('Button_cancel.png')
        sleep(0.5)
        pyautogui.press('s')
        sleep(0.3)
        win_handler.icon_click('Volpe_Close.png')
    except Exception as error:
        for _ in range(3):
            print(f'Error in {error}')
            button_list = ['Button_cancel.png', 'Button_yes.png', 'Button_yes_Win11.png', 'Volpe_Close.png', 'Volpe_Close_Inactive.png']
            for button in button_list:
                try:     
                    win_handler.activate_window('Volpe')       
                    descr_by_customer_win = win_handler.image_search('Description_by_customer.png', path='Images/Registry')
                    region = erp_volpe_handler.region_definer(descr_by_customer_win.left - 15, descr_by_customer_win.top - 20)
                    sleep(0.3)
                    button_pos = win_handler.image_search(button, region=region)
                    win_handler.click_volpe(button_pos)
                except:
                    print(f'Button {button} not found')
    return


def description_shorten_swap(base_descr, shorten_list):
    for shorten_value in shorten_list:
        if shorten_value['DESCRIPTION'] in base_descr:
            base_descr = base_descr.replace(shorten_value['DESCRIPTION'], shorten_value['SHORTEN'])
    return base_descr


def create_white_label_description(white_label, shorten_list, swap_list, config):
    try:
        code_value = ''
        last_code_value = 'old'
        header_pos = win_handler.image_search('Product_sheet_header.png', path='Images/Registry')
        descr_pos = win_handler.image_search('Header_descr.png', path='Images/Registry')
        code_pos = win_handler.image_search('Header_code.png', path='Images/Registry')
        selected_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 15, header_pos.top, 200)))
        code_value = erp_volpe_handler.ctrl_d(code_pos.left + 35, selected_pos.top + 4)
        while not code_value == last_code_value: 
            base_descr = erp_volpe_handler.ctrl_d(descr_pos.left + 15, selected_pos.top + 4)
            base_descr_shorten = description_shorten_swap(base_descr, shorten_list)
            if white_label['CODE'] in swap_list.keys():
                base_descr_shorten = description_shorten_swap(base_descr_shorten, swap_list[white_label['CODE']])
            white_label_name = base_descr_shorten.replace(white_label['BASE'].strip(), white_label['DESCRIPTION'].strip())
            sleep(0.3)
            open_white_label_descr()
            insert_white_label_values(white_label_name,
                                    white_label['CODE'], 
                                    white_label['ENG'])
            data_communication.data_append_values(config['done_list']['sheets_name'], 
                                    config['done_list']['sheets_pos'], 
                                    [[code_value, base_descr, white_label['CODE'], white_label['BASE']]], config['done_list']['sheets_id'])
            last_code_value = code_value
            keyboard.press_and_release('down')
            sleep(0.3)
            selected_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 15, header_pos.top, 200)))
            code_value = erp_volpe_handler.ctrl_d(code_pos.left + 35, selected_pos.top + 4)
    except Exception as error:
        print(f'Create white laber error {error}')
        raise error


if __name__ == '__main__':
    try:
        config = json_config.load_json_config('white_label.json')
    except:
        print('Could not load config file')
        exit()

    # Load config

    sheets_name = config['main_white_label']['sheets_name']
    sheets_id = config['main_white_label']['sheets_id']
    sheets_pos = config['main_white_label']['sheets_pos']
    sheets_name_descr = config['descriptions']['sheets_name']
    sheets_pos_descr = config['descriptions']['sheets_pos']
    sheets_name_swap = config['descriptions_swap']['sheets_name']
    sheets_pos_swap = config['descriptions_swap']['sheets_pos']

    # Get last uploaded date

    try:
        white_label_data = data_communication.get_values(sheets_name, sheets_pos, sheets_id)
        description_shorten = data_communication.get_values(sheets_name_descr, sheets_pos_descr, sheets_id)
        description_swap = data_communication.get_values(sheets_name_swap, sheets_pos_swap, sheets_id)
        
    except Exception as error:
        print(f'{error} loading table {sheets_name}')
        quit()

    # erp_volpe_handler.volpe_back_to_main()
    # erp_volpe_handler.volpe_load_tab('Tab_Reg', 'Icon_Logins_web.png')
    # erp_volpe_handler.volpe_open_window('Icon_Products.png', 'Products.png', path='Images/Registry')

    white_label_list = data_communication.matrix_into_dict(white_label_data['values'], 'BASE', 'DESCRIPTION', 'ENG', 'CUSTOMER', 'CODE', 'BRANCH', 'DETAILS_NAMING', 'STATUS')
    shorten_list = data_communication.matrix_into_dict(description_shorten['values'], 'DESCRIPTION', 'SHORTEN')
    swap_list = data_communication.list_to_dict_with_key(data_communication.matrix_into_dict(description_swap['values'], 'CUSTOMER_CODE', 'DESCRIPTION', 'SWAP'), 'CUSTOMER_CODE')

    for white_label in white_label_list:
        if not white_label['STATUS'].upper() == 'DONE':
            registry_load_by_description(white_label['BASE'])
            create_white_label_description(white_label, shorten_list, swap_list, config)
            print('Not done')
            print('')
    print('Done')