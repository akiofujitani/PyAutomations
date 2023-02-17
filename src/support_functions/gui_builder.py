import tkinter, json_config, logging, pystray
from file_mover_backup import *
from tkinter import ttk
import logger as log
from os.path import normpath
from os.path import exists
from time import sleep
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# for testing
import threading


logger = logging.getLogger('gui_builder')

class Edit_Values(tkinter.Toplevel):
    '''
    Auto create a GUI based on the values passed.
    drop_down_list values are obrigatory if combo_box is in type_list
    '''
    def __init__(self, 
                    parent=ttk.Treeview, 
                    key_list=tuple, 
                    type_list=tuple,
                    edit_title=str, 
                    values_disabled=None | list, 
                    focus_force=None | str, 
                    drop_down_list=None | dict,
                    *args, **kwargs) -> None:
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.parent = parent
        self.title(edit_title)
        self.transient()
        self.selected_item = self.parent.selection()[0]
        self.record_value = [str(value) for value in self.parent.item(self.selected_item)['values']]
        self.type_list = type_list
        self.entry_dict = {}
        self.button_dict = {}
        for key_index in range(len(key_list)):
            ttk.Label(self, text=key_list[key_index], justify='left').grid(column=0, row=key_index, padx=(5), pady=(5, 0))
            match type_list[key_index]:
                case 'str' | 'int' :
                    entry = ttk.Entry(self, width=50, justify='center')
                    entry.grid(column=1, row=key_index, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, str(self.record_value[key_index]))
                case 'path':
                    entry = ttk.Entry(self, width=50, justify='center')
                    entry.grid(column=1, row=key_index, sticky='nesw', columnspan=2, padx=(5, 0), pady=(5, 0))
                    browse_button = tkinter.Button(self, text='...', width=3)
                    browse_button.grid(column=3, row=key_index, padx=(0, 5), pady=(5, 0))
                    self.button_dict[f'{key_list[key_index]}'] = browse_button
                    self.button_dict[f'{key_list[key_index]}'].configure(command= lambda info=key_list[key_index]: self.__browse_files(info))
                    entry.insert(tkinter.END, str(self.record_value[key_index]))
                case 'boolean':
                    entry = tkinter.BooleanVar()
                    entry.set(self.record_value[key_index] if not self.record_value[key_index] == '' else False)
                    boolean_name = ('True', 'False')
                    radio_bool_button = {}
                    for i in range(len(boolean_name)):
                        radio_bool_button[i] = tkinter.ttk.Radiobutton(self, text=boolean_name[i], value=eval(boolean_name[i]), variable=entry, command=lambda variable=entry: self.__click_radio_bool(variable))
                        radio_bool_button[i].grid(column=1 + i, row=key_index)
                case 'combo_box':
                    entry = ttk.Combobox(self, width=50, justify='center')
                    entry['values'] = drop_down_list[key_list[key_index]]
                    entry.set(str(self.record_value[key_index]) if not str(self.record_value[key_index]) == '' else 'Daily')
                    entry.grid(column=1, row=key_index, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
                case _:
                    entry = ttk.Entry(self, width=50, justify='center')
                    entry.grid(column=1, row=key_index, sticky='nesw', columnspan=2, padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, str(self.record_value[key_index]))
            if not values_disabled == None:
                if key_list[key_index] in values_disabled:
                    entry.configure(state='disabled')
            self.entry_dict[key_list[key_index]] = entry
        if focus_force:
            self.entry_dict[focus_force].focus_force()
            self.entry_dict[focus_force].select_clear()
            self.entry_dict[focus_force].select_range(0, tkinter.END)
        self.bind("<Return>", self.__click_button_save)
        self.bind("<Escape>", lambda *ignore: self.destroy())

        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=1, row=key_index + 1, padx=(5), pady=(5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=2, row=key_index + 1, padx=(5), pady=(5))       


    def __click_radio_bool(self, variable):
        logger.debug(variable.get())


    def __click_button_cancel(self):
        logger.debug('Button cancel')
        if self.__compare_to_empty(''):
            self.parent.delete(self.selected_item)
        self.destroy()
    

    def __compare_to_empty(self, compare_value=str):
        for value in self.record_value:
            if not value == compare_value:
                return False
        return True


    def __click_button_save(self, event=None):
        logger.debug('Button save')

        new_record = []
        diff_found = False        
        entry_dict_keys = list(self.entry_dict.keys())
        for index in range(len(entry_dict_keys)):
            match self.type_list[index]:
                case 'str' | 'int':
                    if self.type_list[index] == 'int':
                        try:
                            value = int(self.entry_dict[entry_dict_keys[index]].get())
                        except:
                            messagebox.showerror('Save error', f'Value must be an integer')
                            self.lift()
                            self.focus_force()
                            self.entry_dict[entry_dict_keys[index]].focus_force()
                            return
                    else:
                        value = str(self.entry_dict[entry_dict_keys[index]].get())
                case 'path':
                    try:
                        if not exists(self.entry_dict[entry_dict_keys[index]].get()):
                            raise Exception('Path error')
                        value = normpath(self.entry_dict[entry_dict_keys[index]].get())
                    except:
                        messagebox.showerror('Save error', f'Invalid or inexistent path')
                        self.lift()
                        self.focus_force()
                        self.entry_dict[entry_dict_keys[index]].focus_force()
                        return
                case 'boolean':
                    value = self.entry_dict[entry_dict_keys[index]].get()
                case 'combo_box':
                    value = self.entry_dict[entry_dict_keys[index]].get()
            new_record.append(value)
            if not self.record_value[index] == value:
                diff_found = True
        if diff_found == True:
            self.parent.item(self.selected_item, values=new_record)
        logger.debug(f'Button save done')
        self.destroy()


    def __browse_files(self, button_id=str):
        logger.debug('Browser files')
        logger.debug(button_id)
        file_path = filedialog.askdirectory(initialdir='/', title='Select the file path')
        if file_path:
            self.entry_dict[button_id].delete(0, tkinter.END)
            self.entry_dict[button_id].insert(tkinter.END, str(normpath(file_path)))
        self.lift()
        logger.debug(f'File path {file_path}')


class Main_Frame(tkinter.Frame):
    def __init__(self, config=Configuration_Values, labels=tuple, entry_type=type, treeview_columns=None | dict, *args, **kwargs) -> None:
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.config = config
        self.entry_list = {}
        self.labels = labels
        self.entry_type = entry_type
        self.treeview_columns = treeview_columns
        button_dict = {}
        config_values = list(self.config.__dict__.values())

        row_value = 0
        for i in range(len(self.labels)):
            ttk.Label(self, text=self.labels[i], justify='left').grid(column=0, row=i, padx=(5), pady=(5, 0))
            match self.entry_type[i]:
                case 'str':
                    entry = ttk.Entry(self, width=40, justify='center')                
                    entry.grid(column=1, row=row_value, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, str(config_values[i]))
                case 'int':
                    valid_command = (self.register(self.__validade_values))
                    entry = ttk.Entry(self, width=40, justify='center', validate='key', validatecommand=(valid_command, '%P'))                
                    entry.grid(column=1, row=row_value, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, config_values[i])   
                    button_dict[self.labels[i]] = valid_command
                case 'path':
                    entry = ttk.Entry(self, width=40, justify='center')                
                    entry.grid(column=1, row=row_value, columnspan=2, sticky='nesw', padx=(5), pady=(5, 0))
                    browse_button = tkinter.Button(self, text='...', width=3)
                    browse_button.grid(column=3, row=i, padx=(0, 5), pady=(5, 0))
                    button_dict[f'{self.labels[i]}'] = browse_button
                    button_dict[f'{self.labels[i]}'].configure(command=lambda info=self.labels[i]: self.__browse_files(info))
                    entry.insert(tkinter.END, str(config_values[i]))
                case 'boolean':
                    entry = tkinter.BooleanVar()
                    entry.set(config_values[i] if not config_values[i] == '' else False)
                    boolean_name = ('True', 'False')
                    radio_bool_button = {}
                    for i in range(len(boolean_name)):
                        radio_bool_button[i] = tkinter.ttk.Radiobutton(self, text=boolean_name[i], value=eval(boolean_name[i]), variable=entry, command=lambda variable=entry: self.__click_radio_bool(variable))
                        radio_bool_button[i].grid(column=1 + i, row=row_value)
                case 'treeview':
                    entry = ttk.Treeview(self, columns=tuple(self.treeview_columns.keys()), show='headings')
                    for key, value in treeview_columns.items():
                        entry.heading(key, text=value)
                        entry.column(key, minwidth=10, width=100)
                    for move_settings in config_values[i]:
                        entry.insert('', tkinter.END, values=(tuple(move_settings.__dict__.values())))
                    entry.grid(column=1, row=row_value, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.bind('<Double-1>', lambda info=self.labels[i]: self.__tree_item_edit(info))
                    entry.bind("<Return>", lambda info=self.labels[i]: self.__tree_item_edit(info))
                    row_value += 1
                    add_button = tkinter.Button(self, text='Add', command=lambda info=self.labels[i]: self.__click_button_add(info), width=15)
                    add_button.grid(column=2, row=row_value, padx=(5, 0), pady=(0,5))
                    button_dict[f'{self.labels[i]}_add']
                    edit_button = tkinter.Button(self, text='Edit', command=lambda info=self.labels[i]: self.__click_button_edit(info), width=15)
                    edit_button.grid(column=3, row=row_value, padx=(0), pady=(0, 5))
                    button_dict[f'{self.labels[i]}_edit']
                    delete_button = tkinter.Button(self, text='Delete', command=lambda info=self.labels[i]: self.__click_button_delete(info), width=15)
                    delete_button.grid(column=4, row=row_value, padx=(0), pady=(0, 5))
                    button_dict[f'{self.labels[i]}_delete']
                case _:
                    entry = ttk.Entry(self, width=40, justify='center')                
                    entry.grid(column=1, row=row_value, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, str(config_values[i]))
            row_value += 1
            self.entry_list[self.labels[i]] = entry
        self.columnconfigure(1, weight=1)
    

    def __tree_item_edit(self, entry_label=str, event=None):
        try:
            if self.row_config.state() == 'normal':
                self.row_config.focus_force()
        except Exception as error:
            logger.debug(error)
            try:
                self.entry_list[entry_label].selection()[0]
                self.row_config = Edit_Values(self.entry_list[entry_label], 
                                tuple(self.treeview_columns.keys()),
                                tuple(self.treeview_columns.values()),
                                'Edit settings')
            except:
                messagebox.showerror('Edit error', 'No row is selected')
        logger.debug('Double click')


    def __click_button_add(self, entry_label=str):
        logger.debug('Click button add')
        empty_values = []
        for _ in range(len(self.entry_list[entry_label])):
            empty_values.append('')
        self.self.entry_list[entry_label].insert('', tkinter.END, values=(tuple(empty_values)))
        children_list = self.self.entry_list[entry_label].get_children()
        self.self.entry_list[entry_label].selection_set(children_list[-1])
        self.__tree_item_edit(None)


    def __click_button_edit(self):
        logger.debug('Click button edit')
        self.__tree_item_edit(self)


    def __click_button_delete(self, entry_label=str) -> bool:
        try:
            selected_item = self.entry_list[entry_label].selection()[0]
            logger.debug(selected_item)
            if messagebox.askquestion('Delete', f'Do you really want to delete the item {selected_item}'):
                self.entry_list[entry_label].delete(selected_item)
                return True
            return False
        except:
            messagebox.showerror('Edit error', 'No row is selected')


    def __click_radio_bool(self, variable):
        logger.debug(variable.get())


    def return_config_updated(self) -> dict:
        new_config = []
        for i in range(len(self.labels)):
            match self.entry_type[i]:
                case 'str':
                    new_config.append(str(self.entry_list[self.labels[i]].get()))
                case 'int':
                    new_config.append(int(self.entry_list[self.labels[i]].get()))
                case 'path':
                    new_config.append(normpath(self.entry_list[self.labels[i]].get()))
                case 'boolean':
                    new_config.append(eval(str(self.entry_list[self.labels[i]].get())))
        return new_config


    def __browse_files(self, button_id=str):
        logger.debug('Browser files')
        logger.debug(button_id)
        file_path = filedialog.askdirectory(initialdir='/', title='Select the file path')
        if file_path:
            self.entry_list[button_id].delete(0, tkinter.END)
            self.entry_list[button_id].insert(tkinter.END, str(normpath(file_path)))
        self.focus_force()
        self.lift()
        logger.debug(f'File path {file_path}')


    def __validade_values(self, value=str):
        if value.isnumeric() or value == '':
            logger.debug(f'{value} is true')
            return True
        else:
            logger.debug(f'{value} is false')
            return False

class File_Settings(tkinter.Frame):
    def __init__(self, 
                 config=Configuration_Values, 
                 file_manag_values=dict, 
                 values_type=tuple, 
                 edit_win_title=str | None, 
                 drop_down_list=None | dict, 
                 config_path=str, *args, **kwargs) -> None:
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.config = config
        self.config_path = config_path
        self.values_type = values_type
        self.edit_win_title = edit_win_title
        self.drop_down_list = drop_down_list
        file_manag_column = tuple(list(file_manag_values.keys()))
        self.file_manag_descri = tuple(list(file_manag_values.values()))
        self.file_manag_tree = ttk.Treeview(self, columns=file_manag_column, show='headings')
        for i in range(len(file_manag_column)):
            self.file_manag_tree.heading(file_manag_column[i], text=self.file_manag_descri[i])
            self.file_manag_tree.column(file_manag_column[i], minwidth=10, width=100)
        for directory_list in self.config.directory_list:
            self.file_manag_tree.insert('', tkinter.END, values=(tuple(directory_list.__dict__.values())))
        self.file_manag_tree.bind('<Double-1>', self.__tree_item_edit)
        self.file_manag_tree.bind("<Return>", self.__tree_item_edit)
        self.file_manag_tree.grid(column=1, 
                        row=0, 
                        columnspan=4,
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))
        y_scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.file_manag_tree.yview)
        self.file_manag_tree.configure(yscroll=y_scrollbar.set)
        y_scrollbar.grid(row=0, 
                        column=5, 
                        sticky='ns',
                        padx=(0, 5),
                        pady=(5, 0))
        self.file_manag_tree.columnconfigure(0, weight=1)
        self.file_manag_tree.rowconfigure(0, weight=1)
        self.add_button = tkinter.Button(self, text='Add', command=self.__click_button_add, width=15)
        self.add_button.grid(column=2, row=1, padx=(5, 0), pady=(0,5))
        self.edit_button = tkinter.Button(self, text='Edit', command=self.__click_button_edit, width=15)
        self.edit_button.grid(column=3, row=1, padx=(0), pady=(0, 5))
        self.delete_button = tkinter.Button(self, text='Delete', command=self.__click_button_delete, width=15)
        self.delete_button.grid(column=4, row=1, padx=(0), pady=(0, 5))

    
    def __tree_item_edit(self, event):
        try:
            if self.file_config.state() == 'normal':
                self.file_config.focus_force()
        except Exception as error:
            logger.debug(error)
            try:
                self.file_manag_tree.selection()[0]
                self.file_config = Edit_Values(self.file_manag_tree, 
                                self.file_manag_descri,
                                self.values_type,
                                self.edit_win_title if not self.edit_win_title == None else 'Edit values',
                                drop_down_list=self.drop_down_list)
            except:
                messagebox.showerror('Edit error', 'No row is selected')
        logger.debug('Double click')


    def return_config_updated(self) -> list:
        move_settings_list = [self.file_manag_tree.item(value)['values'] for value in self.file_manag_tree.get_children()]
        return move_settings_list


    def __click_button_add(self):
        empty_values = []
        for _ in range(len(self.file_manag_descri)):
            empty_values.append('')
        self.file_manag_tree.insert('', tkinter.END, values=(tuple(empty_values)))
        children_list = self.file_manag_tree.get_children()
        self.file_manag_tree.selection_set(children_list[-1])
        self.__tree_item_edit(None)


    def __click_button_edit(self):
        self.__tree_item_edit(self)


    def __click_button_delete(self) -> bool:
        try:
            selected_item = self.file_manag_tree.selection()[0]
            logger.debug(selected_item)
            if messagebox.askquestion('Delete', f'Do you really want to delete the item {selected_item}'):
                self.file_manag_tree.delete(selected_item)
                return True
            return False
        except:
            messagebox.showerror('Edit error', 'No row is selected')


    def add_item(self) -> None:
        pass

