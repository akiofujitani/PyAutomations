# import numpy as np
# from matplotlib import pyplot as plt
# from math import pi
# u=0    #x-position of the center
# v=0    #y-position of the center
# a=35    #radius on the x-axis
# b=25    #radius on the y-axis

# t = np.linspace(0, 2*pi, 360)
# plt.figure(figsize=(a*0.2 , b*0.2))
# plt.plot( u+a*np.cos(t) , v+b*np.sin(t) )
# plt.grid(color='lightgray',linestyle='--')
# plt.show()

# print(t)

# for angle in t:
#     print(f'{u+a*np.cos(angle)} x {v+b*np.sin(angle)}')





# import logging, json_config, datetime

# from cv2 import log
# from logging.config import dictConfig


# logging_config_str = '''
# {
#     "version" : 1,
#     "formatters" : {
#         "brief" : {
#             "format" : "%(levelname) -8s: %(name)-15s %(message)s"
#         },
#         "precise" : {
#             "format" : "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
#         }
#     },
#     "handlers" : {
#         "console" : {
#             "class" : "logging.StreamHandler",
#             "formatter" : "brief",
#             "level" : "INFO"
#         },
#         "file" : {
#             "class" : "logging.handlers.RotatingFileHandler",
#             "formatter" : "precise",
#             "filename" : "logs/logconfig.log",
#             "maxBytes" : 1024
#         }
#     },
#     "root" : {
#         "handlers" : ["console", "file"],
#         "level" : "DEBUG"
#     }
# }
# '''


# def convert_to_date(data_dict=list, date_format=str, date_format_out=str, *args):
#     updated_data_dict = []
#     for data in data_dict:
#         temp_data = {}
#         for field in data.keys():
#             if field in args:
#                 temp_data[field] = datetime.datetime.strptime(data[field], date_format).strftime(date_format_out)
#             else:
#                 temp_data[field] = data[field]
#         updated_data_dict.append(temp_data)
#     return updated_data_dict

# import os, sys
# from time import sleep

# capture = ImageGrab.grab(bbox=(200, 300, 1000, 800))

# ImageShow.show(capture, 'Test')

# print('Starting script')
# sleep(1.0)
# print("argv was",sys.argv)
# print("sys.executable was", sys.executable)
# print("restart now")
# python = sys.executable
# os.execl(python, python, sys.argv[0])
# import data_communication

# sheets_id = '1woQuWByZHNX8H74b9w62fQlV3F91G3iqihlNA7Ldfw4'
# sheets_pos = 'A:Z'
# sheets_name = 'WHITE_LABEL_CREATION_LIST'


# test_value = 'test input'
# data_communication.data_update_values(sheets_name, 'F5', [[test_value]], sheets_id)

def convert_number_to_letter(column_int):
    start_index = 1   #  it can start either at 0 or at 1
    letter = ''
    while column_int > 25 + start_index:   
        letter += chr(65 + int((column_int-start_index)/26) - 1)
        column_int = column_int - (int((column_int-start_index)/26))*26
    letter += chr(65 - start_index + (int(column_int)))
    return letter


if __name__ == '__main__':
    number = 150
    letter = convert_number_to_letter(number)
    print(letter)

