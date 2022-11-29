import datetime, file_handler, data_communication, win_handler, data_organizer, json_config, erp_volpe_handler, pyautogui, keyboard, sys, os
from ntpath import join
from time import sleep

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def load_product_code(code):
    try:
        product_pos = win_handler.image_search('Product.png', path='Images/Edging_Config/')
        win_handler.click_field(product_pos, 'Bellow', 15)
        sleep(0.3)
        pyautogui.click()
        sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.5)
        pyautogui.write(code)
        sleep(0.3)
        win_handler.icon_click('Button_Consult.png', path='Images/Edging_Config/')
        return
    except Exception as error:
        raise Exception(f'Load product code {error}')


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


if __name__ == '__main__':
    # erp_volpe_handler.volpe_back_to_main()
    try:
        config = json_config.load_json_config('edging_config.json')
    except:
        print('Could not load config file')
        exit()

    # Load config

    sheets_name = config['data']['sheets_name']
    sheets_id = config['data']['sheets_id']
    sheets_pos = config['data']['sheets_pos']
    sheets_name_done = config['data']['sheets_name_done']
    sheets_pos_done = config['data']['sheets_pos_done']


    # Get last uploaded date

    for try_number in range(config['parameters']['number_tries']):
        try:
            erp_volpe_handler.volpe_back_to_main()
            sleep(0.5)
            erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            sleep(0.5)
            erp_volpe_handler.volpe_open_window('Icon_config_edging.png', 'Configuration_edging.png', path='Images/Edging_Config/')

            print('Base automation done')

            data_list = data_communication.get_values(sheets_name, sheets_pos, sheets_id)
            done_list = data_communication.get_values(sheets_name_done, sheets_pos_done, sheets_id)
            print('Sheets data loaded')

            product_done_list = ''
            if 'values' in done_list.keys():
                product_done_list = data_communication.matrix_into_dict(done_list['values'], 'CODE', 'DESCRIPTION')
            if 'values' in data_list.keys():
                product_list = data_communication.matrix_into_dict(data_list['values'], 'CODE', 'DESCRIPTION')
            print('Sheets data converted')

            for product in product_list:
                if not product['CODE'] in list(done_product['CODE'] for done_product in product_done_list):
                    load_product_code(product['CODE'])
                    list_delete_edging_config(product, config)
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