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

# from time import sleep
# import win_handler, win32gui

# foreground_win = win_handler.activate_window('Volpe')
# print(foreground_win._hWnd)
# active_window = win32gui.GetForegroundWindow()
# print(active_window)
# active_win_text = win32gui.GetWindowText(active_window)

# print(f'Window title: {active_win_text}')
# print()

# import time

# import win32gui, pyautogui

# while True:
#     window = win32gui.GetForegroundWindow()
#     class_name = win32gui.GetClassName(window)
#     menu = win32gui.GetMenu(window)
#     rect = win32gui.GetWindowRect(window)
#     title = win32gui.GetWindowText(window)
#     pyauto = pyautogui.getWindowsWithTitle(title)
#     control = win32gui.FindWindowEx(window, None, None, None)
#     if control:
#         control_text = win32gui.GetWindowText(control)
#         control_class = win32gui.GetClassName(control)
#     print(f'{title}: {class_name} text {control_text} class {control_class}')
#     time.sleep(1)

'''
Emergency stop
'''

# import keyboard, threading, logging
# from time import sleep
# import logger as log

# logger = logging.getLogger('code_tester')


# def quit_func():
#     logger.info('Quit pressed')
#     event.set()
#     return
    

# def while_test(event):
#     counter = 0
#     while True:
#         try:
#             logger.info(f'While counter in {counter}')
#             counter += 1
#             sleep(1)
#             if event.is_set():
#                 logger.info('Event set')
#                 raise Exception('Event is set')
#         except Exception as error:
#             logger.info(f'Event set {error}')
#             event.clear()
#             return


# if __name__ == '__main__':
#     logger = logging.getLogger()
#     log.logger_setup(logger)

#     keyboard.add_hotkey('space', quit_func)
#     event = threading.Event()

#     thread = threading.Thread(target=while_test, args=(event, ), name='Test')
#     thread.start()
#     thread.join()


# List

test_int = str(5.00)
test_dict = {'R' : '', 'L' : ''}
print(len(test_dict))
print(len(test_int))