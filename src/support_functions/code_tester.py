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
# import time
# import threading
# import logging
# try:
#     import tkinter as tk # Python 3.x
#     import tkinter.scrolledtext as ScrolledText
# except ImportError:
#     import Tkinter as tk # Python 2.x
#     import ScrolledText

# class TextHandler(logging.Handler):
#     # This class allows you to log to a Tkinter Text or ScrolledText widget
#     # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

#     def __init__(self, text):
#         # run the regular Handler __init__
#         logging.Handler.__init__(self)
#         # Store a reference to the Text it will log to
#         self.text = text

#     def emit(self, record):
#         msg = self.format(record)
#         def append():
#             self.text.configure(state='normal')
#             self.text.insert(tk.END, msg + '\n')
#             self.text.configure(state='disabled')
#             # Autoscroll to the bottom
#             self.text.yview(tk.END)
#         # This is necessary because we can't modify the Text from other threads
#         self.text.after(0, append)

# class myGUI(tk.Frame):

#     # This class defines the graphical user interface 

#     def __init__(self, parent, *args, **kwargs):
#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         self.root = parent
#         self.build_gui()

#     def build_gui(self):                    
#         # Build GUI
#         self.root.title('TEST')
#         self.root.option_add('*tearOff', 'FALSE')
#         self.grid(column=0, row=0, sticky='ew')
#         self.grid_columnconfigure(0, weight=1, uniform='a')
#         self.grid_columnconfigure(1, weight=1, uniform='a')
#         self.grid_columnconfigure(2, weight=1, uniform='a')
#         self.grid_columnconfigure(3, weight=1, uniform='a')

#         # Add text widget to display logging info
#         st = ScrolledText.ScrolledText(self, state='disabled')
#         st.configure(font='TkFixedFont')
#         st.grid(column=0, row=1, sticky='w', columnspan=4)

#         # Create textLogger
#         text_handler = TextHandler(st)

#         # Logging configuration
#         logging.basicConfig(filename='test.log',
#             level=logging.INFO, 
#             format='%(asctime)s - %(levelname)s - %(message)s')        

#         # Add the handler to logger
#         logger = logging.getLogger()        
#         logger.addHandler(text_handler)

# def worker():
#     # Skeleton worker function, runs in separate thread (see below)   
#     while True:
#         # Report time / date at 2-second intervals
#         time.sleep(2)
#         timeStr = time.asctime()
#         msg = 'Current time: ' + timeStr
#         logging.info(msg) 

# def main():

#     root = tk.Tk()
#     myGUI(root)

#     t1 = threading.Thread(target=worker, args=[])
#     t1.start()

#     root.mainloop()
#     t1.join()

# main()
