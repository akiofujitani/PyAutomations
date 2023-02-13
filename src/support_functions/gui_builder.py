import tkinter, json_config
from file_mover_backup import *
from tkinter import ttk
import logger as log
from os.path import normpath
from os.path import exists
from time import sleep
from tkinter import filedialog
from tkinter import messagebox


logger = log.logger('gui_builder')

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
    def __init__(self, config=Configuration_Values, *args, **kwargs) -> None:
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.config = config
        ttk.Label(self, 
                        text='Wait time', 
                        justify='left').grid(column=0, 
                                        row=0, 
                                        padx=(5), 
                                        pady=(5, 0))
        ttk.Label(self, 
                        text='Files per cicle', 
                        justify='left').grid(column=0, 
                                        row=1, 
                                        padx=(5), 
                                        pady=(5, 0))
        ttk.Label(self, 
                        text='Months naming', 
                        justify='left').grid(column=0, 
                                        row=2, 
                                        padx=(5), 
                                        pady=(5, 0))

        valid_command = (self.register(self.__validade_values))
        self.wait_time_entry = ttk.Entry(self, 
                        width=40, 
                        justify='center', 
                        validate='key', 
                        validatecommand=(valid_command, '%P'))
        self.wait_time_entry.grid(column=1, 
                        row=0, 
                        columnspan=3, 
                        sticky='nesw', 
                        padx=(5), 
                        pady=(5, 0))
        self.wait_time_entry.insert(tkinter.END, str(self.config.wait_time))
        self.files_per_cicle = ttk.Entry(self, 
                        width=40, 
                        justify='center', 
                        validate='key', 
                        validatecommand=(valid_command, '%P'))
        self.files_per_cicle.grid(column=1,
                        row=1, 
                        columnspan=3, 
                        sticky='nesw', 
                        padx=(5), 
                        pady=(5, 0))
        self.files_per_cicle.insert(tkinter.END, str(self.config.file_per_cicle))
        month_columns = ('month_number' , 'month_description')
        self.months_naming_tree = ttk.Treeview(self, columns=month_columns, show='headings')
        self.months_naming_tree.heading('month_number', text='Month Number')
        self.months_naming_tree.heading('month_description', text='Month Description')
        for i in range(len(self.config.month_name_list)):
            self.months_naming_tree.insert('', tkinter.END, values=(i + 1, self.config.month_name_list[i]))
        self.months_naming_tree.bind('<Double-1>', self.__tree_item_edit)
        self.months_naming_tree.bind("<Return>", self.__tree_item_edit)
        self.months_naming_tree.grid(column=1, 
                        row=2, 
                        columnspan=2,
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))
        self.months_naming_tree.columnconfigure(1, weight=1)
        self.months_naming_tree.columnconfigure(0, weight=1)
        scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=self.months_naming_tree.yview)
        self.months_naming_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, 
                        column=3, 
                        sticky='ns',
                        padx=(0, 5),
                        pady=(5, 0))
        self.edit_button = tkinter.Button(self, text='Edit', command=self.__click_button_edit, width=15)
        self.edit_button.grid(column=2, row=3, padx=(5, 0), pady=(0, 5))

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
    

    def return_config_updated(self) -> dict:
        new_config = [int(self.wait_time_entry.get()),
                            int(self.files_per_cicle.get()),
                            [self.months_naming_tree.item(value)['values'][1] for value in self.months_naming_tree.get_children()]]
        return new_config


    def __click_button_edit(self):
        self.__tree_item_edit(self)


    def __tree_item_edit(self, event):
        try:
            if self.month_edit.state() == 'normal':
                self.month_edit.focus_force()
        except Exception as error:
            logger.debug(error)
            try:
                self.months_naming_tree.selection()[0]
                self.month_edit = Edit_Values(self.months_naming_tree, 
                                ('Month number', 
                                'Month Description'),
                                ('int', 'str'), 
                                'Edit month description', 
                                ['Month number'], 
                                focus_force='Month Description')
            except:
                messagebox.showerror('Edit error', 'No row is selected')
        logger.debug('Double click')
    

    def __validade_values(self, value=str):
        if value.isnumeric() or value == '':
            logger.debug(f'{value} is true')
            return True
        else:
            logger.debug(f'{value} is false')
            return False

class File_Settings(tkinter.Frame):
    def __init__(self, config=Configuration_Values, config_path=str, *args, **kwargs) -> None:
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.config = config
        self.config_path = config_path
        file_manag_column = ('source', 'destin', 'extention', 'wait_days', 'copy', 'path_organization')
        self.file_manag_descri = ('Souce', 'Destination', 'Extention', 'Period to move/copy', 'Make copy', 'Path Organization')
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
                                ('path', 'path', 'str', 'int', 'boolean', 'combo_box'),
                                'Edit file move settings',
                                drop_down_list={'Path Organization': ('Yearly', 'Monthly', 'Daily')})
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
        self.tab_control.add(self.tab_main, text='Main')
        self.tab_control.add(self.tab_file_settings, text='File Settings')
        self.tab_control.grid(column=0, 
                        row=0, 
                        columnspan=6, 
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))

        # Tab File Settings
        self.tab_file_settings.columnconfigure(1, weight=1)
        self.tab_file_settings.rowconfigure(0, weight=1)
        
        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=4, row=1, padx=(5), pady=(0, 5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=5, row=1, padx=(5), pady=(0, 5))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)
        self.month_edit = None
        

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
    config = __load_configuration('file_mover_backup.json')
    window = Config_Window(config, 'file_mover_backup.json')
    window.mainloop()