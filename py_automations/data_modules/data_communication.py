import datetime,  logging
from . import sheets_API, file_handler, json_config, log_builder

logger = logging.getLogger('data_communication')


template_data = '''
{
"sheets_id" : "1aqLuNRknJc6ewS7Cehq-8j1kbCPnEftuTrsUelGhpTQ",
"SCOPE" : ["https://www.googleapis.com/auth/spreadsheets"]
}
'''

sheets_values = json_config.load_json_config('sheets_config.json', template_data)
SPREADSHEET_ID = sheets_values['sheets_id']
creds = sheets_API.load_creds()


def get_last_date(sheets_name: str, position: str, minimum_date: str='01/01/2020', sheets_id: str=SPREADSHEET_ID) -> datetime.datetime.date:
    '''
    Get last valid date on selected sheets based on its first column values
    '''
    range_name = f'{sheets_name}!{position}'
    try:
        sheet_loaded = sheets_API.get_values(creds, sheets_id, range_name)
        if len(sheet_loaded['values']) == 0:
            raise Exception('No values in sheets')
    except Exception as error:
        logger.error(f'Get last date error {error}')
        return datetime.datetime.strptime(minimum_date, '%d/%m/%Y').date()
    return return_last_row_date(sheet_loaded)


def get_values(sheets_name, position, sheets_id=SPREADSHEET_ID):
    range_name = f'{sheets_name}!{position}'
    try: 
        return sheets_API.get_values(creds, sheets_id, range_name)
    except Exception as error:
        raise error


def return_last_row_date(sheet_values):
    try:
        date_string = sheet_values['values'][len(sheet_values['values']) - 1][0]
    except KeyError as error:
        logger.error(f'No values found in table {error}')
        return
    return datetime.datetime.strptime(date_string, '%d/%m/%Y').date()


def transform_in_sheet_matrix(dict_list):
    '''
    Transform dictionary list in list of list (matrix like)
    Must be moved 
    '''
    rows_list = []
    for item in dict_list:
        rows_list.append(list(item.values()))
    return rows_list


def matrix_into_dict(matrix_values, *args):
    '''
    Transform sheets values matrix into dictionary
    args must be the correct amount
    ''' 
    if not len(matrix_values[0]) == len(args):
        raise Exception('Args does not match')
    
    matrix_list_dict = []
    temp_dict = {}
    for line in matrix_values:
        if len(line) < len(args):
            for i in range(len(args) - len(line)):
                line.append('')
        for i in range(len(args)):
            temp_dict[args[i]] = line[i] if line[i] else ''
        matrix_list_dict.append(temp_dict)
        temp_dict = {}
    logger.debug('matriz converted to dict')
    return matrix_list_dict


def transform_list_in_coloumn(values_list=list):
    row_list = []
    for item in values_list:
        row_list.append([item])
    logger.debug('list converted in column')
    return row_list


def file_list_last_date(path=str, extension=str, pattern_removal=str, date_pattern=str):
    '''
    Retrieves the last defined data in file list.
    This don't retrieves the creattion date, its the date defined in the file name
    '''
    try:
        file_list = file_handler.file_list(path, extension)
        date_list = []
        for file in file_list:
            file_extension = file.split('.')
            date_list.append(datetime.datetime.strptime(file_extension[0].replace(pattern_removal, ''), date_pattern).date())
            date_list.sort(reverse=True)
        logger.debug(date_list[0])
        return date_list[0]
    except Exception as error:
        logger.error(error)
        return None


def data_append_values(sheets_name, range, values, sheets_id=SPREADSHEET_ID):
    '''
    Append values to sheet, if error try to create sheet.
    '''
    sheets_name_range = f'{sheets_name}!{range}'
    try:
        sheets_API.get_values(creds, sheets_id, sheets_name_range)
        logger.info(f'{sheets_name_range} found')
    except:
        try:
            logger.info(f'Tring to create sheet {sheets_name}')
            result = sheets_API.add_sheet(creds, sheets_id, sheets_name)
            logger.info(result)
        except Exception as error:
            logger.error(error)
            raise error
    return sheets_API.append_values(creds, sheets_id, sheets_name_range, 'USER_ENTERED', values)


