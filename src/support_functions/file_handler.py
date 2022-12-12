import csv, os, shutil, datetime, time, chardet
from ntpath import join


def file_list(path=str, file_extention=str) -> list:
    '''
    List files ended with choosen extension inside one directory
    '''
    if not os.path.exists(path):
        os.mkdir(path)
        print(f'Directory {path} created')
    return [file for file in os.listdir(path) if file.lower().endswith(f'.{file_extention.lower()}')]


def listFilesInDirSubDir(pathRoot=str, extention=str) -> list:
    '''
    List files ended with choosen extension inside all directories inside the path
    '''
    fileList = []
    for root, dir, files in os.walk(pathRoot):
        for file in files:
            if file.lower().endswith(f'{extention}'):
                fileList.append(os.path.join(root, file))
    print(f'Listing for {pathRoot} done')
    return fileList


def fileListFullPath(path, file_extention) -> list:
    '''
    List files returning the full path list ended with choosen extension inside one directory
    '''    
    if not os.path.exists(path):
        os.mkdir(path)
        print(f'Directory {path} created')    
    return [os.path.join(path, file) for file in os.listdir(path) if file.lower().endswith(f'.{file_extention.lower()}')]


def __csv_reader(file_path, case_upper, delimeter_char, encoding='utf-8'):
    '''
    Auxiliary method for CSVtoList
    '''
    with open(file_path, encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimeter_char, quoting=csv.QUOTE_NONE)
        header = []
        header = next(csv_reader)

        csv_contents = []
        for row in csv_reader:
            row_Contents = {}
            for key in range(len(header)):
                if case_upper:
                    header_value = header[key].upper()
                else:
                    header_value = header[key]
                row_Contents[header_value] = row[key]        
            csv_contents.append(row_Contents)
    return csv_contents


def CSVtoList(filePath, case_upper=True, delimeter_char='\t') -> list:
    '''
    Get csv file, ready and convert it to list
    '''
    file_path = os.path.normpath(filePath)
    try:
        csv_contents = __csv_reader(file_path, case_upper, delimeter_char)
    except Exception as error:
        print(error)
        try:
            try:
                csv_contents = __csv_reader(filePath, case_upper, delimeter_char, encoding='cp1252')
            except:
                encoding = __detect_encode(filePath)
                csv_contents = __csv_reader(filePath, case_upper, delimeter_char, encoding=encoding)
        except:
            raise Exception('Could not read file contents')        
    return csv_contents


def __detect_encode(file_path):
    '''
    Auxiliary method for CSVoList
    Try to detect the encoding type
    '''
    with open(file_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))
    return result['encoding']


def listToCSV(valuesList, filePath):
    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=list(valuesList[0].keys()), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(valuesList)
    return


def file_finder(file_list, file_name, start_pos=0, end_pos=None):
    print(f'Searching for file {file_name}')
    for file in file_list:
        base_name = os.path.basename(file)
        cropped_name = base_name[start_pos:end_pos]
        if file_name in cropped_name:
            print(f'{file_name} found')
            return file
    return False


def file_reader(file_path):
    try:
        with open(file_path, encoding='utf-8') as file:
            return file.readlines()
    except Exception as error:
        print(f'Error opening file {error}')
        with open(file_path, encoding='cp1252') as file:
            return file.readlines()


def file_writer(file_path, string_values):
    with open(file_path, 'w') as writer:
        writer.write(string_values)
        return


def file_move_copy(path_from, path_to, file_name, copy=bool):
    try:
        move_copy = 'copied' if copy == True else 'moved'
        print(f'From {path_from} \nto {path_to} \nfile {file_name} {move_copy}')
        check_create_dir(path_to)
        new_file_name = file_name_check(path_to, file_name)
        if copy == True:
            return shutil.copy(join(path_from, file_name), join(path_to, new_file_name))
        else:
            return shutil.move(join(path_from, file_name), join(path_to, new_file_name))
    except Exception as error:
        print('Could not execute {error}')
        raise error


def copy_number_definer(file_name=str):
    count = 0
    file_name_ext_split = file_name.split('.')
    pure_file_name = file_name_ext_split[0].replace(')', '').split('_(Copy_')
    count = int(pure_file_name[1]) + 1
    return f'{pure_file_name[0]}_(Copy_{count}).{file_name_ext_split[1]}' if len(file_name_ext_split) == 2 else f'{pure_file_name}_(Copy_{count})'


