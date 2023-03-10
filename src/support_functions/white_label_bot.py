import data_communication, win_handler, json_config, erp_volpe_handler, pyautogui, keyboard, logging, threading
import logger as log
from ntpath import join
from time import sleep
from dataclasses import dataclass


logger = logging.getLogger('white_label_bot')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''

@dataclass
class Configuration:
    sheets_id : str
    main_name : str
    main_pos : str
    description_name : str
    description_pos : str
    swap_name : str
    swap_pos : str
    done_list_name : str
    done_list_pos : str


    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(__o, key):
                    return False
            return True
    

    @classmethod
    def init_dict(cls, dict_values=dict):
        try:
            sheets_id = dict_values['sheets_id']
            main_name = dict_values['main_name']
            main_pos = dict_values['main_pos']
            description_name = dict_values['description_name']
            description_pos = dict_values['description_pos']
            swap_name = dict_values['swap_name']
            swap_pos = dict_values['swap_pos']
            done_list_name = dict_values['done_list_name']
            done_list_pos = dict_values['done_list_pos']
            return cls(sheets_id, main_name, main_pos, description_name, description_pos, swap_name, swap_pos, done_list_name, done_list_pos)
        except Exception as error:
            logger.error(f'Error in {error}')


'''
==================================================================================================================================

        Template Values     Template Values     Template Values     Template Values     Template Values     Template Values     

==================================================================================================================================
'''


template = '''
{
    "sheets_id" : "1woQuWByZHNX8H74b9w62fQlV3F91G3iqihlNA7Ldfw4",
    "main_name" : "WHITE LABEL LIST",
    "main_pos" : "A2:Z",
    "description_name" : "DESCRIPTION_SHORTEN",
    "description_pos" : "A2:B",
    "swap_name" : "DESCRIPTION_SWAP",
    "swap_pos" : "A2:C",
    "done_list_name" : "DONE_LIST",
    "done_list_pos" : "A:Z"
}
'''


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
        if shorten_value['DESCRIPTION'].strip() in base_descr:
            base_descr = base_descr.replace(shorten_value['DESCRIPTION'].strip(), shorten_value['SWAP_TO'].strip())
    return base_descr


def description_validator(product_description, base_description):
    description_validator = base_description.split(' ')
    for word in product_description.split(' '):
        if word in description_validator:
            description_validator.remove(word)
            if len(description_validator) == 0 and 'SLIM' not in product_description:
                return True
    return False


def create_white_label_description(event, white_label, shorten_list, swap_list, done_list, sheets_id, done_list_name, done_list_pos):
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
            if event.is_set():
                return
            base_descr = erp_volpe_handler.ctrl_d(descr_pos.left + 15, selected_pos.top + 4)
            base_type = erp_volpe_handler.ctrl_d(type_pos.left + 15, selected_pos.top + 4)
            converted_descr = base_descr
            if white_label['CODE'] in swap_list.keys():
                converted_descr = description_shorten_swap(converted_descr, swap_list[white_label['CODE']])
            converted_descr = description_shorten_swap(converted_descr, shorten_list)    
            white_label_name = converted_descr.replace(white_label['BASE'].strip(), white_label['DESCRIPTION'].strip())
            logger.debug(f'{white_label_name} - {converted_descr}')
            sleep(0.3)
            if base_type == white_label['TYPE'] and white_label_name not in done_list:
                open_white_label_descr()
                insert_white_label_values(white_label_name,
                                        white_label['CODE'], 
                                        white_label['ENG'])
                data_communication.data_append_values(done_list_name, 
                                        done_list_pos, 
                                        [[code_value, base_descr, white_label_name, white_label['CODE'], white_label['BASE']]], sheets_id)
            last_code_value = code_value
            keyboard.press_and_release('down')
            sleep(0.3)
            selected_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 15, header_pos.top, 200)))
            code_value = erp_volpe_handler.ctrl_d(code_pos.left + 35, selected_pos.top + 4)
        logger.info('White label done')
        return True
    except Exception as error:
        logger.error(f'Create white label error {error}')
        raise error


'''
==================================================================================================================================

        Main        Main        Main        Main        Main        Main        Main        Main        Main        Main        

==================================================================================================================================
'''

def quit_func():
    logger.info('Quit pressed')
    event.set()
    return


def main(event=threading.Event, config=Configuration):
    if event.is_set():
        logger.warning('Event set')
        return
    
    # Load white label values
    try:
        white_label_data = data_communication.get_values(config.main_name, config.main_pos, config.sheets_id)
        description_shorten = data_communication.get_values(config.description_name, config.description_pos, config.sheets_id)
        description_swap = data_communication.get_values(config.swap_name, config.swap_pos, config.sheets_id)
        white_label_list = data_communication.matrix_into_dict(white_label_data['values'], 'BASE', 'TYPE', 'DESCRIPTION', 'ENG', 'CUSTOMER', 'CODE', 'DETAILS_NAMING', 'STATUS','BRANCH')
        shorten_list = data_communication.matrix_into_dict(description_shorten['values'], 'DESCRIPTION', 'SWAP_TO')
        swap_list = data_communication.list_to_dict_with_key(data_communication.matrix_into_dict(description_swap['values'], 'CUSTOMER_CODE', 'DESCRIPTION', 'SWAP_TO'), 'CUSTOMER_CODE')        
        if event.is_set():
            logger.warning('Event set')
            return
    except Exception as error:
        logger.critical(f'Loading table {error}')
        event.set()
        return

    # Start automation
    try:
        erp_volpe_handler.volpe_back_to_main()
        erp_volpe_handler.volpe_load_tab('Tab_Reg', 'Icon_Logins_web.png')
        erp_volpe_handler.volpe_open_window('Icon_Products.png', 'Products.png', path='Images/Registry')
        if event.is_set():
            logger.warning('Event set')
            return

        for i in range(len(white_label_list)):
            if event.is_set():
                logger.warning('Event set')
                return
            white_label = white_label_list[i]
            if not white_label['STATUS'].upper() == 'DONE':
                try:
                    done_list_data = data_communication.get_values(config.done_list_name, config.done_list_pos, config.sheets_id)
                    white_label_done_list = data_communication.matrix_into_dict(done_list_data['values'], 'CODE', 'DESCRIPTION', 'WHITE_LABEL', 'CUSTOMER_CODE', 'FAMILY')
                except Exception as error:
                    logger.error(f'Error {error}')
                    raise error
                registry_load_by_description(white_label['BASE'])
                white_label_status = create_white_label_description(event, white_label, 
                                                                    shorten_list, 
                                                                    swap_list, 
                                                                    [white_label['WHITE_LABEL'] for white_label in white_label_done_list], 
                                                                    config.sheets_id,
                                                                    config.done_list_name, 
                                                                    config.done_list_pos)
                if white_label_status:
                    data_communication.data_update_value(config.main_name, f'H{i + 2}', [['DONE']], config.sheets_id)
                if event.is_set():
                    logger.warning('Event set')
                    return
        logger.info('Done')
        event.set()
        return
    except Exception as error:
        logger.critical(f'Error {error}')
        return


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    try:
        config_dict = json_config.load_json_config('white_label.json', template)
        config = Configuration.init_dict(config_dict)
    except:
        logger.critical('Could not load config file')
        exit()

    keyboard.add_hotkey('space', quit_func)
    event = threading.Event()

    for _ in range(5):
        if event.is_set():
            break
        thread = threading.Thread(target=main, args=(event, config, ), name='white_label')
        thread.start()
        thread.join()

    logger.debug('Done')