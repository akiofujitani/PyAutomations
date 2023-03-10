import data_communication, win_handler, json_config, erp_volpe_handler, pyautogui, logging, keyboard, win32gui, threading
import logger as log
from time import sleep
from dataclasses import dataclass

logger = logging.getLogger('product_config')  


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''

@dataclass
class Config_Values:
    sheets_name : str
    sheets_name_done : str
    sheets_id : str
    sheets_range : str
    sheets_range_done : str
    try_number : int
    values_list : list

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
            sheets_name = dict_values['sheets_name']
            sheets_name_done = dict_values['sheets_name_done']
            sheets_id = dict_values['sheets_id']
            sheets_range = dict_values['sheets_range']
            sheets_range_done = dict_values['sheets_range_done']
            try_number = dict_values['try_number']
            values_list = dict_values['values_list']
            return cls(sheets_name, sheets_name_done, sheets_id, sheets_range, sheets_range_done, try_number, values_list)
        except Exception as error:
            logger.error(f'Error in {error}')
    

@dataclass
class Product:
    code : any
    description : str
    type : str
    price_1 : float
    price_2 : float
    price_3 : float
    price_4 : float
    price_5 : float
    price_6 : float
    repos_cost : float


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
            code = dict_values['code']
            description = dict_values['description']
            type = dict_values['type']
            price_1 = dict_values['price_1']
            price_2 = dict_values['price_2']
            price_3 = dict_values['price_3']
            price_4 = dict_values['price_4']
            price_5 = dict_values['price_5']
            price_6 = dict_values['price_6']
            repos_cost = dict_values['repos_cost']
            return cls(code, description, type, price_1, price_2, price_3, price_4, price_5, price_6, repos_cost)
        except Exception as error:
            logger.error(f'Erro in {error}')

'''
==================================================================================================================================

        Template Values     Template Values     Template Values     Template Values     Template Values     Template Values     

==================================================================================================================================
'''

template = '''
{
    "sheets_name" : "PRODUCT_CODES",
    "sheets_name_done" : "DONE_LIST",
    "sheets_id" : "1SkeiwNjCXAOHo1qQaIUn-66FwC4lQg2TWXaNfRAYQLw",
    "sheets_range" : "A2:K",
    "sheets_range_done" : "A2:C",
    "try_number" : 3,
    "values_list" : [
        "code",
        "description",
        "type",
        "price_1",
        "price_2",
        "price_3",
        "price_4",
        "price_5",
        "price_6",
        "repos_cost"
    ]
}

'''



'''
==================================================================================================================================

        Automations     Automations     Automations     Automations     Automations     Automations     Automations     

==================================================================================================================================
'''

def add_product_codes(codes_list=list, window_title=str, path='images/') -> None:
    try:
        win_title_pos = win_handler.image_search(window_title, path=path)
        for code in codes_list:
            pyautogui.write(code)
            sleep(0.3)
            pyautogui.press(['tab', 'tab'], interval=0.3)
            sleep(0.3)
            pyautogui.press('space')
            sleep(0.3)
            pyautogui.press(['tab', 'tab', 'tab', 'tab', 'tab', 'tab',], interval=0.3)
            sleep(0.3)
            pyautogui.press('space')
            sleep(0.3)
            pyautogui.press(['tab', 'tab', 'tab', 'tab'], interval=0.3)
            sleep(0.3)
            pyautogui.hotkey('ctrl', 'a')
            sleep(0.3)
        win_handler.icon_click('Button_Select.png', region_value=erp_volpe_handler.region_definer(win_title_pos.left, win_title_pos.top), path=path)
        return
    except Exception as error:
        logger.error(f'Could not add product code due {error}')
        raise error
    except KeyboardInterrupt:
        raise KeyboardInterrupt


def change_price(pos_x=int, pos_y=int,  product=dict):
    values_list = ['price_1', 'price_2', 'price_3', 'price_4', 'price_5', 'price_6', 'repos_cost']
    try:
        sleep(0.3)
        current_code = erp_volpe_handler.ctrl_d(pos_x, pos_y)
        if current_code == product.code:
            sleep(0.5)
            pyautogui.press('a')
            sleep(0.5)
            product_win = win_handler.image_search('Product_change.png', path='./Images/Registry/')
            if product_win:
                sleep(0.3)
                for _ in range(3):
                    keyboard.press('right')
                    sleep(0.3)
                pyautogui.press('tab')  
                sleep(0.5)
                for value in values_list:
                    product_value = getattr(product, value, '')
                    if not product_value == '':
                        pyautogui.write(product_value)
                        sleep(0.5)
                    pyautogui.press('tab')
                    sleep(0.3)
                    logger.debug(f'{product.description} value: {product_value}')
            
                # Debug purpuses
                pyautogui.press('tab')
                sleep(0.5)
                pyautogui.press('space')
                sleep(0.5)
                win_handler.activate_window('Volpe')
                window = win32gui.GetForegroundWindow()
                win_title = win32gui.GetWindowText(window)
                sleep(0.5)
                if 'Altera' in win_title:
                    pyautogui.press('s')
                    sleep(0.3)
                logger.info(f'{product.code} {product.description} done')
                return True
    except Exception as error:
        logger.warning(f'Error due {error}')
        raise error