def clean_complete_values_dict(values_dict=list, dict_date_name=str, template_value=dict, sheets_name=str, search_range=str):
    '''
    Clean and complete dict.
    '''
    last_row_date = get_last_date(sheets_name, search_range)
    values_dict_first_date = datetime.datetime.strptime(values_dict[0][dict_date_name], '%d/%m/%Y')
    date_difference = values_dict_first_date - last_row_date
    if not date_difference.days == 1:
        if date_difference < datetime.timedelta(days=1):
            for _ in range(abs(date_difference.days) + 1):
                values_dict.pop(0)
        else:
            temp_values_dict = values_dict
            values_dict = []
            between_date = last_row_date
            for i in range(date_difference.days - 1):
                between_date = between_date + datetime.timedelta(days=1)
                template_value[dict_date_name] = between_date.strftime('%d/%m/%Y')
                values_dict.append(template_value[dict_date_name])
            values_dict = values_dict + temp_values_dict
    if not len(values_dict) == 0:
        return values_dict


def data_update_values(sheets_name=str, range=str, values=list, sheets_id=SPREADSHEET_ID):
    sheets_name_range = f'{sheets_name}!{range}'
    try:
        sheets_values = sheets_API.get_values(creds, sheets_id, sheets_name_range)
        logger.info(f'{sheets_name_range} found')
        range_details = range.split(':')
        if "values" in sheets_values.keys():
            sheets_name_range = f'{sheets_name}!{range_details[0]}{len(sheets_values["values"]) + 1}:{range_details[1]}'
    except:
        try:
            logger.info(f'Tring to create sheet {sheets_name}')
            result = sheets_API.add_sheet(creds, sheets_id, sheets_name)
            logger.info(result)
        except Exception as error:
            logger.error(error)
            raise error
    return sheets_API.update_values(creds, sheets_id, sheets_name_range, 'USER_ENTERED', values)


def data_update_value(sheets_name=str, range=str, value=list, sheets_id=SPREADSHEET_ID):
    sheets_name_range = f'{sheets_name}!{range}'
    try:
        sheets_value = sheets_API.get_values(creds, sheets_id, sheets_name_range)
        logger.info(f'{sheets_name_range} found')
        sheets_API.update_values(creds, sheets_id, sheets_name_range, 'USER_ENTERED', value)
        if 'values' in sheets_value.keys():
            logger.info(f'{sheets_value["values"][0]} overwritten by {value} in {sheets_name} at {range}')
        else:
            logger.info(f'{value} inserted in {sheets_name} at {range}')
        return
    except Exception as error:
        logger.error(error)
        raise error


def column_to_list(sheets_values, column_number=0):
    values_list = []
    for row in sheets_values:
        if len(row) >= column_number + 1 and len(row[column_number]) > 0:
            values_list.append(row[column_number])
    return values_list


def list_to_dict_with_key(dict_list, key):
    dict_temp = {}

    for dict_values in dict_list:
        key_value = dict_values.pop(key)
        if key_value in dict_temp.keys():
            dict_temp[key_value] = dict_temp[key_value] + [dict_values]
        else:
            dict_temp[key_value] = [dict_values]
    return dict_temp


def list_to_dict_key_and_list(values_list, key_index) -> dict:
    dict_temp = {}

    for values in values_list:
        key_name = values.pop(key_index)
        dict_temp[key_name] = [values for values in values if values != '']
    return dict_temp

    
def convert_number_to_letter(column_int):
    start_index = 1   #  it can start either at 0 or at 1
    letter = ''
    while column_int > 25 + start_index:   
        letter += chr(65 + int((column_int-start_index)/26) - 1)
        column_int = column_int - (int((column_int-start_index)/26))*26
    letter += chr(65 - start_index + (int(column_int)))
    return letter


if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)
    
    try:
        config = json_config.load_json_config('config_volpe.json')
    except:
        logger.critical('Could not load config file')
        exit()
    
    sheets_id = config['heat_map']['sheets_id']
    sheets_name = config['heat_map']['status_list']['sheets_name']
    sheets_pos_ff = config['heat_map']['status_list']['free_form']
    sheets_pos_tr = config['heat_map']['status_list']['coating']
    sheets_pos_ed = config['heat_map']['status_list']['edging']

    logger.debug(sheets_id)
    logger.debug(sheets_name)

    sheets_values = get_values(sheets_name, sheets_pos_ff, sheets_id)

    column_values = column_to_list(sheets_values)
    logger.debug(sheets_values)
    logger.debug(column_values)
    logger.debug()

    if __name__ == '__main__':
        print('Main')