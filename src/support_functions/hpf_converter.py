import file_handler, logging, json_config
import logger as log
from dataclasses import dataclass


logger = logging.getLogger('hpf_converter')


'''
==================================================================================================================================

        Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     Classes     

==================================================================================================================================
'''

@dataclass
class Configuration:
    source : str
    destin : str
    extension : str
    file_header: str
    properties : list

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
    def check_type_insertion(cls, setting_dict=dict):
        try:
            source = setting_dict['source']
            destin = setting_dict['destin']
            extension = setting_dict['extension']
            file_header = setting_dict['file_header']
            properties = setting_dict['properties']
            return cls(source, destin, extension, file_header, properties)
        except Exception as error:
            raise error


'''
==================================================================================================================================

        Template             Template        Template        Template        Template        Template        Template        

==================================================================================================================================
'''

template = '''{
    "source" : "",
    "destin" : "",
    "extension" : "",
    "file_header" : "#File converted by HPF Converter",
    "properties" : {
        "ID" : "",
        "NAME" : "",
        "DOTSIZE" : 150, 
        "CAPHEIGHT" : "",
        "CHARWIDTH" : "",
        "CELLWIDTH" : "",
        "LINEFEED" : "",
        "HEIGHT_CM" : ""
    }
}
'''

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''

def hpf_reader(file_contents: str) -> dict:
    '''
    Read hpf file contents and return a dictionary with its values
    '''
    hpf_values = {}
    temp_list = []
    value_header = ''
    for line in file_contents:
        line = line.replace('\n', '')
        if len(line) > 0:
            if '[' == line[0] and ']' == line[len(line) - 1]:
                if value_header:
                    logger.debug(value_header)
                    hpf_values[value_header] = temp_list
                    value_header = ''
                    temp_list= []
                value_header = line.replace('[', '').replace(']', '')

            elif '#' in line:
                hpf_values['HEADER'] = line
            elif '=' in line:
                tag_and_value = line.split('=')
                if ',' in tag_and_value[1]:
                    value = tag_and_value[1].replace(';', '').split[',']
                else:
                    value = tag_and_value[1]
                temp_list.append({tag_and_value[0] : value})
                logger.debug(f'{tag_and_value[0]} : {value}')
            elif 'P' == line[0]:
                tag = line[0:2]
                value = line[2:len(line) - 1].replace(';', '').split(',')
                temp_list.append({tag : value})
            else:
                temp_list.append(line)
    if value_header:
        hpf_values[value_header] = temp_list
    return hpf_values
        

def hpf_builder(name: str, id: int, hpf_contents: dict, config: Configuration) -> bool:
    hpf_data = ''
    for key, value in hpf_contents.items():
        logger.debug(key)
        if key == 'HEADER':
            hpf_data = f'{config.file_header}\n\n'
        elif key == 'Properties':
            hpf_data += f'[{key}]\n'
            for list_value in value:
                list_key = list(list_value.keys())[0]
                list_value_v = list(list_value.values())[0]
                logger.debug(f'{list_key} {list_value_v}')
                if list_key == 'ID':
                    hpf_data += f'ID={id}\n'
                elif list_key == 'NAME':
                    hpf_data += f'NAME={name}\n'
                else:
                    if config.properties[list_key]:
                        hpf_data += f'{list_key}={config.properties[list_key]}\n'
                    else:
                        hpf_data += f'{list_key}={list_value_v}\n'
            hpf_data += '\n'
        elif 'Char' in key:
            last_key = ''
            for list_value in value:
                list_key = list(list_value.keys())[0]
                list_value_v = list(list_value.values())[0]
                if last_key == 'PD' and list_key == 'PD':
                    hpf_data += ','.join(list_value_v)
                else:
                    hpf_data += f'{list_key}{",".join(list_value_v)}'
                last_key = list_key

    pass
    





'''
==================================================================================================================================

        Main        Main        Main        Main        Main        Main        Main        Main        Main        Main        

==================================================================================================================================
'''

if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)
    

    try:
        config_data = json_config.load_json_config('./config_hpf_converter.json', template)
        config = Configuration.check_type_insertion(config_data)
    except:
        logger.critical('Could not load config file')
        exit()    
    
    logger.info('Load config')

    try:
        file_list = file_handler.fileListFullPath(config.source, config.extension)
        if len(file_list) > 0:
            for file in file_list:
                file_contents = file_handler.file_reader(file)
                hpf_values = hpf_reader(file_contents)
                hpf_builder('Test', 42, hpf_values, config)
                print(hpf_values)
    except Exception as error:
        logger.error(f'Error reading files {error}')