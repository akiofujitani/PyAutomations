import logging
import pyautogui
import keyboard
import pyscreeze
from threading import Event
from pynput import keyboard as pynkeyboard
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
from os.path import join, normpath
from time import sleep
from data_modules.file_handler import CSVtoList, file_move_copy, file_list
from data_modules import win_handler
from data_modules import erp_volpe_handler
from data_modules import log_builder


logger = logging.getLogger('product_blocking')


def delete_from_table(column_pos=pyscreeze.Box, delete_value=str, deactivate_middle_search=True) -> None:
    try:
        pyautogui.rightClick(column_pos.left + 10, column_pos.top + 5)
        sleep(0.3)
        pyautogui.write(delete_value)
        sleep(0.3)
        logger.debug(f'{delete_value} deleted')
        if deactivate_middle_search:
            for _ in range(3):
                keyboard.press_and_release('tab')
                sleep(0.3)
            keyboard.press_and_release('space')
            sleep(0.3)
            for _ in range(2):
                keyboard.press_and_release('shift + tab')
                sleep(0.3)
            keyboard.press_and_release('space')
        else:
            for _ in range(2):
                keyboard.press_and_release('enter')
                sleep(0.3)
        sleep(0.3)
        keyboard.press_and_release('delete')
        sleep(0.7)
        win_title = win_handler.get_active_windows_title()
        sleep(0.5)
        if 'DELETAR' in win_title:
            pyautogui.press('s')
            sleep(0.5)
            return
        if 'AVISO' in win_title:
            logger.warning(f'Could not find {delete_value} value.')
            keyboard.press_and_release('space')
            sleep(0.5)
            return
        else:
            raise Exception(f'Error in {delete_value} exclusion')
    except Exception as error:
        logger.error(f'Error deleting code due {error}')
        raise error


def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None


def load_customer(customer_code: int, field_pos) -> bool:
    try:
        sleep(0.3)
        win_handler.click_field(field_pos)
        sleep(0.6)
        pyautogui.hotkey('ctrl', 'a')
        sleep(0.5)
        pyautogui.write(customer_code)
        sleep(0.3)
        pyautogui.press('tab')
        sleep(0.2)
        pyautogui.press('space')
    except Exception as error:
        logger.error(f'Load customer code error {error}')
        raise Exception(f'Load customer code {error}')        


def initial_set():
    erp_volpe_handler.volpe_open_window('Icon_Products_block.png', 'Title_Products_block.png', path='Images/Registry/')
    sleep(1)
    pyautogui.press('tab')
    sleep(0.3)
    pyautogui.write('499')
    sleep(0.5)
    pyautogui.press('tab')
    sleep(0.3)
    pyautogui.press('space')
    sleep(1)
    win_handler.icon_click('Link_registry_500.png', path='Images/Registry/')
    sleep(1)
    keyboard.press_and_release('down')
    sleep(0.3)
    keyboard.press_and_release('enter')
    sleep(0.3)
    pyautogui.press('tab')
    sleep(0.5)
    pyautogui.press('space')
    sleep(0.3)    
    return


def filter_values(main_list: list, values_list: list) -> list:
    filtered_list = []
    values_product_id_list = [value.get('code') for value in values_list]
    for value in main_list:
        if value.get('product_id') in values_product_id_list:
            filtered_list.append(value)
    if len(filtered_list) == 0:
        return None
    return filtered_list


def get_done_list(done_path: str, extension: str) -> list:
    done_file_list = file_list(done_path, extension)
    done_list = [file.replace('.txt', '') for file in done_file_list]
    return done_list


def format_csv_load_to_dict(list_csv: list, headers: tuple, reverse: bool=False) -> list:
    try:
        values_list = []
        for value_csv in list_csv:
            values_dict = {}
            for i, value in enumerate(value_csv.values()):
                values_dict[headers[i]] = value
            values_list.append(values_dict)
        if reverse:
            values_list.reverse()
        return values_list
    except Exception as error:
        logger.error(f'Could not format csv list due {error}')
        return None


def on_press(key):
    # if key == keyboard.Key.esc:
    #     event.set()
    #     return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['f12']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        event.set()
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys


def main(event: Event):
    try:
        customer_csv = CSVtoList('./rj_customer.csv', delimeter_char=';')
        product_csv = CSVtoList('./toppro_list.csv', delimeter_char=';')
        
        customer_list = format_csv_load_to_dict(customer_csv, ('status', 'code', 'name', 'full_name'), True)
        product_list = format_csv_load_to_dict(product_csv, ('code', 'description'))

        report_path = normpath('C:/PyAutomations_Reports/Product_Block')
        report_path_done = normpath('H:/Informatica/Products_block_done')
        if event.is_set():
            return
    except Exception as error:
        logger.error(f'Could not load values due {error}')
        quit()

    try:
        erp_volpe_handler.volpe_back_to_main()
        erp_volpe_handler.volpe_load_tab('Tab_Reg', 'Icon_Reg_par.png')
        initial_set()
        if event.is_set():
            return
        field_pos = win_handler.image_search('Field_registry.png', path='Images/Registry/')
        product_code_pos = win_handler.image_search('Product_block_code.png', path='Images/Registry/')

        for customer in customer_list:
            if event.is_set():
                return   
            logger.info(f'{customer.get("code")} - {customer.get("name")}')
            sleep(0.3)
            customer_code = customer.get('code').replace('.', '')
            done_list = get_done_list(report_path_done, 'txt')
            if customer_code not in done_list and customer_code:
                if event.is_set():
                    return                
                load_customer(customer_code, field_pos)
                sleep(3)
                file_name = f'{customer_code}.txt'
                erp_volpe_handler.volpe_save_report(file_name, report_path)
                sleep(0.5)
                blocked_product_csv = CSVtoList(join(report_path, file_name))
                blocked_list = format_csv_load_to_dict(blocked_product_csv, ('x', 'code', 'customer', 'customer_name', 'product_id', 'product'))
                filtered_values = filter_values(blocked_list, product_list)
                if filtered_values:
                    for delete_code in filtered_values:
                        if event.is_set():
                            return                        
                        delete_from_table(product_code_pos, delete_code.get('code'))
                file_move_copy(report_path, report_path_done, file_name, False, True)
                done_list.append(customer_code)
                logger.info(f'Customer {customer_code} done')
    except Exception as error:
        logger.error(f'Error in automation due {error}')
        return

if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)
    event = Event()
    listener = pynkeyboard.Listener(on_press=on_press, args=(event, ))
    listener.start()  # start to listen on a separa11te thread

    for i in range(5):
        main(event)