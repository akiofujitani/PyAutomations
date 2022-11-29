from time import sleep
import file_handler, datetime, calendar, data_organizer, os, json_config
from vca_handler import VCAtoDict
from ntpath import join


def read_vca(path, extension, start_date, end_date):
    file_list = file_handler.listFilesInDirSubDir(path, extension)
    date_filtered_list = file_handler.listByDate(file_list, start_date, end_date)
    values_dict = {}
    for file in date_filtered_list:
        try:
            with open(file, 'r', errors='replace') as contents:
                fileContents = contents.readlines()
                temp_vca_contents = VCAtoDict(fileContents)
                values_dict[temp_vca_contents['JOB']] = temp_vca_contents
        except Exception as error:
            print(error)
    return values_dict


def week_date(date_value, days_to_subtract):
    
    new_date = date_value - datetime.timedelta(days=days_to_subtract)
    while calendar.weekday(new_date.year, new_date.month, new_date.day) >= 5:
        new_date = new_date - datetime.timedelta(days=1)
    return new_date


def values_merger(path_list=list, base_list=list, base_search_tag=str, *args, start_pos=0, end_pos=12):
    file_list = []
    for path in path_list:
        file_list = file_list + file_handler.listFilesInDirSubDir(path, 'vca')
    merged_list = []
    for value in base_list:
        merged_values = value
        file_found = file_handler.file_finder(file_list, value[base_search_tag.upper()], start_pos=start_pos, end_pos=end_pos)
        filtered_tags_value = {}
        filtered_tags_value[base_search_tag.upper()] = value[base_search_tag.upper()]
        if file_found:
            vca_converted = VCAtoDict(file_handler.file_reader(file_found))
            filtered_tags_value.update(data_organizer.filter_tag(vca_converted, *args))
            merged_values[base_search_tag.upper()] = data_organizer.tags_dict_to_plain_dict(filtered_tags_value)
        else:
            merged_values[base_search_tag.upper()] = filtered_tags_value
        merged_list.append(merged_values)
    return merged_list



if __name__ == '__main__':
    # date_target = week_date(datetime.datetime.now().date(), 1)
    while True:
        try:
            print('Filter start date (dd/mm/yyyy): ')
            start_date_string = input()
            date_start = datetime.datetime.strptime(start_date_string, '%d/%m/%Y').date()
            if date_start > datetime.datetime.now().date():
                print('Date cannot be in the future')
                raise ValueError
        except ValueError:
            print('Invalid or incorrect date. Please, enter again.')
        try:
            print('Filter end date (dd/mm/yyyy):')
            end_date_string = input()    
            date_end = datetime.datetime.strptime(end_date_string, '%d/%m/%Y').date()
            if date_end > datetime.datetime.now().date() or date_end < date_start:
                print('Date value not valid')
                raise ValueError
            break
        except ValueError:
            print('Invalid or incorrect date. Please, enter again.')
    
    print()
    extension = 'vca'
    # file_path = []
    # while True:
    #     print('Insert path press and "Enter" to store')
    #     path_temp = input()
    #     if os.path.exists(path_temp):
    #         file_path.append(path_temp)
    #         path_temp = ''
    #         print(file_path)
    #     if keyboard.is_pressed('enter') and len(file_path) > 0:
    #         break

    file_path = [r'C:\LMS\HOST_EXPORT\VCA\read_app',r'Z:\Backup LMS\LMS Export\Backup\2022']
    # path_vca_backup = r'Z:\Backup LMS\LMS Export\Backup'

    export_data = {}
    for path in file_path:
        export_data.update(read_vca(path, extension, date_start, date_end))
    # export_data = read_vca(path_vca, extension, date_start, date_end)
    # export_data.update(read_vca(path_vca_backup, extension, date_start, date_end))

    # tags_list = ['JOB', 'CLIENT', 'LNAM', 'LDNAM', 'SPH', 'CYL', 'AX', 'ADD', 'LIND', 'INSPRPRVA','INSPRPRVM' ,'_CUSTOMER', 'ERDRIN', 'ERDRUP', 'ERNRIN', 'ERNRUP', 'ERSGIN', 'ERSGUP', 'CORRLEN', 'LTYP', 'LTYPEB', 'LTYPEF']
    tags_list = ['JOB', '_ENTRYDATE', 'CLIENT', 'LNAM', 'LDNAM', 'SPH', 'CYL', 'AX', 'ADD', 'CLIENT', 'LIND', 'INSPRPRVA', 'INSPRPRVM', '_CUSTOMER', 'CTHNA', 'CTHNP', '_XCALC' , 'MBASE', 'GBASE', 'GCROS', 'FRNT']

    filtered_data = []
    for job in export_data:
        tag_filtered = data_organizer.filter_tag(export_data[job], 'JOB', *tags_list)
        tag_filtered['JOB'] = job
        filtered_data.append(tag_filtered)

    plain_dict = data_organizer.dict_list_to_plain_dict(filtered_data)
    filled_plain_dict = data_organizer.plain_dict_list_filler(plain_dict)
    float_updated_dict = data_organizer.plain_dict_float_format(filled_plain_dict)

    date_from_to_str = f'{date_start.strftime("%Y%m%d")}_{date_end.strftime("%Y%m%d")}'
    filtered_name = f'Filtered_list_{date_from_to_str}'
    file_handler.listToCSV(float_updated_dict, join(r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\JobFilterPy', f'{filtered_name}.csv'))

    # advance_filtered = data_organizer.filter_tag_by_values(filtered_data, [{'Tag' : 'SPH', 'Operator' : '>=', 'Value' : 10},
    #                                     {'Tag' : 'SPH', 'Operator' : '<=', 'Value' : -12}, 
    #                                     {'Tag' : 'INSPRPRVM', 'Operator' : '>=', 'Value' : 6}, 
    #                                     {'Tag' : 'CYL', 'Operator' : '<=', 'Value' : -6}, 
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : 'SingleVision2NC_LP'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : 'DigitalBifocalRS28R'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : 'AlphaH65_LP'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : '3117'},
    #                                     {'Tag': 'LDNAM', 'Operator' : '=', 'Value' : '01/08/'},
    #                                     {'Tag': 'LNAM', 'Operator' : '=', 'Value' : '4166'},
    #                                     {'Tag': 'LNAM', 'Operator' : '=', 'Value' : '4144'},
    #                                     {'Tag': 'LNAM', 'Operator' : '=', 'Value' : '4180'},
    #                                     {'Tag': '_CUSTOMER', 'Operator' : 'contains', 'Value' : 'POLY'},
    #                                     {'Tag': '_CUSTOMER', 'Operator' : 'contains', 'Value' : 'ITA Ot'},
    #                                     {'Tag': '_CUSTOMER', 'Operator' : 'contains', 'Value' : 'NATAL LENT'}])

    # plain_dict = data_organizer.dict_list_to_plain_dict(advance_filtered)
    # filled_plain_dict = data_organizer.plain_dict_list_filler(plain_dict)
    # float_updated_dict = data_organizer.plain_dict_float_format(filled_plain_dict)

    # advance_name = f'Advance_filter_{date_from_to_str}'
    # file_handler.listToCSV(float_updated_dict, join(r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\JobFilterPy', f'{advance_name}.csv'))

