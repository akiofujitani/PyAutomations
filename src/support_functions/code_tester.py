# # SuperFastPython.com
# # example of stopping a custom thread class
# from time import sleep
# from threading import Thread
# from threading import Event
# import keyboard

# # custom thread class
# class CustomThread(Thread):
#     # constructor
#     def __init__(self, event):
#         # call the parent constructor
#         super(CustomThread, self).__init__()
#         # store the event
#         self.event = event
 
#     # execute task
#     def run(self):
#         # execute a task in a loop
#         count = 0
#         while True:
#             # block for a moment
#             count += 1
#             sleep(1)
#             # check for stop
#             if self.event.is_set():
#                 break
#             # report a message
#             print(f'Worker thread running...{count}')
#         print('Worker closing down')
 
# # create the event
# event = Event()
# # create a new thread
# thread = CustomThread(event)
# # start the new thread
# thread.start()
# # block for a while
# sleep(3)
# # stop the worker thread

# keyboard.wait('esc')
# print('Main stopping thread')
# event.set()
# thread.join()
# # wait for the new thread to finish


# =====================================================================================================================
# Creating time viewer
# =====================================================================================================================

# from time import sleep


# value = 120



# for second in range(value):
#     sleep(0.5)
#     if value % 60 == 0 and value >= 60:
#         print(value)
#     elif value % 30 == 0 and value < 60:
#         print(value)
#     elif value % 15 == 0 and value < 30:
#         print(value)
#     elif value % 1 == 0 and value < 15:
#         print(value)
#     value -= 1


# =====================================================================================================================

# import tkinter as tk
# from tkinter import ttk
# from tkinter.messagebox import showinfo

# root = tk.Tk()
# root.title('Treeview demo')
# root.geometry('620x200')

# # define columns
# columns = ('first_name', 'last_name', 'email')

# tree = ttk.Treeview(root, columns=columns, show='headings')

# # define headings
# tree.heading('first_name', text='First Name')
# tree.heading('last_name', text='Last Name')
# tree.heading('email', text='Email')

# # generate sample data
# contacts = []
# for n in range(1, 100):
#     contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

# # add data to the treeview
# for contact in contacts:
#     tree.insert('', tk.END, values=contact)


# def item_selected(event):
#     for selected_item in tree.selection():
#         item = tree.item(selected_item)
#         record = item['values']
#         # show a message
#         showinfo(title='Information', message=','.join(record))


# tree.bind('<<TreeviewSelect>>', item_selected)

# tree.grid(row=0, column=0, sticky='nsew')

# # add a scrollbar
# scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
# tree.configure(yscroll=scrollbar.set)
# scrollbar.grid(row=0, column=1, sticky='ns')

# # run the app
# root.mainloop()


# Import the required libraries
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image

# Create an instance of tkinter frame or window
win=Tk()
win.title("System Tray Application")

# Set the size of the window
win.geometry("700x350")





# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   win.destroy()

# Define a function to show the window again
def show_window(icon, item):
    win.after(150, win.deiconify)
    icon.stop()

# Hide the window and show on the system taskbar
def hide_window():
   win.withdraw()
   image=Image.open("./Icon/tiger.ico")
   menu=(item('Quit', quit_window), item('Show', show_window))
   icon=pystray.Icon("name", image, "My System Tray Icon", menu)
   icon.run()

win.protocol('WM_DELETE_WINDOW', hide_window)

win.mainloop()

