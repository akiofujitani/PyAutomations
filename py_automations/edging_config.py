import datetime, pyautogui, logging, keyboard
from data_modules import file_handler, data_communication, win_handler, json_config, erp_volpe_handler, log_builder
from ntpath import join
from time import sleep
from copy import deepcopy
from dataclasses import dataclass
from collections import namedtuple
from itertools import combinations
from threading import Event

logger = logging.getLogger('edging_config')  

'''
==================================================================================================================================



        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes          

==================================================================================================================================

'''

template = '''
{        
    "sheets_id" : "1ZS5BCBYj51YeVTek_TCyoXavjxeH9FxEwKRFfJY9Q1k",
    "number_tries" : 3,
    "file_name_pattern" : "Product_edging_",
    "report_path" : "C:/PyAutomations/Edging",
    "report_path_done" : "C:/PyAutomations/Edging/Done",
    "product_codes" : {
        "sheets_name" : "PRODUCT_CODES",
        "sheets_pos" : "A2:D"
    },
    "done_list" : {
        "sheets_name" : "DONE_LIST",
        "sheets_pos" : "A2:B"       
    },
    "edging_regular" : {
        "sheets_name" : "EDGING_REGULAR",
        "sheets_pos" : "A3:P"
    },
    "edging_remote" : {
        "sheets_name" : "EDGING_REGULAR",
        "sheets_pos" : "A3:P"        
    },
    "edging_special" : {
        "sheets_name" : "EDGING_SPECIAL",
        "sheets_pos" : "A2:F"         
    },
    "edging_frame" : {
        "sheets_name" : "EDGING_FRAME",
        "sheets_pos" : "A2:C"         
    },
    "edging_type" : {
        "sheets_name" : "INDEX_EDGING_TYPE",
        "sheets_pos" : "A2:2"         
    },
    "family_list" : {
        "sheets_name" : "FAMILY",
        "sheets_pos" : "A1:A"         
    }  
}
'''

Edging_List = namedtuple('Edging_List', 'default_baixo default_medio default_alto neg_baixo neg_medio neg_alto surf_baixo surf_medio surf_alto lp_baixo lp_medio lp_alto special ac_mdo ac10')
Edging_Index = namedtuple('Edging_Index', 'index_type')
Type_Frame = namedtuple('Type_Frame', ['type',  'frame'])
Sheets_Values = namedtuple('SheetsValues', 'sheets_name sheets_pos')
Config_Line = namedtuple('Config_Line', 'code edging_id frame_id')

@dataclass
class ConfigurationValues:
    sheets_id : str
    number_tries : int
    file_name_pattern : str
    report_path : str
    report_path_done : str
    product_codes : Sheets_Values
    done_list : Sheets_Values
    edging_regular : Sheets_Values
    edging_remote : Sheets_Values
    edging_special : Sheets_Values
    edging_frame : Sheets_Values
    edging_type : Sheets_Values
    family_list: Sheets_Values


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True


    @classmethod
    def check_create_insertion(cls, dict_values: dict):
        sheets_id = dict_values['sheets_id']
        number_tries = int(dict_values['number_tries'])
        file_name_pattern = dict_values['file_name_pattern']
        report_path = dict_values['report_path']
        report_path_done = dict_values['report_path_done']
        product_codes = Sheets_Values(*dict_values['product_codes'].values())
        done_list = Sheets_Values(*dict_values['done_list'].values())
        edging_regular = Sheets_Values(*dict_values['edging_regular'].values())
        edging_remote = Sheets_Values(*dict_values['edging_remote'].values())
        edging_special = Sheets_Values(*dict_values['edging_special'].values())
        edging_frame = Sheets_Values(*dict_values['edging_frame'].values())
        edging_type = Sheets_Values(*dict_values['edging_type'].values())
        family_list = Sheets_Values(*dict_values['family_list'].values())
        return cls(sheets_id, number_tries, file_name_pattern, report_path, report_path_done, product_codes, done_list, edging_regular, edging_remote, edging_special, edging_frame, edging_type, family_list)


