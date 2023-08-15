import os, pyautogui
from data_modules import file_handler, data_organizer, json_config, erp_volpe_handler, win_handler, data_communication, ocr_text_reader
from ntpath import join
from time import sleep


def process_detail(detail_contents):
    detail_processed = []
    for line in detail_contents:
        detail_processed.append(line['MODELO'])
        detail_processed.append(line['VL. ORIGINAL'])
        detail_processed.append(line['PREÇO TOTAL'])
    return detail_processed


def load_details(reference_pos_image, path='Images'):
    try:
        referen_pos = win_handler.image_search(reference_pos_image, path=path)
        win_handler.click_field(referen_pos, 'Bellow', distanceY=20)
        sleep(0.5)
        pyautogui.hotkey('ctrl', 't')
        win_handler.loading_wait('Title_properties.png', path=path)
        sleep(0.3)
        erp_volpe_handler.volpe_tab_select('Tab_process_data', path=path)
    except Exception as error:
        print(f'Load details {error}')
        raise error
    return


def get_second_pair():
    try:
        sheet_header_pos = win_handler.image_search('Sheet_header.png', path='Images/Sells')
        win_handler.click_field(sheet_header_pos, 'Bellow', distanceY=20)
        sleep(0.5)
        pyautogui.press('z')
        sleep(0.3)
        erp_volpe_handler.message_box_confirm()
    except Exception as error:
        print(error)



if __name__ == '__main__':    
    try:
        config = json_config.load_json_config('second_pair_config.json')
    except:
        print('Could not load config file')
        exit()
    
    path = file_handler.check_create_dir(os.path.normpath(config['path']))
    path_done = file_handler.check_create_dir(os.path.normpath(config['path_done']))
    path_detail = file_handler.check_create_dir(os.path.normpath(config['path_detail']))
    path_detail_done = file_handler.check_create_dir(os.path.normpath(config['path_detail_done']))
    extension = config['extension']
    sheets_id = config['sheets_id']
    sheets_name = config['sheets_name']
    sheets_order_pos = config['order_num_pos']
    remove_list = config['remove_fields']

    sheets_values = data_communication.get_values(sheets_name, sheets_order_pos, sheets_id)
    order_number_list = ''
    if 'values' in sheets_values.keys():
        order_number_list = data_communication.column_to_list(sheets_values, 0)
    file_list = file_handler.file_list(path, extension)


    file_contents = []
    for file in file_list:
        file_contents = file_contents + file_handler.CSVtoList(join(path, file))

    updated_order_list = data_organizer.remove_from_dict(file_contents, *remove_list)


    if len(updated_order_list) > 0:
        try:
            # erp_volpe_handler.volpe_back_to_main()
            # erp_volpe_handler.volpe_load_tab('Tab_Sells', 'Icon_sell_parameter.png')
            # erp_volpe_handler.volpe_open_window('Icon_sell_order.png', 'Title_sell_order.png')      
            sheet_header_pos = win_handler.image_search('Sheet_header.png', path='Images/Sells')
            for order in updated_order_list:
                if order['CÓDIGO'] not in order_number_list:
                    win_handler.click_field(sheet_header_pos, 'Bellow', distanceY=20)
                    sleep(0.5)
                    pyautogui.hotkey('ctrl', 'n')
                    sleep(0.5)
                    win_handler.loading_wait('filter_by_id.png', path='Images/Sells')
                    pyautogui.write(order['CÓDIGO'])
                    sleep(0.3)
                    pyautogui.press('tab')
                    sleep(0.3)
                    pyautogui.press('enter')
                    sleep(0.5)
                    get_second_pair()
                    load_details('Sheet_detail_header.png', path='Images/Sells')
                    erp_volpe_handler.volpe_save_report(f'{order["CÓDIGO"]}.txt', path_detail, reference='Title_properties.png', load_report_path='Images/Sells')
                    sleep(0.3)
                    win_handler.icon_click('Volpe_Close.png')
                    details_file_list = file_handler.file_list(path_detail, extension)
                    file_details = []
                    for file in details_file_list:
                        file_details = file_details + file_handler.CSVtoList(join(path_detail, file))
                        file_handler.file_move_copy(path_detail, path_detail_done, file, False)
                    filtered_data = process_detail(file_details)
                    temp_list = list(order.values()) + filtered_data
                    data_communication.data_append_values(sheets_name, "A:Z", [temp_list], sheets_id)
                    print(f'Done {order["CÓDIGO"]}')
        except Exception as error:
            print(f'Error {error}')
    print('Test')
