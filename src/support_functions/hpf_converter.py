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
            return cls(source, destin, extension)
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
    "file_header" : "File converted by HPF Converter",
    "properties" : {
        "ID" : "",
        "NAME" : "",
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
    temp_dict = {}
    for line in file_contents:
        value_header = ''
        if '[]' in line.lower():
            value_header = 'properties'
        





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
