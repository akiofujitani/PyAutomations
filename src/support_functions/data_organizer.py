from audioop import reverse
from ntpath import join

from cv2 import sort
import file_handler, datetime, calendar
from collections import Counter

'''
filter_tag
checkData
isFloat
matchAndReturn
jobAndFileDate
dict_list_to_plain_dict
length_counter
return_keys
plain_dict_list_filler
'''


def filter_tag(job_data, base_name, *args):
    '''
    filter tags based on tag's list
    '''
    filtered_data = {}
    filtered_data[base_name] = job_data[base_name]
    for arg in args:
        if arg in job_data.keys():
            filtered_data[arg] = job_data[arg]
    return filtered_data


def checkData(tag, convertedData):
    '''
    Check number of values inside TAG
    '''

    countOne = 0
    countTwo = 0
    for line in convertedData:
        if tag in line.keys():
            match len(line[tag]):
                case 1:
                    countOne += 1
                case 2:
                    countTwo += 1
    print(f'{tag} checked')
    return 2 if countTwo > countOne else 1



def isFloat(number):
    '''
    Check if values if float compatible
    '''

    try:
        float(number)
        return True
    except ValueError:
        return False


def plain_dict_float_format(plain_dict):
    float_updated_plain_dict = []    
    for line in plain_dict:
        temp_dict = {}
        for key in line.keys():
            print(line[key])
            if not line[key] == 0 and isFloat(line[key]):
                temp_dict[key] = str(line[key]).replace('.',',')
            else:
                temp_dict[key] = line[key]
        float_updated_plain_dict.append(temp_dict)
        print('Float values converted')
    return float_updated_plain_dict


def matchAndReturn(number):
    '''
    Matching and retuning values to auto fill
    '''

    valuesKey = {}
    match number:
        case 2:
            valuesKey = {'MIDR' : 'ABSENT', 
            'MIDL' : 'ABSENT', 
            'NEWR' : 'ABSENT', 
            'NEWL' : 'ABSENT'}
        case 1:
            valuesKey = {'MID' : 'ABSENT', 
            'NEW' : 'ABSENT'}
    return valuesKey


def jobAndFileDate(filePath, fileList):
    job_list = []
    for file in fileList:
        tempDict = file_handler.CSVtoList(join(filePath, file))
        tempJobSet = set()
        for line in tempDict:
            tempJobSet.add(line['PEDIDO'])
        fileDate = file_handler.fileCreationDate(join(filePath, file))
        job_list.append({fileDate.strftime('%d-%m-%Y') : tempJobSet})
    return job_list


def dict_list_to_plain_dict(dict_list):
    print('Converting to simple dict')
    plain_dict = []
    for line in dict_list:
        line_dict = {}
        for key_name in line.keys():
            if type(line[key_name]) == dict:
                for key_name_detail in line[key_name]:
                    if type(line[key_name][key_name_detail]) == dict:
                        temp_values = ''
                        for value in line[key_name][key_name_detail]:
                            temp_values += f';{value}'
                        temp_values = temp_values.replace(';', '', 1)
                        line_dict[f'{key_name}_{key_name_detail}'] = temp_values
                    else:
                        line_dict[f'{key_name}_{key_name_detail}'] = line[key_name][key_name_detail]
            else:
                line_dict[key_name] = line[key_name]
        plain_dict.append(line_dict)
    return plain_dict


def tags_dict_to_plain_dict(keys_dict=dict):
    plain_dict = {}
    for key_name in keys_dict.keys():
        if type(keys_dict[key_name]) == dict:
            for key_name_detail in keys_dict[key_name]:
                plain_dict[f'{key_name}_{key_name_detail}'] = keys_dict[key_name][key_name_detail]
        else:
            plain_dict[key_name] = keys_dict[key_name]
    return plain_dict


def length_counter(plain_dict):
    count_list = []
    for line in plain_dict:
        count_list.append(len(line))
    values_counter = Counter(count_list)
    sorted_value = list(values_counter.keys())
    return max(sorted_value)


def return_keys(plain_dict, default_length):
    for line in plain_dict:
        if len(line) == default_length:
            return list(line.keys())


def plain_dict_list_filler(plain_dict, *args):
    default_length = length_counter(plain_dict)
    default_keys_list = return_keys(plain_dict, default_length)
    for default_key in args:
        if default_key not in default_keys_list:
            default_keys_list.append(default_key)
    updated_plain_dict = []
    for line in plain_dict:
        temp_dict = {}
        for key in default_keys_list:
            if key in line.keys():
                temp_dict[key] = line[key]
            elif f'{key}_R' in line.keys():
                temp_dict[key] = f'{line[f"{key}_R"]};{line[f"{key}_L"]}'
            else: temp_dict[key] = 'Absent'
        updated_plain_dict.append(temp_dict)
    return updated_plain_dict


