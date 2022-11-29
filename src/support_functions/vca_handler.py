import os

def VCAtoObject(VCAFileContent):
    dataValue = {}
    counter = 0
    for line in VCAFileContent:
        line = line.replace('\n', '')
        if len(line) > 0:
            tagAndValue = line.split('=')
            if ';' in tagAndValue[1]:
                valueSplit = tagAndValue[1].split(';')
            if counter:
                radiusList = radiusList + valueSplit
                counter += 1
            if counter == 37:
                if 'TRCFMT' in dataValue.keys():
                    dataValue['TRCFMT'].update({tempObj.side : JobClasses.frameShape(radiusList, (f'TRCFMT_{tempObj.side}'), tempObj.initAngle, tempObj.endAngle, tempObj.char1, tempObj.side, tempObj.char2)})
                else:
                    dataValue['TRCFMT'] = {tempObj.side : JobClasses.frameShape(radiusList, (f'TRCFMT_{tempObj.side}'), tempObj.initAngle, tempObj.endAngle, tempObj.char1, tempObj.side, tempObj.char2)}
                counter = 0
                tempObj = ''
                radiusList = ''
            if 'TRCFMT' in tagAndValue[0]:            
                tempObj = JobClasses.trcFormat(valueSplit[0], valueSplit[1], valueSplit[2], valueSplit[3], valueSplit[4])
                counter = 1
                radiusList = []
            elif ';' in tagAndValue[1] and tagAndValue[1].count(';') == 1:
                if tagAndValue[0] in dataValue.keys():
                    if not isinstance(dataValue[tagAndValue[0]], dict):
                        tempValue = dataValue[tagAndValue[0]]
                        dataValue[tagAndValue[0]] = {1 : tempValue}
                    else:
                        num = len(dataValue[tagAndValue[0]]) + 1
                    dataValue[tagAndValue[0]].update({2 : JobClasses.tagRL(tagAndValue[0], valueSplit[0], valueSplit[1])})
                else:    
                    dataValue[tagAndValue[0]] = JobClasses.tagRL(tagAndValue[0], valueSplit[0], valueSplit[1])
            elif tagAndValue[1].count(';') == 0:
                dataValue[tagAndValue[0]] = JobClasses.tagSingle(tagAndValue[0], tagAndValue[1])
    print(dataValue)
    return dataValue


def VCAtoDict(VCAFileCOntent):
    try:
        tempList = []
        dataValue = {}
        counter = 0
        valueSplit = ''
        for line in VCAFileCOntent:
            line = line.replace('\n', '').replace('\t', '')
            if len(line) > 0:
                tagAndValue = line.split('=')
                if ';' in tagAndValue[1]:
                    valueSplit = tagAndValue[1].split(';')
                if counter:
                    radiusList = radiusList + valueSplit
                    counter += 1
                if counter == 37:
                    counter = 0
                    if 'TRCFMT' in dataValue.keys():
                        dataValue['TRCFMT'].update({tempList[3]: tempList})
                        dataValue['R'].update({tempList[3]: radiusList})
                    else:
                        dataValue['TRCFMT'] = {tempList[3] : tempList}
                        dataValue['R'] = {tempList[3] : radiusList}
                if 'TRCFMT' in tagAndValue[0]:
                    tempList = valueSplit
                    counter += 1
                    radiusList = []
                elif ';' in tagAndValue[1] and tagAndValue[1].count(';') == 1:
                    if tagAndValue[0] in dataValue.keys():
                        tempValue = dataValue[tagAndValue[0]]
                        if 'R' in dataValue[tagAndValue[0]].keys():
                            num = 1
                        else:
                            num = len(dataValue[tagAndValue[0]])
                        dataValue[tagAndValue[0]] = {num : tempValue}
                        dataValue[tagAndValue[0]].update({(num + 1) : {'R' : valueSplit[0], 'L' : valueSplit[1]}})
                    else:
                        dataValue[tagAndValue[0]] = {'R' : valueSplit[0], 'L' : valueSplit[1]}
                elif tagAndValue[1].count(';') == 0:
                    if tagAndValue[0] in dataValue.keys():
                        tempValue = dataValue[tagAndValue[0]]
                        dataValue[tagAndValue[0]] = {1 : tempValue}
                        dataValue[tagAndValue[0]].update({2 : tagAndValue[1]})
                    else:
                        dataValue[tagAndValue[0]] = tagAndValue[1]
        print(f'Terminated tag convertion of {dataValue["JOB"]}')
        return dataValue
    except Exception as error:
        print(f'Could not read VCA contents {error}')
        raise Exception('VCA reading error')


# check and deativate > file_handler.listFilesInDirSubDir is simpler and works almost the same way getting the same input
def listVCAInDirSubDir(pathRoot, extention):
    fileList = []
    for root, dir, files in os.walk(pathRoot):
        file_dict = {}
        for file in files:
            if file.lower().endswith(f'{extention}'):
                file_dict['root'] = root
                file_dict['file_name'] = file
                fileList.append(file_dict)
        print(root)
    print(f'Listing for {pathRoot} done')
    return fileList


# check and deativate > file_handler.file_finder is simpler and works almost the same way getting the same input
def find_files(path_root_list, name, extention, start_pos, end_pos=None):
    for path_root in path_root_list:
        for root, dir, files in os.walk(path_root):
            file_dict = {}
            for file in files:
                if file.lower().endswith(f'{extention}') and name in file[start_pos:end_pos]:
                    file_dict['root'] = root
                    file_dict['file_name'] = file
                    return file_dict
    return False


def fileList(path, file_extention):
    return [{'file_name' : file, 'root' : path} for file in os.listdir(path) if file.lower().endswith(f'.{file_extention}')]