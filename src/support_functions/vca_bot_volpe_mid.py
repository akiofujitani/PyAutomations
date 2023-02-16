import file_handler, vca_handler, vca_handler_frame_size, json_config, datetime, tkinter, threading, sys
from time import sleep
from tkinter import messagebox
from ntpath import join
from os.path import normpath
import logger as log
from dataclasses import dataclass
from os.path import normpath, abspath, exists
from tkinter import filedialog
from tkinter import ttk


logger = log.logger('vca_bot_volpe_mid')


config_template = """{
    "wait_time" : "5",  
    "vca_path" : "C:/LMS/HOST_IMPORT/VCA/IMPORT_TEMP",
    "vca_done" : "C:/LMS/HOST_IMPORT/VCA/NOVO_LMS",
    "vca_new_file": "C:/LMS/HOST_IMPORT/VCA/359",
    "extension" : "vca",
    "directory_list" : [
            {
                "source" : "C:/LMS/HOST_EXPORT/VCA/read",
                "destination" : "C:/LMS/HOST_EXPORT/VCA/NOVO_LMS",
                "extension" : "vca",
                "copy" : "True",
            },
            {
                "source" : "C:/LMS/HOST_EXPORT/VCA/read",
                "destination" : "C:/LMS/HOST_EXPORT/VCA/MID_READ",
                "extension" : "vca",
                "copy" : "False",
            }
    ]
}"""


@dataclass
class Move_Settings:
    source: str
    destination: str
    extension: str
    copy: bool


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, source=str, destination=str, extension=str, copy=bool):
        try:
            source = normpath(abspath(str(source)))
            destination = normpath(abspath(str(destination)))
            extension = str(extension)
            copy = eval(str(copy))
            return cls(source, destination, extension, copy)
        except Exception as error:
            raise error


    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['source'] = self.source.replace('\\', '/')
        values_dict['destination'] = self.destination.replace('\\', '/')
        values_dict['extension'] = self.extension
        values_dict['copy'] = self.copy
        return values_dict

@dataclass
class Configuration_Values:
    wait_time: int
    vca_path: str
    vca_done: str
    vca_new_file: str
    extension : str
    directory_list : list


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, config_file_path=str, template=str):
        try:
            config = json_config.load_json_config(config_file_path, template)
            wait_time = int(config['wait_time'])
            vca_path = normpath(abspath(str(config['vca_path'])))
            vca_done = normpath(abspath(str(config['vca_done'])))
            vca_new_file = normpath(abspath(str(config['vca_new_file'])))
            extension = str(config['extension'])
            directory_list = [Move_Settings.check_type_insertion(item['source'],
                            item['destination'],
                            item['extension'],
                            item['copy']) for item in config['directory_list']]
            return cls(wait_time, vca_path, vca_done, vca_new_file, extension, directory_list)
        except Exception as error:
            raise error


    def convert_to_dict(self) -> dict:
        values_dict = {}
        values_dict['wait_time'] = self.wait_time
        values_dict['vca_path'] = self.vca_path
        values_dict['vca_done'] = self.vca_done
        values_dict['vca_new_file'] = self.vca_new_file
        values_dict['extension'] = self.extension
        values_dict['directory_list'] = [directory_value.convert_to_dict() for directory_value in self.directory_list]
        return values_dict


    def directory_list_add(self, move_settings=Move_Settings) -> None:
        self.directory_list.append(move_settings)


    def min_to_seconds(self) -> int:
        return self.wait_time * 60