'''
==================================================================================================================================

        Automations     Automations     Automations     Automations     Automations     Automations     Automations     

==================================================================================================================================
'''

def add_frame_type(codes_list: list) -> None:
    r'''
    Add frame type
    --------------

    Add values from list to the ERP list
    '''
    sleep(1)
    for code in codes_list:
        pyautogui.write(code)
        sleep(0.5)
        pyautogui.press('enter')
        sleep(0.5)
    pyautogui.press(['tab', 'tab', 'tab', 'tab', 'tab', 'tab'], interval=0.3)
    sleep(0.3)
    pyautogui.press('space')
    sleep(0.5)
    return



def add_product_codes(codes_list=list) -> None:
    r'''
    Add Product Codes
    -----------------

    Add product codes to "Incluir" window
    '''
    try:
        # win_title_pos = win_handler.image_search(window_title, path=path)
        for code in codes_list:
            sleep(0.4)
            pyautogui.write(code)
            sleep(0.3)
            pyautogui.press(['tab', 'tab'], interval=0.3)
            sleep(0.3)
            pyautogui.press('space')
            sleep(0.3)
            if len(code) == 4:
                pyautogui.press(['tab', 'tab', 'tab'], interval=0.3)
                sleep(0.3)
                pyautogui.write(code)
                sleep(0.5)
                pyautogui.press('enter')
                sleep(0.3)
                pyautogui.press(['tab', 'tab', 'tab', 'tab', 'tab', 'tab', 'tab'], interval=0.3)    
            else:
                pyautogui.press(['tab', 'tab', 'tab', 'tab', 'tab', 'tab',], interval=0.3)
                sleep(0.3)
                pyautogui.press('space')
                sleep(0.3)
                pyautogui.press(['tab', 'tab', 'tab', 'tab'], interval=0.3)
            sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            sleep(0.3)
        for _ in range(2):
            keyboard.press_and_release('shift+tab')
            sleep(0.3)
        pyautogui.press('space')
        sleep(0.3)
        # win_handler.icon_click('Button_Select.png', region_value=erp_volpe_handler.region_definer(win_title_pos.left, win_title_pos.top, 500, 600), path=path)
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


def __get_list_by_family(family: str, dict_values: dict, default: str='DEFAULT') -> list:
    if family not in dict_values.keys():
        logger.debug(f'{default} {dict_values[default]}')
        return default, deepcopy(dict_values[default])
    else:
        logger.debug(f'{family} {dict_values[family]}')
        return family, deepcopy(dict_values[family])


def __filter_by_index_type(index_type: str, fields_list: tuple, *args) -> list:
    filtered_list = []
    if len(args) > 0:
        for arg in args:
            if arg in fields_list:
                filtered_list.append(arg)
    index_type = index_type.lower()
    for field in fields_list:
        if index_type in field:
            filtered_list.append(field)
    return filtered_list


def __get_index_type(product_name: str, edging_type: dict) -> str:
    for key, edging in edging_type.items():
        if key in product_name:
            return edging.index_type     
    return None


def __filter_edging_by_index(product_name: str, edging_list: Edging_List, edging_type: dict, *args, **kwargs):
    r'''
    By product name and parameters, extract the valid edging list
    product_name: MF FREEVIEW HDI 1.74
    edging_list: Edging_List(default_baixo default_medio default_alto neg_baixo neg_medio neg_alto surf_baixo surf_meio surf_alto lp_baixo lp_medio lp_alto special ac_mdo)
    edging_type: {
        1.49 : BAIXO
        1.61 : MEDIO
    }
    kwargs : {'POLY' : '1.59', '1.50 BLUECUT' : '1.56', '1.50' : '1.49', 'POLI' : '1.59'} < for description swap
    '''
    for key, value in kwargs.items():
        if key in product_name:
            product_name = product_name.replace(key, value)
    index_type = __get_index_type(product_name, edging_type)
    if not index_type:
        return []
    fields_list = edging_list._fields
    filtered_fields = __filter_by_index_type(index_type, fields_list, *args)
    logger.debug(filtered_fields)

    edging_filtered = []
    for field_name in filtered_fields:
        field_value = getattr(edging_list, field_name)
        if field_value:
            edging_filtered.append(field_value)
    return edging_filtered


