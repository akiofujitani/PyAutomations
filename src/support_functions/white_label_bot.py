import datetime, file_handler, data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, pyautogui, keyboard, logging
import logger as log
from ntpath import join
from time import sleep



logger = logging.getLogger('white_label_bot')

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
        logger.debug(f'{description} written')
    except Exception as error:
        logger.error(f'Error {error}')
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
        logger.debug('White label description openned')
        sleep(0.5)
    except Exception as error:
        logger.error(f'Erro opening windows {error}')
        raise error


def insert_white_label_values(description=str, code=str, engraving=str):
    try:
        pyautogui.press('i')
        sleep(0.6)
        pyautogui.write(code)
        sleep(0.3)
        pyautogui.press('tab')
        sleep(0.3)
        pyautogui.write(description)
        sleep(0.3)
        pyautogui.press('tab')
        sleep(0.3)
        pyautogui.write(engraving)
        pyautogui.press('tab')
        sleep(0.5)
        pyautogui.press('space')
        sleep(0.5)
        pyautogui.press('s')
        sleep(0.3)
        win_handler.icon_click('Volpe_Close.png')
    except Exception as error:
        for _ in range(3):
            logger.warning(f'Error in {error}')
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
                    logger.warning(f'Button {button} not found')
    return


def description_shorten_swap(base_descr, shorten_list):
    for shorten_value in shorten_list:
        if shorten_value['DESCRIPTION'] in base_descr:
            base_descr = base_descr.replace(shorten_value['DESCRIPTION'], shorten_value['SHORTEN'])
    return base_descr


def description_validator(product_description, base_description):
    description_validator = base_description.split(' ')
    for word in product_description.split(' '):
        if word in description_validator:
            description_validator.remove(word)
            if len(description_validator) == 0 and 'SLIM' not in product_description:
                return True
    return False


def create_white_label_description(white_label, shorten_list, swap_list, done_list, config):
    try:
        code_value = ''
        last_code_value = 'old'
        header_pos = win_handler.image_search('Product_sheet_header.png', path='Images/Registry')
        descr_pos = win_handler.image_search('Header_descr.png', path='Images/Registry')
        code_pos = win_handler.image_search('Header_code.png', path='Images/Registry')
        type_pos = win_handler.image_search('Header_type.png', path='Images/Registry')
        try:
            selected_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 15, header_pos.top, 200)))
        except Exception as error:
            return
        code_value = erp_volpe_handler.ctrl_d(code_pos.left + 35, selected_pos.top + 4)
        while not code_value == last_code_value: 
            base_descr = erp_volpe_handler.ctrl_d(descr_pos.left + 15, selected_pos.top + 4)
            base_type = erp_volpe_handler.ctrl_d(type_pos.left + 15, selected_pos.top + 4)
            base_descr_shorten = description_shorten_swap(base_descr, shorten_list)
            if white_label['CODE'] in swap_list.keys():
                base_descr_shorten = description_shorten_swap(base_descr_shorten, swap_list[white_label['CODE']])
            white_label_name = base_descr_shorten.replace(white_label['BASE'].strip(), white_label['DESCRIPTION'].strip())
            sleep(0.3)
            if base_type == white_label['TYPE'] and white_label_name not in done_list:
                open_white_label_descr()
                insert_white_label_values(white_label_name,
                                        white_label['CODE'], 
                                        white_label['ENG'])
                data_communication.data_append_values(config['done_list']['sheets_name'], 
                                        config['done_list']['sheets_pos'], 
                                        [[code_value, base_descr, white_label_name, white_label['CODE'], white_label['BASE']]], config['done_list']['sheets_id'])
            last_code_value = code_value
            keyboard.press_and_release('down')
            sleep(0.3)
            selected_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 15, header_pos.top, 200)))
            code_value = erp_volpe_handler.ctrl_d(code_pos.left + 35, selected_pos.top + 4)
        return True
    except Exception as error:
        logger.error(f'Create white laber error {error}')
        raise error


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)
    try:
        config = json_config.load_json_config('white_label.json')
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config

    sheets_name = config['main_white_label']['sheets_name']
    sheets_id = config['main_white_label']['sheets_id']
    sheets_pos = config['main_white_label']['sheets_pos']
    sheets_name_descr = config['descriptions']['sheets_name']
    sheets_pos_descr = config['descriptions']['sheets_pos']
    sheets_name_swap = config['descriptions_swap']['sheets_name']
    sheets_pos_swap = config['descriptions_swap']['sheets_pos']
    sheets_done_name = config['done_list']['sheets_name']
    sheets_done_pos = config['done_list']['sheets_pos']

    # Get last uploaded date

    try:
        white_label_data = data_communication.get_values(sheets_name, sheets_pos, sheets_id)
        description_shorten = data_communication.get_values(sheets_name_descr, sheets_pos_descr, sheets_id)
        description_swap = data_communication.get_values(sheets_name_swap, sheets_pos_swap, sheets_id)
        
    except Exception as error:
        logger.critical(f'{error} loading table {sheets_name}')
        quit()

    # erp_volpe_handler.volpe_back_to_main()
    # erp_volpe_handler.volpe_load_tab('Tab_Reg', 'Icon_Logins_web.png')
    erp_volpe_handler.volpe_open_window('Icon_Products.png', 'Products.png', path='Images/Registry')

    white_label_list = data_communication.matrix_into_dict(white_label_data['values'], 'BASE', 'TYPE', 'DESCRIPTION', 'ENG', 'CUSTOMER', 'CODE', 'DETAILS_NAMING', 'STATUS','BRANCH')
    shorten_list = data_communication.matrix_into_dict(description_shorten['values'], 'DESCRIPTION', 'SHORTEN')
    swap_list = data_communication.list_to_dict_with_key(data_communication.matrix_into_dict(description_swap['values'], 'CUSTOMER_CODE', 'DESCRIPTION', 'SWAP'), 'CUSTOMER_CODE')

    try:
        for i in range(len(white_label_list)):
            white_label = white_label_list[i]
            if not white_label['STATUS'].upper() == 'DONE':
                try:
                    done_list_data = data_communication.get_values(sheets_done_name, sheets_done_pos, sheets_id)
                    white_label_done_list = data_communication.matrix_into_dict(done_list_data['values'], 'CODE', 'DESCRIPTION', 'WHITE_LABEL', 'CUSTOMER_CODE', 'FAMILY')
                except Exception as error:
                    logger.error(f'Error {error}')
                    raise error
                registry_load_by_description(white_label['BASE'])
                white_label_status = create_white_label_description(white_label, shorten_list, swap_list, [white_label['WHITE_LABEL'] for white_label in white_label_done_list], config)
                if white_label_list:
                    data_communication.data_update_value(sheets_name, f'H{i + 2}', [['DONE']], sheets_id)
        logger.info('Done')
    except Exception as error:
        logger.critical(f'Error {error}')
        quit()
    except KeyboardInterrupt:
        logger.critical('Script interrupted')