class ThreadEventException(Exception):
    '''Thread event exception'''
    pass


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
        button_dict = {}
        self.entry_list = {}
        config_values = list(self.config.__dict__.values())
        self.labels = ('Wait time', 'VCA Import', 'VCA VOLPE', 'VCA Middleware', 'Extension')
        self.entry_type = ('int', 'path', 'path', 'path', 'str')
        for i in range(len(self.labels)):
            ttk.Label(self, text=self.labels[i], justify='left').grid(column=0, row=i, padx=(5), pady=(5, 0))
            match self.entry_type[i]:
                case 'str':
                    entry = ttk.Entry(self, width=40, justify='center')                
                    entry.grid(column=1, row=i, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, str(config_values[i]))
                case 'int':
                    valid_command = (self.register(self.__validade_values))
                    entry = ttk.Entry(self, width=40, justify='center', validate='key', validatecommand=(valid_command, '%P'))                
                    entry.grid(column=1, row=i, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, config_values[i])   
                    button_dict[self.labels[i]] = valid_command
                case 'path':
                    entry = ttk.Entry(self, width=40, justify='center')                
                    entry.grid(column=1, row=i, columnspan=2, sticky='nesw', padx=(5), pady=(5, 0))
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
                        radio_bool_button[i].grid(column=1 + i, row=i)
                case _:
                    entry = ttk.Entry(self, width=40, justify='center')                
                    entry.grid(column=1, row=i, columnspan=3, sticky='nesw', padx=(5), pady=(5, 0))
                    entry.insert(tkinter.END, str(config_values[i]))
            self.entry_list[self.labels[i]] = entry
        self.columnconfigure(1, weight=1)
    

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
    def __init__(self, config=Configuration_Values, config_path=str, *args, **kwargs) -> None:
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.config = config
        self.config_path = config_path
        file_manag_column = ('source', 'destin', 'extension', 'copy')
        self.file_manag_descri = ('Souce', 'Destination', 'Extension', 'Make copy')
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
                                ('path', 'path', 'str', 'boolean'),
                                'Edit file move settings')
            except:
                messagebox.showerror('Edit error', 'No row is selected')
        logger.debug('Double click')


    def return_config_updated(self) -> list:
        logger.debug('Return configuration values for file settings')
        move_settings_list = [self.file_manag_tree.item(value)['values'] for value in self.file_manag_tree.get_children()]
        return move_settings_list


    def __click_button_add(self):
        logger.debug('Click button add')
        empty_values = []
        for _ in range(len(self.file_manag_descri)):
            empty_values.append('')
        self.file_manag_tree.insert('', tkinter.END, values=(tuple(empty_values)))
        children_list = self.file_manag_tree.get_children()
        self.file_manag_tree.selection_set(children_list[-1])
        self.__tree_item_edit(None)


    def __click_button_edit(self):
        logger.debug('Click button edit')
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

class Config_Window(tkinter.Toplevel):
    def __init__(self, config=Configuration_Values, config_path=str, *args, **kwargs) -> None:
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.config = config
        self.config_path = config_path
        self.title('Configuration')
        self.minsize(width=400, height=300)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tab_control = ttk.Notebook(self)

        # Tabs 
        self.tab_main = Main_Frame(self.config, master=self.tab_control)
        self.tab_file_settings = File_Settings(self.config, master=self.tab_control)
        self.tab_control.add(self.tab_main, text='Main')
        self.tab_control.add(self.tab_file_settings, text='File Settings')
        self.tab_control.grid(column=0, 
                        row=0, 
                        columnspan=6, 
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))

        self.tab_file_settings.columnconfigure(1, weight=1)
        self.tab_file_settings.rowconfigure(0, weight=1)

        # Buttons

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
        main_config = self.tab_main.return_config_updated()
        file_settings = self.tab_file_settings.return_config_updated()
        new_config = Configuration_Values(int(main_config[0]),
                normpath(main_config[1]),
                normpath(main_config[2]),
                normpath(main_config[3]),
                str(main_config[4]),
                [Move_Settings(normpath(item[0]), 
                        normpath(item[1]),
                        item[2],
                        eval(item[3])) for item in file_settings])
        if not self.config.__eq__(new_config):
            logger.debug('Not equals')
            try:
                json_config.save_json_config(self.config_path, new_config.convert_to_dict())
                logger.info(f'New config saved to {self.config_path}')
            except Exception as error:
                messagebox.showerror('Configuration save', 'Error saving configuration')
                logger.error(error)
        self.destroy()


    def __on_window_close(self):
        logger.debug('Window close click')
        self.destroy()

class Main_App(tkinter.Tk):
    def __init__(self, title=str, config_file_name=str, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title(title)
        self.config_file_name = config_file_name
        self.minsize(width=500, height=500)
        self.grid_rowconfigure(0, minsize=40)
        self.grid_columnconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1, minsize=50)
        self.grid_columnconfigure(3, weight=0, minsize=50)

        start_button = tkinter.Button(self, text='Start', command=self.__click_button_start, width=25)
        start_button.grid(column=0, row=0, padx=(3), pady=(3), sticky='nesw')

        stop_button = tkinter.Button(self, text='Stop', command=self.__click_button_stop, width=25)
        stop_button.grid(column=1, row=0, padx=(3), pady=(3), sticky='nesw')

        config_button = tkinter.Button(self, text='Configuration', command=self.__click_button_config, width=25)
        config_button.grid(column=3, row=0, padx=(3), pady=(3), sticky='nesw')

        scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        scrolled_text.grid(column=0, row=1, columnspan=4, sticky='nesw', padx=(3), pady=(3))
        logger.addHanlder(log.TextHandler(scrolled_text))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)


    def __click_button_start(self):
        logger.debug('Button start clicked')
        if event.is_set():
            thread = threading.Thread(target=main, args=(event,), daemon=True,  name='File_Mover')
            thread.start()
            event.clear()


    def __click_button_stop(self):
        logger.debug('Button stop clicked')
        event.set()


    def __click_button_config(self):
        logger.debug('Button config clicked')
        try:
            if self.config_window.state() == 'normal':
                self.config_window.focus_force()
        except Exception as error:
            logger.info(error)
            event.set()
            self.config_window = Config_Window(Configuration_Values.check_type_insertion(self.config_file_name), self.config_file_name)


    def __on_window_close(self):
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            event.set()
            logger.info('Forcing kill thread if it is open')
            self.destroy()
            sys.exit()


