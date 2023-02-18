import tkinter, logging
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from os.path import normpath, exists

logger = logging.getLogger('gui_classes')


class Edit_Values(tkinter.Toplevel):
    def __init__(self, 
                    parent=ttk.Treeview, 
                    key_list=tuple, 
                    type_list=tuple,
                    edit_title=str, 
                    values_disabled=None, 
                    focus_force=None, 
                    drop_down_list=None,
                    *args, **kwargs) -> None:
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.last_grab = self.grab_current()
        self.grab_set()
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


    def destroy(self) -> None:
        if self.last_grab:
            self.last_grab.grab_set()
        return super().destroy()


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
        self.labels = labels
        self.entry_type = entry_type
        self.treeview_columns = treeview_columns
        self.entry_list = {}
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




# Basic About class
class About(tkinter.Toplevel):
    def __init__(self, title=str, label_values=str, image_file=str, *args, **kwargs) -> None:
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.last_grab = self.grab_current()
        self.grab_set()
        self.geometry('450x400')
        self.title(title)
        self.resizable(width=False, height=False)
        image = Image.open(image_file)
        image_tk = ImageTk.PhotoImage(image=image)
        image_label = tkinter.Label(self, image=image_tk, justify='center')
        image_label.image = image_tk
        image_label.grid(column=0, row=0, columnspan=2, padx=(10), pady=(5, 0))

        text_label = tkinter.Label(self, text=label_values, justify='left')
        text_label.grid(column=0, row=1, rowspan=2, sticky='nw', padx=(5), pady=(5, 0))

        ok_button = tkinter.Button(self, text='Ok', width=15, command=self.__pressed_ok_button)
        ok_button.grid(column=1, row=2, sticky='se', padx=(10), pady=(5, 10))

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)    
        
    def destroy(self) -> None:
        if self.last_grab:
            self.last_grab.grab_set()
        return super().destroy()


    def __pressed_ok_button(self):
        self.__on_window_close()
    

    def __on_window_close(self):
        self.destroy()