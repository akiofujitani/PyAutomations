import json, os


sheets_cred = '''
{
    "sheets_id" : "1aqLuNRknJc6ewS7Cehq-8j1kbCPnEftuTrsUelGhpTQ",
    "SCOPE" : ["https://www.googleapis.com/auth/spreadsheets"]
}
'''


def load_json_config(config_file=str, template_data=None):
    '''
    load json file and transforms it in dictionary
    the template_data  
    '''
    if os.path.exists(config_file):
        with open(config_file, encoding='utf-8') as file_data:
            return json.load(file_data)
    elif template_data:
        template_data = json.loads(template_data)
        with open(config_file, 'w') as json_file:
            json.dump(template_data, json_file, indent=4)
            return template_data
    else:
        print('File not found and no template data inserted')
        raise Exception('File not found and no template data inserted')


def save_json_config(config_file=str, json_config=dict):
    with open(config_file) as json_file:
        json.dump(json_config, json_file, indent=4)
    return


def return_template_ccl():
    json_template = {
    "templates" : {
        "Info" : {
                "FileType" : "CCL100 Marking Layout File", 
                "Version" : "1.0"
            }
        ,
        "Count" : {
                "Number" : 9
            }
        ,
        "FileParams" : {
            "rotation" : 0.00000, 
            "xoffset" : 0.00000, 
            "yoffset" : 0.00000, 
            "mirrored" : 0, 
            "flipped" : 0
            }
        ,
        "CircleL" : {
            "char" : 0, 
            "enabled" : 0, 
            "font" : 20, 
            "pen" : 1, 
            "height" : 1.500000, 
            "width" : 1.500000, 
            "x" : 17.00000, 
            "y" : 0.00000, 
            "rotation" : 0.00000, 
            "orientation" : 5, 
            "mirroring" : 1, 
            "flipping" : 0, 
            "decimalsign" : 1, 
            "digits" : 2, 
            "type" : 6, 
            "name" : "CircleL"
            }
        ,
        "CircleR" : {
            "char" : 0,
            "enabled" : 0, 
            "font" : 20, 
            "pen" : 1, 
            "height" : 1.500000, 
            "width" : 1.500000, 
            "x" : 17.00000, 
            "y" : 0.00000, 
            "rotation" : 0.00000, 
            "orientation" : 5,
            "mirroring" : 1,  
            "flipping" : 0, 
            "decimalsign" : 1, 
            "digits" : 2, 
            "type" : 6, 
            "name" : "CircleR"
            }
        ,
        "Logo" : {
            "char" : 0, 
            "enabled" : 0, 
            "font" : 32, 
            "pen" : 2, 
            "height" : 2.00000, 
            "width" : 2.500000, 
            "x" : 17.00000, 
            "y" : -6.00000, 
            "rotation" : 0.00000, 
            "orientation" : 5, 
            "mirroring" : 1, 
            "flipping" : 0, 
            "decimalsign" : 1, 
            "digits" : 2, 
            "type" : 6, 
            "name" : "Logo"
            }
        
    },
    "Text" : {
        "text" : "",
        "enabled" : 0,
        "font" : 10,
        "pen" : 3,
        "height" : 1.500000,
        "width" : 1.500000,
        "x" : 0.000000,
        "y" : 0.000000,
        "rotation" : 0.000000,
        "orientation" : 5,
        "mirroring" : 0,
        "flipping" : 0,
        "decimalsign" : 0,
        "digits" : 2,
        "type" : 6,
        "name" : ""
    }
}
    return json_template
