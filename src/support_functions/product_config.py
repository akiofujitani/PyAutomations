import datetime, file_handler, data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, pyautogui, logging
import logger as log
from ntpath import join
from time import sleep
from dataclasses import dataclass
from os.path import normpath

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
            values_list = dict_values['values_list']
            return cls(sheets_name, sheets_name_done, sheets_id, sheets_range, sheets_range_done, values_list)
        except Exception as error:
            logger.error(f'Error in {error}')
    

@dataclass
class Product:
    code : any
    description : str
    type : str
    family : str
    value_1 : float
    value_2 : float
    value_3 : float
    value_4 : float
    value_5 : float
    value_6 : float
    repos_cost : float


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
    "values_list" : [
        "CODE",
        "DESCRIPTION",
        "TYPE",
        "FAMILY",
        "PRICE_1",
        "PRICE_2",
        "PRICE_3",
        "PRICE_4",
        "PRICE_5",
        "PRICE_6",
        "REPOS_COST"
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




'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''

def product_list_converter(product_list=list) -> list:
    converted_list = []
    for product in product_list:
        pass
    


def wait_time(seconds=int):
    regressive_count = seconds
    for i in range(seconds):
        logger.info(f'Waiting.......{regressive_count}')
        regressive_count = regressive_count - 1
        sleep(1.0)
    logger.info('Waiting done')
    return


'''
==========================================================================================================================================


            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN


==========================================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)
    # erp_volpe_handler.volpe_back_to_main()
    try:
        config_dict = json_config.load_json_config('c:/PyAutomations_Reports/product_price_adjust.json', template)
        config = Config_Values.init_dict(config_dict)
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config  
    try:
        products_sheet = data_communication.get_values(config.sheets_name, config.sheets_range, config.sheets_id)
        if 'values' in products_sheet.keys():
            product_list = data_communication.matrix_into_dict(products_sheet['values'], config.values_list)
    except Exception as error:
        logger.critical(f'Error converting configuration values {error}')
    
    # Get last uploaded date

    for try_number in range(config['parameters']['number_tries']):
        try:
            erp_volpe_handler.volpe_back_to_main()
            erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            erp_volpe_handler.volpe_open_window('Icon_Coating_config.png', 'Title_Configuration_coating.png', path='Images/Coating_Config/')
            logger.info('Base automation done')

            done_data = data_communication.get_values(sheets_name_done, sheets_pos_done, sheets_id=sheets_id)
            done_list = ''
            if 'values' in done_data.keys():
                done_list = data_communication.matrix_into_dict(done_data['values'], 'CODE', 'DESCRIPTION')

            logger.info('Sheets data loaded')

            done_list_code = [done_product['CODE'] for done_product in done_list]
            for product in codes_list:
                if not product['CODE'] in done_list_code and product['FAMILY'] in family_list:
                    product_coating_list = []
                    family_type, product_coating_list = __get_coating(product['FAMILY'], coating_list)
                    if __get_lens_tint(product['DESCRIPTION'], feature_values_list):
                        product_coating_list = product_coating_list + __define_tint_coating(product['DESCRIPTION'], index_tint_coat, {'POLY' : '1.59', '1.50 BLUECUT' : '1.56', '1.50' : '1.49'})
                        tint_family = family_type if family_type == 'BELLIOTICA' else 'DEFAULT'
                        product_coating_list = product_coating_list + [tint['CODE'] for tint in tint_list if tint['TYPE'] == tint_family]
                    if not __uv_tint(product['DESCRIPTION'], uv_check_list):
                        product_coating_list = product_coating_list + [tint['CODE'] for tint in tint_list if tint['TYPE'] == 'UV']
                    logger.debug(f'{product["DESCRIPTION"]} : {product_coating_list}')
                    win_handler.activate_window('Volpe')
                    erp_volpe_handler.load_product_code(product['CODE'], 
                                    field_name='Product.png', 
                                    consult_button='Button_Consult.png', 
                                    path='Images/Coating_Config/')
                    file_name = f'{file_name_pattern}{product["CODE"]}.txt'
                    erp_volpe_handler.volpe_save_report(file_name, report_path)

                    # Evaluate items
                    combined_delete_list = ''
                    product_coating_diff = ''
                    current_service_list = file_handler.CSVtoList(join(report_path, file_name))
                    service_code_list = [line['ID.TRATAMENTO'] for line in current_service_list]
                    duplicates = data_organizer.find_duplicates(service_code_list)
                    unique_code_list = list(set(service_code_list))
                    unique_list_diff = [item for item in unique_code_list if item not in product_coating_list]
                    product_coating_diff = [item for item in product_coating_list if item not in unique_code_list]


                    #Delete items
                    if len(duplicates) > 0 or len(unique_list_diff) > 0 or len(product_coating_diff) > 0:
                        column_pos = win_handler.image_search('Coating_id.png', path='Images/Coating_Config')
                    if len(duplicates) > 0 or len(unique_list_diff) > 0:
                        try:
                            combined_delete_list = list(set(duplicates + unique_list_diff))
                            for delete_item in combined_delete_list:
                                erp_volpe_handler.delete_from_table(column_pos, delete_item)
                        except Exception as error:
                            logger.error(f'Could not delete item due {error}')
                            raise error

                    # Add items                    
                    if len(product_coating_diff) > 0:
                        try:
                            pyautogui.rightClick(column_pos.left, column_pos.top + 100)
                            sleep(0.3)
                            pyautogui.press('i')
                            sleep(0.5)
                            config_coat_win_pos = win_handler.image_search('Title_Configuration_coating.png', path='Images/Coating_Config')
                            pyautogui.press('space')
                            add_product_codes([product['CODE']], 'Title_Select_product.png', path='Images/Coating_Config')
                            sleep(0.3)
                            pyautogui.press('tab')
                            sleep(0.3)
                            pyautogui.press('space')
                            sleep(0.6)
                            add_product_codes(product_coating_diff, 'Title_Select_product.png', path='Images/Coating_Config')
                            sleep(0.3)
                            win_handler.icon_click('Button_Ok.png', path='Images/Coating_Config')
                        except Exception as error:
                            logger.error(f'Coating insertion error due {error}')
                            raise error
                    logger.info(f'{product["CODE"]} Done')
                    file_handler.file_move_copy(report_path, report_path_done, file_name, False)
                    now_datetime = datetime.datetime.now()
                    data_communication.data_append_values(sheets_name_done, 
                                        sheets_pos_done, 
                                        [[product['CODE'], 
                                        product['DESCRIPTION'], 
                                        ', '.join([str(delete) for delete in combined_delete_list]) if len(combined_delete_list) > 0 else '',
                                        ', '.join([str(add) for add in product_coating_diff]) if len(product_coating_diff) > 0 else '',
                                        now_datetime.strftime('%d/%m/%Y'), 
                                        now_datetime.strftime('%H:%M:%S')]], 
                                        sheets_id)
                    logger.info(f'{product["DESCRIPTION"]} done')
            logger.info('Done')
        except Exception as error:
            logger.critical(f'Error {error}')
            logger.critical(f'Try number {try_number + 1}')
            wait_time(5)