def wait_time(seconds=int):
    regressive_count = seconds
    for _ in range(seconds):
        logger.info(f'Waiting.......{regressive_count}')
        regressive_count = regressive_count - 1
        sleep(1.0)
    logger.info('Waiting done')
    return


def rule_evaluator(evaluate: any, condition: str, value: any) -> bool:
    r'''
    Support function for the product_special_coating
    '''
    match condition:
        case 'ENDS':
            if str(evaluate).endswith(value):
                return True
        case 'CONTAINS':
            if value in str(evaluate):
                return True
        case 'N_CONTAINS':
            if not value in str(evaluate):
                return True
        case 'LOWER':
            if float(evaluate) < float(value):
                return True
        case 'HIGHER':
            if float(evaluate) > float(value):
                return True
        case _:
            return False
    return False


def product_special_feature(product: dict, special_feature: dict, product_values: list, value_object: namedtuple):
    r'''
    Evaluate products based o values in sheets
    product -> CODE, DESCRIPTION, TYPE, FAMILY
    rule -> FAMILY, PRODUCT_PAR, CONDITION, VALUE, ADD_REMOVE, FEATURE_LIST

    '''
    if special_feature:
        for rule in special_feature:
            if rule['FAMILY'] == product['FAMILY']:
                if rule_evaluator(product[rule['PRODUCT_PAR']], rule['CONDITION'], rule['VALUE']):
                    rule_feature = [value_object(*feature.split(':')) for feature in rule['FEATURE_LIST'].split(',')]
                    for feature in rule_feature:
                        if feature in product_values:
                            product_values.remove(feature)
    return product_values


def convert_dict(sheets_values: dict, *args):
    r'''
    Verify sheets values and return values if exists
    '''
    if 'values' in sheets_values.keys():
        dict_values = data_communication.matrix_into_dict(sheets_values['values'], *args)
        return dict_values
    return


def dict_key_and_list(sheets_values: dict, values_object: namedtuple, key_column: int) -> dict:
    r'''
    Transform sheets matrix in dictionary with specific namedtuple as value and column number as key
    '''
    if 'values' in sheets_values.keys():
        new_dict = {}
        for item in sheets_values['values']:
            key_value = item[key_column]
            item.remove(item[key_column])
            if len(item) < len(values_object._fields):
                for _ in range(len(values_object._fields) - len(item)):
                    item.append('')
            new_dict[key_value] = values_object(*item)
        return new_dict
    return


def convert_column(sheets_values: dict, column: int) -> list:
    r'''
    Transform matrix column in list
    '''
    if 'values' in sheets_values.keys():
        return data_communication.column_to_list(sheets_values['values'], column)
    return


def edging_type_frame(frame_list: list, regular_edging: list, remote_edging: list):
    r'''
    Create a full list of frames and edging
    '''
    full_list = []
    for frame in frame_list:
        for edging in regular_edging:
            full_list.append(Type_Frame(edging, frame['CODE']))
        for edging in remote_edging:
            if frame['REMOTE'] == 'YES':
                full_list.append(Type_Frame(edging, frame['CODE']))
    return full_list


def find_duplicates_edging(service_code_list: list, *args):
    r'''
    Find duplicates in edging list
    '''
    full_list = []
    duplicate = []
    for service in service_code_list:
        temp_dict = []
        for arg in args:
            temp_dict.append(getattr(service, arg))
        if temp_dict in full_list:
            duplicate.append(service)
        else:
            full_list.append(temp_dict)
    return duplicate


def convert_named_type(values_list: list, named_tuple: namedtuple, *args) -> list:
    converted_list = []
    for value in values_list:
        converted_list.append(named_tuple(*[getattr(value, arg) for arg in args]))
    return converted_list