class Config_Window(tkinter.Tk):
    def __init__(self, config=Configuration_Values, config_path=str, *args, **kwargs) -> None:
        '''
        Default main configuration window        
        ''' 
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.config = config
        self.config_path = config_path
        self.title('Configuration')
        self.minsize(width=400, height=300)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tab_control = ttk.Notebook(self)

        # Tab Main
        self.tab_main = Main_Frame(self.config)
        self.tab_file_settings = File_Settings(self.config)

        # Tab File Settings
        self.tab_file_settings.columnconfigure(1, weight=1)
        self.tab_file_settings.rowconfigure(0, weight=1)

        # Add tabs to tab control
        self.tab_control.add(self.tab_main, text='Main')
        self.tab_control.add(self.tab_file_settings, text='File Settings')
        self.tab_control.grid(column=0, 
                        row=0, 
                        columnspan=6, 
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))
        
        # Buttons
        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=4, row=1, padx=(5), pady=(0, 5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=5, row=1, padx=(5), pady=(0, 5))


        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)
        

    def __click_button_cancel(self):
        logger.debug('Cancel click')
        self.__on_window_close()


    def __click_button_save(self):
        logger.debug('Save click')
        logger.debug('')
        main_config = self.tab_main.return_config_updated()
        file_settings = self.tab_file_settings.return_config_updated()
        new_config = Configuration_Values(int(main_config[0]),
                int(main_config[1]),
                main_config[2], 
                [Move_Settings(normpath(item[0]), 
                        normpath(item[1]),
                        item[2],
                        int(item[3]),
                        eval(item[4]),
                        item[5]) for item in file_settings])
        if not self.config.__eq__(new_config):
            logger.debug('Not equals')
            json_config.save_json_config(self.config_path, new_config.convert_to_dict())
        self.destroy()


    def __on_window_close(self):
        logger.debug('On close click')
        self.destroy()
    

