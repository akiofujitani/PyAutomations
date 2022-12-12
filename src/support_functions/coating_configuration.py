import datetime, file_handler, data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, pyautogui, keyboard, sys, os
from ntpath import join
from time import sleep

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def edging_index_type(product_description, type_list):
    print(product_description)
    for type in type_list:
        for index in type_list[type]:
            if index.upper() in product_description.upper():
                print(f'Product type: {type}')
                return type
    raise Exception('Could not find eding type')


def delete_line(tries=2):
    for count in range(tries):
        try:
            sleep(0.2)
            pyautogui.rightClick()
            sleep(0.3)
            pyautogui.press('e')
            sleep(0.7)
            pyautogui.press('s')
            sleep(0.3)
            print('Line deleted')
            return
        except Exception as error:
            print(f'Could not dele line due {error}')
            if count >= 1:
                raise error
    return


def frame_type_checker(ocr_text, frame_type_list):
    for frame in frame_type_list:
        if frame in ocr_text:
            print(f'Frame type {frame} return')
            return True
    return False


def delete_duplicates(ocurrences_list) -> None:
    pass


def wait_time(seconds=int):
    regressive_count = seconds
    for i in range(seconds):
        print(f'Waiting.......{regressive_count}')
        regressive_count = regressive_count - 1
        sleep(1.0)
    print('Waiting done')
    return


def get_coating(family=str, coating_by_family=dict, default_name='DEFAULT') -> list:
    if family not in coating_by_family.keys():
        return default_name, coating_by_family[default_name]
    else:
        return family, coating_by_family[family]


def define_tint_coating(product_name=str, index_tint_coat=dict, index_value_swap={'POLY' : '1.59'}) -> list:
    for key in index_value_swap.keys():
        if key in product_name:
            product_name = product_name.replace(key, index_value_swap[key])
        for index in index_tint_coat.keys():
            if index in product_name:
                return index_tint_coat[index]
    return


def get_lens_tint(product_name=str, feature_list=list) -> bool:
    for feature in feature_list:
        if feature in product_name:
            return False
    return True


'''
==========================================================================================================================================


            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN


==========================================================================================================================================
'''



if __name__ == '__main__':
    # erp_volpe_handler.volpe_back_to_main()
    try:
        config = json_config.load_json_config('coating_config.json')
    except:
        print('Could not load config file')
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
        feature_list = ''
        if 'values' in feature_data.keys():
            feature_list = data_communication.column_to_list(feature_data)
        if 'values' in coating_data.keys():
            coating_list = data_communication.list_to_dict_key_and_list(coating_data['values'], 0)
        tint_list = ''
        if 'values' in tint_data.keys():
            tint_list = data_communication.matrix_into_dict(tint_data['values'], 'CODE', 'DESCRIPTION', 'TYPE')
        index_tint_coat = ''
        if 'values' in index_tint_and_tinticoat_data.keys():
            index_tint_coat = data_communication.list_to_dict_key_and_list(index_tint_and_tinticoat_data['values'], 0)
    except Exception as error:
        print(f'Error converting configuration values {error}')
    
    # Get last uploaded date

    for try_number in range(config['parameters']['number_tries']):
        try:
            # erp_volpe_handler.volpe_back_to_main()
            # erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            # erp_volpe_handler.volpe_open_window('Icon_Coating_config.png', 'Configuration_coating.png', path='Images/Coating_Config/')

            print('Base automation done')

            done_data = data_communication.get_values(config['done_list']['sheets_name'], config['done_list']['sheets_pos'], sheets_id=sheets_id)
            done_list = ''
            if 'values' in done_data.keys():
                done_list = data_communication.matrix_into_dict(done_data, 'CODE', 'DESCRIPTION')

            print('Sheets data loaded')

            for product in codes_list:
                if not product['CODE'] in list(done_product['CODE'] for done_product in done_list):
                    product_coating_list = []
                    family_type, product_coating_list = get_coating(product['FAMILY'], coating_list)
                    if get_lens_tint(product['DESCRIPTION'], feature_list):
                        product_coating_list = product_coating_list + define_tint_coating(product['DESCRIPTION'], index_tint_coat)
                        product_coating_list = product_coating_list + [tint['CODE'] for tint in tint_list if tint['TYPE'] == family_type]
                    print(product_coating_list)
                    erp_volpe_handler.load_product_code(product['CODE'], 
                                    field_name='Product.png', 
                                    consult_button='Button_Consult.png', 
                                    path='Images/Coating_Config/')
                    file_name = f'{config["parameters"]["file_name_pattern"]}{product["CODE"]}'
                    erp_volpe_handler.volpe_save_report(file_name, config['parameters']['report_path'])
                    current_coating_list = file_handler.CSVtoList(join(config['parameters']['report_path'], f'{file_name}.txt'))
                    print('Done')
                    now_datetime = datetime.datetime.now()
                    data_communication.data_append_values(sheets_name_done, 
                                        sheets_pos_done, 
                                        [[product['CODE'], 
                                        product['DESCRIPTION'], 
                                        now_datetime.strftime('%d/%m/%Y'), 
                                        now_datetime.strftime('%H:%M:%S')]], 
                                        sheets_id)
                    print(f'{product["DESCRIPTION"]} done')
            print('Done')
        except Exception as error:
            print(f'Error {error}')
            print(f'Try number {try_number + 1}')
            wait_time(5)