def remove_list(service_code_list: list, base_list: list) -> list:
    r'''
    Return list that is not in "base_list"
    base_list > Type_Frame = namedtuple('Type_Frame', ['type',  'frame'])
    service_code_list > Config_Line = namedtuple('Config_Line', 'code edging_id frame_id')

    '''
    service_remove_list = []
    for service in service_code_list:
        if not Type_Frame(getattr(service, 'edging_id'), getattr(service, 'frame_id')) in base_list:
            service_remove_list.append(service)
    return service_remove_list


def insert_filter(add_list: list) -> list:
    r'''
    Get add list and filter by frame volume
    '''
    matrix_values = values_to_matriz(add_list)
    new_add_list = max_column(matrix_values)
    logger.debug(new_add_list)
    for value in new_add_list:
        if value in add_list:
            add_list.remove(value)
    return new_add_list


def values_to_matriz(add_list: dict) -> list:
    r'''
    Transform list of frame/code to matrix
    '''
    row_list = set([add_value.frame for add_value in add_list])
    column_list = set([add_value.type for add_value in add_list])
    matrix = [[None for _ in range(len(row_list))] for _ in range(len(column_list))]
    for row_key, frame in enumerate(row_list):
        for column_key, code in enumerate(column_list):
            for add_value in add_list:
                if int(add_value.frame) == int(frame) and int(add_value.type) == int(code):
                    matrix[column_key][row_key] = add_value
    return matrix


def max_column(matrix: list) -> list:
    r'''
    Get column combinations and return the most present in matrix
    '''
    matrix_pos = []
    for row in matrix:
        temp_list = []
        for i, value in enumerate(row):
            if not value == None:
                temp_list.append(i)
        matrix_pos.append(temp_list)
    column_comb = all_combinations(unique_values(matrix_pos))
    print(column_comb)
    columns_list = count_columns(matrix_pos, column_comb)
    matrix_values = []
    for row in matrix:
        for column, value in enumerate(row):
            if column in columns_list and not value == None:
                matrix_values.append(value)
    return matrix_values


def unique_values(matrix: list):
    r'''
    Get columns numbers with values in matrix
    '''
    unique_list = []
    for row in matrix:
        for column in row:
            if column not in unique_list:
                unique_list.append(column)
    return unique_list


def all_combinations(unique_list: list):
    r'''
    Return all column combinations in matrix
    '''
    combinations_list = []
    for i in range(len(unique_list) + 1):
        combinations_list += combinations(unique_list, i)
    return combinations_list


def count_columns(matrix_pos: list, combination_list: list):
    r'''
    Count the most present column combination in matrix
    '''
    most_present_counter = 0
    most_present = ''
    for combination in combination_list:
        counter = 0
        if len(combination) > 0:
            for row in matrix_pos:
                if all(item in row for item in combination):
                    counter += 1
        if counter >= most_present_counter and len(combination) >= len(most_present):
            most_present_counter = counter
            most_present = combination
    return most_present


