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
from webbrowser import open as web_open
import tkinter
import tkinter.messagebox

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('Middleware Job Visualizer')
    window.geometry('500x300')
    window.rowconfigure(0, minsize=30)
    window.columnconfigure(0, minsize=15)
    window.rowconfigure(3, minsize=50)



    text_label = tkinter.Label(window, text='Insira o número do pedido no campo abaixo e pressione o botão "OK"', font=('Arial', 10))
    text_label.grid(column=1, row=1)

    input_text = tkinter.Entry(window, justify='center', font=('Arial', 10))
    input_text.place(width=350, height=25)
    input_text.grid(column=1, row=2)
    input_text.focus()

    def click_button_ok():
        job_number = input_text.get()
        try:
            int(job_number)
            web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(job_number)}')
        except Exception as error:
            print(error)
            tkinter.messagebox.showerror('Somente números são aceitos, favor digitar novamente')

    ok_button = tkinter.Button(window, text='OK', command=click_button_ok, width=7, height=1)
    ok_button.grid(column=2, row=2)       

    window.mainloop()
    # job_number = 2677872

    # web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(job_number)}')