class Main_App(tkinter.Tk):
    '''
    Main window for file processing automation with log queue
    '''
    def __init__(self, title=str, config_file_name=str, icon_path=str, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title(title)
        self.config_file_name = config_file_name
        self.minsize(width=500, height=500)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_columnconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1, minsize=50)
        self.grid_columnconfigure(3, weight=0, minsize=50)

        # basic menu bar
        menu_bar = tkinter.Menu(self)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Start   ', command=self.__click_button_start)
        file_menu.add_command(label='Stop    ', command=self.__click_button_stop)        
        file_menu.add_separator()
        file_menu.add_command(label='Exit   ', command=self.__quit_window)
        menu_bar.add_cascade(label='File   ', menu=file_menu)

        help_menu = tkinter.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='About   ', command=self.__about_command)
        menu_bar.add_cascade(label='Help   ', menu=help_menu)
        self.config(menu=menu_bar)

        # Main buttons
        start_button = tkinter.Button(self, text='Start', command=self.__click_button_start, width=20)
        start_button.grid(column=0, row=0, padx=(3), pady=(3), sticky='nesw')

        stop_button = tkinter.Button(self, text='Stop', command=self.__click_button_stop, width=20)
        stop_button.grid(column=1, row=0, padx=(3), pady=(3), sticky='nesw')

        config_button = tkinter.Button(self, text='Configuration', command=self.__click_button_config, width=20)
        config_button.grid(column=3, row=0, padx=(3), pady=(3), sticky='nesw')

        # Scrolled text field
        self.scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        self.scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        self.scrolled_text.grid(column=0, row=1, columnspan=4, sticky='nesw', padx=(3), pady=(3))

        # Set log queuer
        self.log_queue = Queue()
        logger.addHandler(log.LogQueuer(self.log_queue))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)
        self.after(100, self.__pull_log_queue)

        # Set tray icon values
        icon_image = Image.open(icon_path)
        tray_menu = (pystray.MenuItem('Open', self.__show_window), pystray.MenuItem('Quit', self.__quit_window))
        self.tray_icon = pystray.Icon('Tkinter GUI', icon_image, title, tray_menu)


    def __display(self, message):
        # Add value to scrolled text field
        self.scrolled_text.configure(state='normal')
        line_count = int(float(self.scrolled_text.index('end')))
        # Define maximum number of lines and delete the old ones
        if line_count > 300:
            self.scrolled_text.delete('1.0', str("{:0.1f}".format(line_count - 299)))
        self.scrolled_text.insert(tkinter.END, f'{message}\n')
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview(tkinter.END)


    def __about_command(event_value):
        # Window will be created
        logger.info('About clicked')


    def __pull_log_queue(self):
        # Get value from log_queue
        while not self.log_queue.empty():
            message = self.log_queue.get(block=False)
            self.__display(message)
        self.after(100, self.__pull_log_queue)


    def __click_button_start(self):
        # Start main thread and clear event
        logger.debug('Button start clicked')
        if event.is_set():
            thread = threading.Thread(target=main, args=(event,), daemon=True,  name='File_Mover')
            thread.start()
            event.clear()


    def __click_button_stop(self):
        # Set event to stop thread execution
        logger.debug('Button stop clicked')
        event.set()


    def __click_button_config(self):
        # Stop thread execution and open configuration window
        logger.debug('Button config clicked')
        try:
            if self.config_window.state() == 'normal':
                self.config_window.focus_force()
        except Exception as error:
            logger.info(error)
            event.set()
            self.config_window = Config_Window(Configuration_Values.check_type_insertion(self.config_file_name), self.config_file_name)


    def __on_window_close(self):
        # Hide window to tray
        self.__hide_window_to_tray()


    def __quit_window(self):
        # Quit application
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            event.set()
            logger.info('Forcing kill thread if it is open')
            try:
                self.tray_icon.stop()
            except:
                logger.warning('Tray icon is not started')
            self.after(150, self.deiconify)
            self.destroy()
    

    def __show_window(self):
        # Show window hidden in tray
        self.tray_icon.stop()
        self.after(150, self.deiconify)


    def __hide_window_to_tray(self):
        # Hide window to tray
        logger.debug('Run tray icon')
        self.withdraw()
        self.tray_icon.run()