def plain_dict_extract_keys(plain_dict=dict):
    default_length = length_counter(plain_dict)
    for dict_value in plain_dict:
        if len(dict_value) == default_length:
            return list(dict_value.keys())


def plain_dict_list_completer(plain_dict=list):
    keys_list = plain_dict_extract_keys(plain_dict)
    updated_plain_dict = []
    for values_dict in plain_dict:
        temp_dict = {}
        for key in keys_list:
            if key not in values_dict.keys():
                temp_dict[key] = ''
            else:
                temp_dict[key] = values_dict[key]
        updated_plain_dict.append(temp_dict)
    return updated_plain_dict


# def plain_dict_list_filler(plain_dict, *args):
#     default_length = length_counter(plain_dict)
#     default_keys_list = return_keys(plain_dict, default_length)
#     for default_key in args:
#         if default_key not in default_keys_list:
#             default_keys_list.append(default_key)
#     updated_plain_dict = []
#     for line in plain_dict:
#         temp_dict = {}
#         if len(line) == default_length:
#             updated_plain_dict.append(line)
#         if len(line) < default_length:
#             for key in default_keys_list:
#                 if key in line.keys():
#                     temp_dict[key] = line[key]
#                 else:
#                     temp_dict[key] = 'Absent'
#             updated_plain_dict.append(temp_dict)
#         if len(line) > default_length:
#             double_value = ''
#             for key in line.keys():
#                 if key in default_keys_list:
#                     temp_dict[key] = line[key]
#                 else:
#                     double_value = double_value + f'{line[key]}'
#             for key in default_keys_list:
#                 if key not in line.keys():
#                     temp_dict[key] = double_value
#             updated_plain_dict.append(temp_dict)
#     return updated_plain_dict


def retrieve_file_name_date(file_name=str, name_pattern=str, date_format=str):
    return datetime.datetime.strptime(file_name.replace(name_pattern, '').split('.')[0], date_format)


def define_start_date(date_1, date_2):
    date_diff = date_1 - date_2
    if date_diff == datetime.timedelta(days=0):
        return date_1
    start_date = date_1 - date_diff
    if start_date == date_1 or start_date == date_2:
        plus_date = datetime.timedelta(days=1)
        return start_date + plus_date
    return start_date


def dict_values_compare(values, conditional):
    if type(values) == dict:
        for key in values.keys():
            if value_compare(values[key], conditional):
                return True
    else:
        return value_compare(values, conditional)


# Make more generic
def filter_tag_by_values(data_list, tag_conditionals):
    filtered_values = []
    for data in data_list:
        for conditional in tag_conditionals:
            if conditional['Tag'] in data and dict_values_compare(data[conditional['Tag']], conditional):
                filtered_values.append(data)
    return filtered_values


def value_compare(value, conditional):
    value = value_type_definer(value)
    if not value == '':
        match conditional['Operator']:
            case '<':
                if value < conditional['Value']:
                    return True
            case '>':
                if value > conditional['Value']:
                    return True
            case '<=':
                if value <= conditional['Value']:
                    return True
            case '>=':
                if value >= conditional['Value']:
                    return True
            case '=':
                if value == conditional['Value']:
                    return True
            case 'contains':
                if conditional['Value'] in value:
                    return True
    return False


def value_type_definer(value):
    if '.' in value:
        return float(value) if isFloat(value) else value
    try:
        return int(value)
    except ValueError:
        return value


def filter_by_values(data_list, field_name, *args):
    filtered_list = []
    for data in data_list:
        if data[field_name] in args:
            filtered_list.append(data)
    return filtered_list


def num_to_col_letters(num):
    letters = ''
    while num:
        mod = (num - 1) % 26
        letters += chr(mod + 65)
        num = (num - 1) // 26
    return ''.join(reversed(letters))


def convert_to_date(data_dict=list, date_format=str, date_format_out=str, *args):
    updated_data_dict = []
    for data in data_dict:
        temp_data = {}
        for field in data.keys():
            if field in args:
                temp_data[field] = datetime.datetime.strptime(data[field], date_format).strftime(date_format_out)
            else:
                temp_data[field] = data[field]
        updated_data_dict.append(temp_data)
    return updated_data_dict


def remove_from_dict(values_dict=dict, *args):
    updated_dict = []
    for value in values_dict:
        for arg in args:
            value.pop(arg.upper())
        updated_dict.append(value)
    return updated_dict


def add_months_to_date(date=datetime.datetime, num_of_months=int):
    for i in range(num_of_months):
        date = date + datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1])
    return date


def find_duplicates(ocurrences_list=list) -> list:
    duplicates = []
    seen = []
    for item in ocurrences_list:
        if item in seen:
            duplicates.append(item)
        else:
            seen.append(item)
    return duplicates