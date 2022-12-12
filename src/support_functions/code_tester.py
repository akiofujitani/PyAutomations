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

print('Test')