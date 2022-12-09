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

import tkinter
import tkinter.ttk


    

if __name__ == '__main__':
    # Create window
    window = tkinter.Tk()

    window.title('Test fuck the name')
    window.geometry('500x200')

    #Create label with text

    label = tkinter.Label(window, text='Please enter your name and click in the Button OK', font=('Arial', 10))
    label.grid(column=0, row=0)

    # Create text input field

    text = tkinter.Entry(window, width=30)
    text.grid(column=0, row=1)
    text.focus()

    label_2 = tkinter.Label(window, font=('Arial Bold', 20))
    label_2.grid(column=0, row=3)

    # Create text input field disabled

    text_2 = tkinter.Entry(window,width=30, state='disabled')
    text_2.grid(column=0, row=4)

    # Button click action

    def click_button_ok():
        text_value = f'Fuck you {text.get()}'
        label_2.configure(text=text_value)


    def combo_box_get():
        text_value = f'Value from combobox {combo_box.get()}'
        print(text_value)
        text_2.configure(state='normal')
        text_2.delete(0, tkinter.END)
        text_2.insert(0, text_value)
        text_2.configure(state='disabled')


    # Create button

    Button = tkinter.Button(window, text='Ok', command=click_button_ok, width=5)
    Button.grid(column=1, row=1)

    Button_2 = tkinter.Button(window, text='Second Button', command=combo_box_get, bg='red', fg='white')
    Button_2.grid(column=1, row=2)

    # Create combobox

    combo_box = tkinter.ttk.Combobox(window, width=10)
    combo_box['values'] = (1, 2, 3, 4, 5, 'Text')
    combo_box.current(5)
    combo_box.grid(column=1, row=3)

    # Check button

    check_button_state = tkinter.BooleanVar()
    check_button_state.set(False)
    check_button = tkinter.ttk.Checkbutton(window, text='Choose', variable=check_button_state)

    check_button.grid(column=1, row=4)


    # Radio Button

    radio_button_1 = tkinter.ttk.Radiobutton(window, text=f'Radio 1', value=0)
    radio_button_2 = tkinter.ttk.Radiobutton(window, text=f'Radio 2', value=0)
    radio_button_3 = tkinter.ttk.Radiobutton(window, text=f'Radio 3', value=0)
    radio_button_4 = tkinter.ttk.Radiobutton(window, text=f'Radio 4', value=0)


    # Run GUI

    window.mainloop()
        