class About(tkinter.Toplevel):
    def __init__(self, title='About', label_values=str, image_file=str, *args, **kwargs) -> None:
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.geometry('500 x 400')
        self.title = title
        self.resizable(width=False, height=False)
        image = ImageTk.PhotoImage(Image.open(image_file))
        image_label = tkinter.Label(self, image=image)
        image_label.grid(column=0, row=0, columnspan=3)
        image_label.configure(width=450)

        text_label = tkinter.Label(self, label_values)
        text_label.grid(column=0, row=1, columnspan=3)

        ok_button = tkinter.Button(text='Ok', width=15, command=self.__pressed_ok_button)
        ok_button.grid(column=3, row=2)
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)    


    def __pressed_ok_button(self):
        self.__on_window_close()
    

    def __on_window_close(self):
        self.destroy()


def __load_configuration(config_path=str) -> dict:
    '''
    Load configuration from .json file. If json file do not exists it will be created using the template values.
    '''
    try:
        config_template = """{
        "wait_time" : 15,
        "files_per_cicle" : 1500,
        "month_name_list" : [
            "01 January",
            "02 February",
            "03 March",
            "04 April",
            "05 May",
            "06 June",
            "07 July",
            "08 August",
            "09 September",
            "10 October",
            "11 November",
            "12 December"
            ],
            "directory_list" : [
                {
                    "source" : "./Source",
                    "destination" : "./Destin",
                    "extention" : "",
                    "days_from_today" : 0,
                    "copy" : "False"
                    "path_organization" : "Daily"
                }
            ]
        }"""
        config = json_config.load_json_config(config_path, config_template)
        return Configuration_Values(int(config['wait_time']),
                int(config['files_per_cicle']),
                config['month_name_list'], 
                [Move_Settings(normpath(item['source']), 
                        normpath(item['destination']),
                        item['extention'],
                        int(item['days_from_today']),
                        eval(str(item['copy'])),
                        item['path_organization']) for item in config['directory_list']])
    except Exception as error:
        logger.critical(f'Error loading configuration file. {error}')
        sleep(3)
        quit()


if __name__ == '__main__':
    event = threading.Event()
    window = Main_App('GUI Builder', 'file_mover_backup.json', './Icon/tiger.ico')
    window.mainloop()