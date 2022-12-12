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


def __get_feature(product_name=str, feature_list=list) -> str:
    for feature in feature_list:
        if feature in product_name:
            return feature
    return


def __get_family(product_family=str, family_list=list) -> str:
    if product_family not in family_list:
        return 'DEFAULT'
    for family in family_list:
        if family == product_family:
            return family


def __get_tint_list(product_family=str, tint_list=list) -> list:
    if product_family not in [tint['TYPE'] for tint in tint_list]:
        raise Exception('Family not found')
    return [tint for tint in tint_list if tint['TYPE'] == product_family]


def __tint_coating_by_product(product):
    pass

def list_delete_edging_config(product, config):
    edging_index = edging_index_type(product['DESCRIPTION'], config['index_type'])
    try:
        win_pos = win_handler.image_search('Configuration_edging.png', path='Images/Edging_Config')
        header_pos = win_handler.image_search('sheet_header.png', region=(erp_volpe_handler.region_definer(win_pos.left - 15, win_pos.top)), path='Images/Edging_Config/')
        code_pos = win_handler.image_search('header_code.png', region=(erp_volpe_handler.region_definer(win_pos.left - 15, win_pos.top)), path='Images/Edging_Config/')
        type_edging_header_pos = win_handler.image_search('header_montagem.png', region=(erp_volpe_handler.region_definer(win_pos.left - 15, win_pos.top)), path='Images/Edging_Config/')
        frame_header_pos = win_handler.image_search('header_arm.png', region=(erp_volpe_handler.region_definer(win_pos.left - 15, win_pos.top)), path='Images/Edging_Config/')
        line_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 15, header_pos.top)))       
        
        code = erp_volpe_handler.ctrl_d(code_pos.left + 15, line_pos.top + 3)
        while True:
            line_text = ''
            try:
                line_text = erp_volpe_handler.get_text_square(line_pos.left + line_pos.width, line_pos.top, header_pos.width, line_pos.height + 2)
                # line_text = f'{erp_volpe_handler.ctrl_d(type_edging_header_pos.left + 100, line_pos.top + 3)} {erp_volpe_handler.ctrl_d(frame_header_pos.left + 100, line_pos.top + 3)}'
                if 'CORTE REMOTO SURF' in line_text:
                    raise Exception('Text main part not visible')
                if len(line_text) <= 30:
                    raise Exception('Text incomplete')
            except Exception as error:
                print(f'OCR Error {error}')
                line_text = f'{erp_volpe_handler.ctrl_d(type_edging_header_pos.left + 100, line_pos.top + 3)} {erp_volpe_handler.ctrl_d(frame_header_pos.left + 100, line_pos.top + 3)}'
            line_text = line_text.replace('É', 'E')
            if edging_index not in line_text:
                # edging_type = erp_volpe_handler.ctrl_d(type_edging_header_pos.left + 100, line_pos.top + 3)
                # if edging_index not in edging_type.replace('É', 'E'):
                delete_line()      
            else:
                if 'CORTE REMOTO' in line_text and frame_type_checker(line_text, config['remote_edging']['exclude']): 
                    delete_line()
                    # else:
                    #     keyboard.press_and_release('down')
                    #     sleep(0.3)                        
                else:
                    keyboard.press_and_release('down')
                    sleep(0.5)
            old_code = code
            line_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 25, header_pos.top)))
            sleep(0.3)
            code = erp_volpe_handler.ctrl_d(code_pos.left + 30, line_pos.top + 3)
            if old_code == code:
                keyboard.press_and_release('down')
                sleep(0.5)
                line_pos = win_handler.image_search('Volpe_Table_selected.png', region=(erp_volpe_handler.region_definer(header_pos.left - 25, header_pos.top)))
                sleep(0.3)
                code = erp_volpe_handler.ctrl_d(code_pos.left + 30, line_pos.top + 3)
                if old_code == code:
                    break
        return
    except Exception as error:
        print(f'List delete error {error}')
        raise error


def wait_time(seconds=int):
    regressive_count = seconds
    for i in range(seconds):
        print(f'Waiting.......{regressive_count}')
        regressive_count = regressive_count - 1
        sleep(1.0)
    print('Waiting done')
    return


'''
==================================================================================================================================


            Main         Main        Main        Main       Main         Main           Main            Main            Main


==================================================================================================================================
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
                    '''
                    list coating and tinting for current product (may have slight changes later)
                                        '''
                    erp_volpe_handler.load_product_code(product['CODE'], 
                                    field_name='Product.png', 
                                    consult_button='Button_Consult.png', 
                                    path='Images/Coating_Config/')
                    '''
                    save current list if it exists
                        automation
                    read saved current list
                    move or delete read file
                    proccess values
                    delete duplacate values in current list
                        automation
                    compare lists
                    add missing values
                        automation
                            insert window
                            select product
                            select coating and tintings
                            execute
                    insert code and product at done_list
                    '''
            print('Done')
        except Exception as error:
            print(f'Error {error}')
            print(f'Try number {try_number + 1}')
            wait_time(5)