def file_name_check(path, file_name):
    while os.path.exists(join(path, file_name)):
        name_splitted = file_name.split('.')
        if '_(Copy_' in name_splitted[0]:
            file_name = copy_number_definer(file_name)
        else:
            file_name = f'{name_splitted[0]}_(Copy_1).{name_splitted[1]}' if len(name_splitted) == 2 else f'{name_splitted[0]}_(Copy_1)'
    return file_name


def fileNameDefiner(path, file_name, extention):
    while os.path.exists(join(path, f'{file_name}.{extention}')):
        name_splitted = file_name.split('_')
        if len(name_splitted) == 1:
            file_name += '_1'
        else:
            number = int(name_splitted[-1]) + 1
            rebuilt_name = ''
            for part in range(len(name_splitted) - 1):
                rebuilt_name = rebuilt_name + '_' + name_splitted[part]
            rebuilt_name = rebuilt_name.replace('_' , '', 1)
            file_name = f'{rebuilt_name}_{number}'
    print(f'File name {file_name}')
    return file_name


def fileMoveRename(source, destin, source_name, destin_name):
    destin_name_no_extention = destin_name.split('.')[0]
    extention = destin_name.split('.')[1]
    try:
        file_name_checked = fileNameDefiner(destin, destin_name_no_extention, extention)
        shutil.move(join(source, f'{source_name}'), join(destin, f'{file_name_checked}.{extention}'))
        print(f'{source_name} renamed to {destin_name}')
        print(f'Moved from "{source}" to "{destin}"')
        return
    except FileNotFoundError as file_error:
        print(file_error)
    return


def creatDir(path, dir_name=None):
    full_path = path
    if not dir_name == None:
        full_path = join(path, dir_name)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
        print(f'Directory "{dir_name}" created.')
    return


def check_create_dir(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
            print(f'Directory "{path}" created.')
        return path
    except Exception as error:
        print(f'Could not check/create {path}')
        raise Exception('Check/create directory error.')


def file_list_last_date(path=str, extension=str, pattern_removal=str, date_pattern=str):
    '''
    Retrieves the last defined data in file list.
    This don't retrieves the creattion date, its the date defined in the file name
    '''
    try:
        files_list = file_list(path, extension)
        date_list = []
        for file in files_list:
            file_extension = file.split('.')
            date_list.append(datetime.datetime.strptime(file_extension[0].replace(pattern_removal, ''), date_pattern))
            date_list.sort(reverse=True)
        return date_list[0]
    except Exception as error:
        print(f'File not found or path incorrect')
        return None


def file_contents_last_date(file_contents=dict, field_name=str, time_format='%d/%m/%Y'):
    try:
        last_date = sorted(file_contents, key=lambda value : datetime.datetime.strptime(value[field_name], time_format), reverse=True)[0][field_name]
        strip_date = datetime.datetime.strptime(last_date, time_format).date()
        return datetime.datetime.strptime(strip_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
    except Exception as error:
        print('Could not get date from file')
        raise error


def file_contents_last_date1(path=str, extension=str, field_name=str):
    try:
        files_list = file_list(path, extension)
        last_date = ''
        for file in files_list:
            file_contents = CSVtoList(join(path, file))
            temp_date =  datetime.datetime.strptime(sorted(file_contents, key=lambda value : value[field_name], reverse=True)[0][field_name], '%d/%m/%Y')
            if last_date == '':
                last_date = temp_date
            if temp_date > last_date:
                last_date = temp_date
        return last_date
    except Exception as error:
        print('Could not get date from files')
        raise error


def listByDate(filesList, dateStart, dateEnd):
    listByDate = []
    for file in filesList:
        fileDate = fileCreationDate(file)
        if fileDate >= dateStart and fileDate <= dateEnd if dateEnd else dateStart:
            listByDate.append(file)
    print(f'Listing by date {dateStart} / {dateEnd} done')
    return listByDate


def fileCreationDate(file):
    strSplit = time.ctime(os.path.getmtime(file)).split(' ')
    for item in strSplit:
        if len(item) == 0:
            strSplit.remove(item)
    return datetime.datetime.strptime(f'{strSplit[4]}/{strSplit[1]}/{strSplit[2]}', '%Y/%b/%d').date()