'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def wait_time(seconds=int):
    regressive_count = seconds
    for _ in range(seconds):
        logger.info(f'Waiting.......{regressive_count}')
        regressive_count = regressive_count - 1
        sleep(1.0)
    logger.info('Waiting done')
    return


def build_product_list(product_data_list=list, keys_list=list) -> list:
    product_list = []
    for product_data in product_data_list:
        product_values = {}
        for key_number in range(len(keys_list)):
            try:
                product_values[keys_list[key_number]] = product_data[key_number]
            except:
                product_values[keys_list[key_number]] = ''
        product_list.append(Product.init_dict(product_values))
    return product_list



'''
==========================================================================================================================================


            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN


==========================================================================================================================================
'''

def quit_func():
    logger.info('Quit pressed')
    event.set()
    return


def main(event=threading.Event, config=Config_Values):
    if event.is_set():
        logger.warning('Event set')
        return

    # Load config  
    try:
        products_sheet = data_communication.get_values(config.sheets_name, config.sheets_range, config.sheets_id)
        if 'values' in products_sheet.keys():
            product_list = build_product_list(products_sheet['values'], config.values_list)
    except Exception as error:
        logger.critical(f'Error converting configuration values {error}')
        event.set()
    
    # Get last uploaded date
    for try_number in range(config.try_number):
        if event.is_set():
            logger.warning('Event set')
            return
        try:
            erp_volpe_handler.volpe_back_to_main()
            erp_volpe_handler.volpe_load_tab('Tab_Reg', 'Icon_Reg_par.png')
            erp_volpe_handler.volpe_open_window('Icon_Products.png', 'Products.png', path='Images/Registry/')
            win_handler.activate_window('Volpe')
            logger.info('Base automation done')
            if event.is_set():
                logger.warning('Event set')
                return
            done_data = data_communication.get_values(config.sheets_name_done, config.sheets_range_done, sheets_id=config.sheets_id)
            done_list = ''
            if 'values' in done_data.keys():
                done_list = data_communication.matrix_into_dict(done_data['values'], 'CODE', 'DESCRIPTION', 'TYPE')

            logger.info('Sheets data loaded')
            done_list_code = [done_product['CODE'] for done_product in done_list]

            #Fields Position
            try:
                table_header = win_handler.image_search('Product_sheet_header.png', path='./Images/Registry')
            except Exception as error:
                logger.error(f'Error due {error}')

            for product in product_list:
                change_result = ''
                if not product.code in done_list_code:
                    win_handler.activate_window('Volpe')
                    erp_volpe_handler.load_product_code(product.code, 
                                    field_name='Code.png', 
                                    consult_button='Button_Consult.png', 
                                    path='Images/Registry/')
                    if event.is_set():
                        logger.warning('Event set')
                        return
                    change_result = change_price(table_header.left + 15, table_header.top + 20, product)
                    if change_result:
                        try:
                            data_communication.data_append_values(config.sheets_name_done, 
                                        config.sheets_range_done, 
                                        [[product.code, product.description, product.type]], 
                                        config.sheets_id)
                        except Exception as error:
                            logger.error(f'Could not save values sheets due {error}')
                            raise error
                if event.is_set():
                    logger.warning('Event set')
                    return
        except Exception as error:
            logger.critical(f'Error {error}')
            logger.critical(f'Try number {try_number + 1}')
            wait_time(5)
    return


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)

    try:
        config_dict = json_config.load_json_config('c:/PyAutomations_Reports/product_price_adjust.json', template)
        config = Config_Values.init_dict(config_dict)
    except:
        logger.critical('Could not load config file')
        quit()

    keyboard.add_hotkey('space', quit_func)
    event = threading.Event()

    for _ in range(3):
        if event.is_set():
            break
        thread = threading.Thread(target=main, args=(event, config, ), name='product_config')
        thread.start()
        thread.join()

    logger.debug('Done')