def __resize_both_sides(trcfmt=dict, hbox=int, vbox=int) -> dict:
    try:
        resized_trcfmt = {}
        temp_trcfmt = {}
        for side, value in trcfmt.items():
            shape_resized = vca_handler_frame_size.frame_resize(value['R'], hbox[side], vbox[side])
            temp_trcfmt['R'] = list(shape_resized.values())
            temp_trcfmt['TRCFMT'] = ['1', str(len(shape_resized)), 'E', side, 'F']
            resized_trcfmt[side] = temp_trcfmt
            temp_trcfmt = {}
            if len(trcfmt) == 1:
                other_side = 'R' if side == 'R' else 'L'
                temp_trcfmt['R'] = list(vca_handler_frame_size.shape_mirror(shape_resized).values())
                temp_trcfmt['TRCFMT'] = ['1', len(shape_resized), 'E', other_side, 'F']
                resized_trcfmt[other_side] = temp_trcfmt
            logger.info(f'Side {side} done')      
        return resized_trcfmt
    except Exception as error:
        logger.error(error)
        event.set()
        return


def vca_file_process(event=threading.Event):
    try:
        config = Configuration_Values.check_type_insertion('config.json', config_template)
    except Exception as error:
        logger.critical(error)
        messagebox.showerror('VCA Bot Volpe/Middleware', f'Error loading configuration json file due \n{error}')
        event.set()
        return

    try:
        while True:
            # VCA converter
            if event.is_set():
                logger.info('Proccess interrupted')
                return
            vca_list = file_handler.file_list(config.vca_path, config.extension)
            if len(vca_list) > 0:
                logger.info(f'List for {config.vca_path} contains {len(vca_list)}')
                for vca_file in vca_list:
                    try:
                        vca_data = file_handler.file_reader(join(config.vca_path, vca_file))
                        job_vca = vca_handler.VCA_to_dict(vca_data)
                        logger.info(f'{job_vca["JOB"]}\n')
                        if 'TRCFMT' not in job_vca.keys() or not int(job_vca['TRCFMT']['R']['TRCFMT'][1]) == 400:
                            file_handler.file_move_copy(config.vca_path, config.path_done, vca_file, True)
                            sleep(0.5)
                            file_handler.file_move_copy(config.vca_path, config.path_new, vca_file, False)
                            logger.info(f'File {file} copied/moved without changes')
                        else:
                            trace_format_resized = __resize_both_sides(job_vca['TRCFMT'], job_vca['HBOX'], job_vca['VBOX'])
                            job_vca['TRCFMT'] = trace_format_resized
                            vca_contents_string = vca_handler.dict_do_VCA(job_vca)
                            file_handler.file_move_copy(config.path, config.path_done, vca_file, False)
                            file_handler.file_writer(config.path_new, vca_file, vca_contents_string)
                            logger.debug(vca_contents_string)
                            logger.info(f'File {file} copied/moved changing frame values')
                    except Exception as error:
                        logger.error(f'Error {error} in file {vca_file}')
                    if event.is_set():
                        logger.info('Proccess interrupted')
                        return

            # File mover
            if len(config.directory_list) > 0:
                for move_group in config.directory_list:
                    try:
                        file_list = file_handler.file_list(move_group.source, move_group.extension)
                        if len(file_list) > 0:
                            logger.info(f'File list for {move_group.source} contains {len(file_list)}')
                            for file in file_list:
                                file_handler.file_move_copy(move_group.source, move_group.destination, file, move_group.copy)
                                logger.info(f'File {file} copied/moved')
                                sleep(0.1)
                    except Exception as error:
                        logger.error(f'Error processing files {error}')
                    if event.is_set():
                        logger.info('Proccess interrupted')
                        return
            logger.info(f'Waiting... {config.wait_time} seconds')
            sleep(config.wait_time)
    except Exception as error:
        logger.critical(error)
        event.set()
        return


def main(event=threading.Event):
    vca_file_process(event)


if __name__ == '__main__':
    window = Main_App('VCA Data Process', 'config.json')
    event = threading.Event()
    thread = threading.Thread(target=main, args=(event, ), daemon=True, name='VCA_Data_Process')
    thread.start()
    window.mainloop()