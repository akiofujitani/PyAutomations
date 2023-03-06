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

from time import sleep
import win_handler, win32gui

foreground_win_hWnd = win32gui.GetForegroundWindow()
active_win_text = win32gui.GetWindowText(foreground_win_hWnd)
active_win_control = win32gui.FindWindowEx(foreground_win_hWnd, 0, 'static', None)
control_text = win32gui.GetWindowText(active_win_control)

print(f'Window title: {active_win_text}')
print(active_win_control)
print()