def main(config: ConfigurationValues, event: Event):
    try:
        codes_list = convert_dict(data_communication.get_values(config.product_codes.sheets_name, 
                                    config.product_codes.sheets_pos, 
                                    config.sheets_id),
                                    'CODE',
                                    'DESCRIPTION',
                                    'TYPE',
                                    'FAMILY')
        edging_frame = convert_dict(data_communication.get_values(config.edging_frame.sheets_name, 
                                    config.edging_frame.sheets_pos,
                                    config.sheets_id),
                                    'TYPE',
                                    'CODE',
                                    'REMOTE')
        edging_regular = dict_key_and_list(data_communication.get_values(config.edging_regular.sheets_name, 
                                    config.edging_regular.sheets_pos, 
                                    config.sheets_id), Edging_List, 0)
        edging_remote = dict_key_and_list(data_communication.get_values(config.edging_remote.sheets_name,
                                    config.edging_remote.sheets_pos,
                                    config.sheets_id), Edging_List, 0)
        feature_special = convert_dict(data_communication.get_values(config.edging_special.sheets_name, 
                                    config.edging_special.sheets_pos, 
                                    config.sheets_id), 
                                    'FAMILY', 
                                    'PRODUCT_PAR', 
                                    'CONDITION', 
                                    'VALUE', 
                                    'ADD_REM', 
                                    'FEATURE_LIST')
        edging_type = dict_key_and_list(data_communication.get_values(config.edging_type.sheets_name, 
                                    config.edging_type.sheets_pos, 
                                    config.sheets_id), Edging_Index, 0)
        family_list = convert_column(data_communication.get_values(config.family_list.sheets_name, 
                                    config.family_list.sheets_pos, 
                                    config.sheets_id), 0)
        logger.debug('Configuration done')
    except Exception as error:
        logger.critical(f'Error converting configuration values {error}')
        return
    # Get last uploaded date

    if event.is_set():
        logger.info('Event set')
        return

    for try_number in range(config.number_tries):
        try:        
            erp_volpe_handler.volpe_back_to_main()
            sleep(1)
            erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            erp_volpe_handler.volpe_open_window('Icon_Edging_Config.png', 'Title_Configuration_edging.png', path='Images/Edging_Config/')
            logger.info('Base automation done')

            if event.is_set():
                logger.info('Event set')
                return

            done_list = convert_dict(data_communication.get_values(config.done_list.sheets_name, config.done_list.sheets_pos, config.sheets_id), 'CODE', 'DESCRIPTION')

            logger.info('Sheets data loaded')
            done_list_code = [done_product['CODE'] for done_product in done_list] if done_list else ''
            for product in codes_list:
                if event.is_set():
                    logger.info('Event set')
                    return
                if not product['CODE'] in done_list_code and product['FAMILY'] in family_list:
                    # Load all services for the given product
                    product_edging_list = []
                    family_type, edging_regular_list = __get_list_by_family(product['FAMILY'], edging_regular)
                    family_type, edging_remote_list = __get_list_by_family(product['FAMILY'], edging_remote)
                    edging_regular_filtered = __filter_edging_by_index(product['DESCRIPTION'], edging_regular_list, edging_type, 'special', 'ac_mdo', 'ac10', **{'POLY' :'1.59', '1.50 BLUECUT' : '1.56', '1.50' : '1.49', 'POLI' : '1.59'})
                    edging_remote_filtered = __filter_edging_by_index(product['DESCRIPTION'], edging_remote_list, edging_type, 'special', 'ac_mdo', 'ac10', **{'POLY' :'1.59', '1.50 BLUECUT' : '1.56', '1.50' : '1.49', 'POLI' : '1.59'})
                    full_edging_list = edging_type_frame(edging_frame, edging_regular_filtered, edging_remote_filtered)

                    logger.debug(f'Edging list done {full_edging_list}')
                    sleep(1)
                    win_handler.activate_window('Volpe')
                    product_code = f'{int(product["CODE"]):04d}' if len(product['CODE']) < 4 else product['CODE']
                    erp_volpe_handler.load_product_code(product_code, 
                                    field_name='Product.png', 
                                    consult_button='Button_Consult.png', 
                                    path='Images/Edging_Config/')
                    file_name = f'{config.file_name_pattern}{product["CODE"]}.txt'
                    erp_volpe_handler.volpe_save_report(file_name, config.report_path)
                    
                    # Evaluate items
                    current_service_list = file_handler.CSVtoList(join(config.report_path, file_name))
                    service_code_list = [Config_Line(line['CÓDIGO'], line['ID.MONTAGEM'], line['ID.ARMACAO']) for line in current_service_list]
                    if len(service_code_list) > 0:
                        product['DESCRIPTION'] = current_service_list[0]['PRODUTO'] 
                    full_edging_list = product_special_feature(product, feature_special, full_edging_list, Type_Frame)
                    logger.debug(f'Current code list loaded {product_code}')
                    

                    # Remove list creation
                    duplicates = find_duplicates_edging(service_code_list, 'edging_id', 'frame_id')
                    no_duplicates_service_list = [service for service in service_code_list if service not in duplicates]
                    remove_service_list = remove_list(no_duplicates_service_list, full_edging_list) + duplicates

                    # Add list creation
                    type_frame_service_list = convert_named_type(no_duplicates_service_list, Type_Frame, 'edging_id', 'frame_id')
                    add_list = [item for item in full_edging_list if item not in type_frame_service_list]

                    if len(remove_service_list) > 0 or len(add_list) > 0:
                        column_pos = win_handler.image_search('header_code.png', path='Images/Edging_Config')

                    if event.is_set():
                        logger.info('Event set')
                        return

                    #Delete items
                    if len(remove_service_list) > 0:
                        try:
                            for delete_item in remove_service_list:
                                erp_volpe_handler.delete_from_table(column_pos, delete_item.code, False)
                        except Exception as error:
                            logger.error(f'Could not delete item due {error}')
                            raise error
                    
                    if event.is_set():
                        logger.info('Event set')
                        return

                    # Add items                    
                    add_list_codes = ', '.join([f'{str(add.type)}:{str(add.frame)}' for add in add_list]) if len(add_list) > 0 else ''
                    if len(add_list) > 0:
                        try:
                            while len(add_list) > 0:
                                new_add_list = insert_filter(add_list)
                                if len(new_add_list) > 0:
                                    pyautogui.rightClick(column_pos.left, column_pos.top + 100)
                                    sleep(0.3)
                                    pyautogui.press('i')
                                    sleep(0.5)
                                    config_coat_win_pos = win_handler.image_search('Title_Edging_Config_Include.png', path='Images/Edging_Config')
                                    pyautogui.press('space')
                                    # Insert product code
                                    add_product_codes([product_code])
                                    sleep(0.3)
                                    pyautogui.press('tab')
                                    sleep(0.3)
                                    pyautogui.press('space')
                                    sleep(0.6)
                                    # insert frames
                                    add_frame_type(set([add_edging.frame for add_edging in new_add_list]))
                                    sleep(0.3)
                                    pyautogui.press('tab')
                                    sleep(0.3)
                                    pyautogui.press('space')
                                    sleep(0.6)
                                    # Insert edgint type
                                    add_product_codes(set([add_edging.type for add_edging in new_add_list]))
                                    sleep(0.3)
                                    pyautogui.press('tab')
                                    sleep(0.5)
                                    pyautogui.press('space')
                                    sleep(3)
                                    
                                    if event.is_set():
                                        logger.info('Event set')
                                        return

                        except Exception as error:
                            logger.error(f'Insertion error due {error}')
                            raise error
                    logger.info(f'{product["CODE"]} Done')
                    file_handler.file_move_copy(config.report_path, config.report_path_done, file_name, False)
                    now_datetime = datetime.datetime.now()
                    data_communication.data_append_values(config.done_list.sheets_name, 
                                        config.done_list.sheets_pos, 
                                        [[product_code, 
                                        product['DESCRIPTION'], 
                                        ', '.join([f'{str(delete.edging_id)}:{str(delete.frame_id)}' for delete in remove_service_list]) if len(remove_service_list) > 0 else '',
                                        add_list_codes,
                                        now_datetime.strftime('%d/%m/%Y'), 
                                        now_datetime.strftime('%H:%M:%S')]], 
                                        config.sheets_id)
                    logger.info(f'{product["DESCRIPTION"]} done')
            logger.info('Done')
        except Exception as error:
            logger.critical(f'Error {error}')
            logger.critical(f'Try number {try_number + 1}')
            wait_time(5)
    return


def quit_func():
    logger.info('Quit pressed')
    event.set()
    return


# def quit_func():
#     logger.info('Quit pressed')
#     event.set()
#     return



'''
==========================================================================================================================================


            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN            MAIN


==========================================================================================================================================
'''


if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)

    try:
        config_dict = json_config.load_json_config('c:/PyAutomations_Reports/edging_config.json', template)
        config = ConfigurationValues.check_create_insertion(config_dict)
    except Exception as error:
        logger.critical(f'Could not load config file {error}')
        exit()

    event = Event()
    keyboard.add_hotkey('esc', quit_func)    

    main(config, event)
    