import datetime, file_handler, data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, pyautogui, logging
import logger as log
from ntpath import join
from time import sleep

logger = logging.getLogger('coating_config')  

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


def wait_time(seconds=int):
    regressive_count = seconds
    for i in range(seconds):
        logger.info(f'Waiting.......{regressive_count}')
        regressive_count = regressive_count - 1
        sleep(1.0)
    logger.info('Waiting done')
    return


def __get_coating(family=str, coating_by_family=dict, default_name='DEFAULT') -> list:
    logger.debug(f'{default_name} {family} {coating_by_family[default_name]}')
    if family not in coating_by_family.keys():
        return default_name, coating_by_family[default_name]
    else:
        return family, coating_by_family[family]


def __define_tint_coating(product_name=str, index_tint_coat=dict, index_value_swap={'POLY' : '1.59'}) -> list:
    for key in index_value_swap.keys():
        if key in product_name:
            product_name = product_name.replace(key, index_value_swap[key])
        for index in index_tint_coat.keys():
            if index in product_name:
                return index_tint_coat[index]
    return


def __uv_check_list(feature_list=list, remove_list=list, add_list=list) -> list:
    uv_check_list = [item for item in feature_list]
    for remove_item in remove_list:
        if remove_item in uv_check_list:
            uv_check_list.remove(remove_item)
    for add_item in add_list:
        if add_item not in uv_check_list:
            uv_check_list.append(add_item)
    return uv_check_list


def __uv_tint(product_name=str, uv_check_list=list) -> bool:
    for feature in uv_check_list:
        if feature in product_name:
            return True
    return


def __get_lens_tint(product_name=str, feature_list=list) -> bool:
    for feature in feature_list:
        if feature in product_name:
            return False
    return True


def load_table_list(file_path=str, file_path_done=str, file_name=str) -> dict:
    try:
        file_contents = file_handler.CSVtoList(join(file_path, file_name))

    except Exception as error:
        logger.error(f'Load table error {error}')


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
        config = json_config.load_json_config('c:/PyAutomations_Reports/coating_config.json')
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config  
    try:
        sheets_id = config['sheets_id']
        codes_list = data_communication.matrix_into_dict(data_communication.get_values(config['product_codes']['sheets_name'], 
                                    config['product_codes']['sheets_pos'], 
                                    sheets_id=sheets_id)['values'],
                                    'CODE',
                                    'DESCRIPTION',
                                    'TYPE',
                                    'FAMILY')
        feature_data = data_communication.get_values(config['feature_list']['sheets_name'], 
                                    config['feature_list']['sheets_pos'],
                                    sheets_id=sheets_id)
        coating_data = data_communication.get_values(config['coating']['sheets_name'], 
                                    config['coating']['sheets_pos'],
                                    sheets_id=sheets_id)
        tint_data = data_communication.get_values(config['tint_list']['sheets_name'], 
                                    config['tint_list']['sheets_pos'], 
                                    sheets_id=sheets_id)
        tint_color = data_communication.get_values(config['tint_list']['sheets_name'], 
                                    config['tint_list']['sheets_pos'], 
                                    sheets_id=sheets_id)
        index_tint_and_tinticoat_data = data_communication.get_values(config['index_tint_and_tintcoat']['sheets_name'], 
                                    config['index_tint_and_tintcoat']['sheets_pos'], 
                                    sheets_id=sheets_id)
        family_data = data_communication.get_values(config['family_list']['sheets_name'], 
                                    config['family_list']['sheets_pos'], 
                                    sheets_id=sheets_id)
        file_name_pattern = config['parameters']['file_name_pattern']
        report_path = config['parameters']['report_path']
        report_path_done = config['parameters']['report_path_done']
        sheets_name_done = config['done_list']['sheets_name']
        sheets_pos_done = config['done_list']['sheets_pos']
        feature_values_list = ''
        if 'values' in feature_data.keys():
            feature_values_list = data_communication.column_to_list(feature_data)
        if 'values' in coating_data.keys():
            coating_list = data_communication.list_to_dict_key_and_list(coating_data['values'], 0)
        tint_list = ''
        if 'values' in tint_data.keys():
            tint_list = data_communication.matrix_into_dict(tint_data['values'], 'CODE', 'DESCRIPTION', 'TYPE')
        index_tint_coat = ''
        if 'values' in index_tint_and_tinticoat_data.keys():
            index_tint_coat = data_communication.list_to_dict_key_and_list(index_tint_and_tinticoat_data['values'], 0)
        if 'values' in family_data.keys():
            family_list = data_communication.column_to_list(family_data, 0)
        uv_check_list = __uv_check_list(feature_values_list, ['POLAR'], ['UV', 'BLUECUT', '1.59 POLAR'])
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