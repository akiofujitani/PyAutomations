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

class EntryPopup(ttk.Entry):
    def __init__(self, parent, iid, column, text, **kw):
        ttk.Style().configure('pad.TEntry', padding='1 1 1 1')
        super().__init__(parent, style='pad.TEntry', **kw)
        self.tv = parent
        self.iid = iid
        self.column = column

        self.insert(0, text) 
        # self['state'] = 'readonly'
        # self['readonlybackground'] = 'white'
        # self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False

        self.focus_force()
        self.select_all()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())


    def on_return(self, event):
        rowid = self.tv.focus()
        vals = self.tv.item(rowid, 'values')
        vals = list(vals)
        vals[self.column] = self.get()
        self.tv.item(rowid, values=vals)
        self.destroy()


    def select_all(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'


class Edit_Values(tkinter.Toplevel):
    def __init__(self, parent=ttk.Treeview, key_list=list, edit_title=str, values_disabled=None, path_keys=None, focus_force=None, *args, **kwargs) -> None:
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.parent = parent
        self.title(edit_title)
        self.transient()
        self.selected_item = self.parent.selection()[0]
        self.record_value = [str(value) for value in self.parent.item(self.selected_item)['values']]
        self.entry_dict = {}
        self.button_dict = {}
        for key_index in range(len(key_list)):
            ttk.Label(self, text=key_list[key_index], justify='left').grid(column=0, row=key_index, padx=(5), pady=(5, 0))
            entry = ttk.Entry(self, width=50, justify='center')
            entry_column_span = 3
            if not path_keys == None:
                if key_list[key_index] in path_keys:
                    entry_column_span = 2
                    entry.grid(column=1, row=key_index, sticky='nesw', columnspan=entry_column_span, padx=(5, 0), pady=(5, 0))
                    browse_button = tkinter.Button(self, text='...', width=3)
                    browse_button.grid(column=3, row=key_index, padx=(0, 5), pady=(5, 0))
                    self.button_dict[f'{key_list[key_index]}_button'] = browse_button
                    self.button_dict[f'{key_list[key_index]}_button'].configure(command= lambda info=key_list[key_index]: self.__browse_files(info))
            else:
                entry.grid(column=1, row=key_index, sticky='nesw', columnspan=entry_column_span, padx=(5), pady=(5, 0))
            entry.grid(column=1, row=key_index, sticky='nesw', columnspan=entry_column_span, padx=(5), pady=(5, 0))
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
        

    def __click_button_cancel(self):
        logger.debug('Button cancel')
        self.destroy()
    

    def __click_button_save(self, event=None):
        logger.debug('Button save')
        new_record = []
        for entry in self.entry_dict.values():
            new_record.append(entry.get())
        for i in range(len(new_record)):
            if not self.record_value[i] == new_record[i]:
                self.parent.item(self.selected_item, values=new_record)
        logger.debug(f'Button save {new_record[1]}')
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

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
    

    def return_config_updated(self) -> dict:
        new_config = [int(self.wait_time_entry.get()),
                            int(self.files_per_cicle.get()),
                            [self.months_naming_tree.item(value)['values'][1] for value in self.months_naming_tree.get_children()]]
        return new_config
    

    def __tree_item_edit(self, event):
        try:
            if self.month_edit.state() == 'normal':
                self.month_edit.focus_force()
        except Exception as error:
            logger.debug(error)
            self.month_edit = Edit_Values(self.months_naming_tree, 
                            ['Month number', 
                            'Month Description'], 
                            'Edit month description', 
                            ['Month number'], 
                            focus_force='Month Description')
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
        file_manag_column = ('source', 'destin', 'extention', 'wait_days', 'copy')
        self.file_manag_descri = ('Souce', 'Destination', 'Extention', 'Days to move/copy', 'Make copy')
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

    
    def __tree_item_edit(self, event):
        try:
            if self.file_config.state() == 'normal':
                self.file_config.focus_force()
        except Exception as error:
            logger.debug(error)
            self.file_config = Edit_Values(self.file_manag_tree, 
                            self.file_manag_descri, 
                            'Edit file move settings',
                            path_keys=['Souce', 'Destination'])
        logger.debug('Double click')


    def return_config_updated(self) -> list:
        move_settings_list = [self.file_manag_tree.item(value)['values'] for value in self.file_manag_tree.get_children()]
        return move_settings_list


    def delete_item(self) -> bool:
        selected_item = self.file_manag_tree.selection()[0]
        logger.debug(selected_item)
        if messagebox.askquestion('Delete', f'Do you really want to delete the item {selected_item}'):
            self.file_manag_tree.delete(selected_item)
            return True
        return False


class Config_Window(tkinter.Tk):
    def __init__(self, config=Configuration_Values, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.config = config
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
                        columnspan=4, 
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))

        # Tab File Settings
        self.tab_file_settings.columnconfigure(1, weight=1)
        self.tab_file_settings.rowconfigure(0, weight=1)
        
        self.delete_button = tkinter.Button(self, text='Delete', command=self.__click_button_delete, width=15)
        self.delete_button.grid(column=1, row=1, padx=(5), pady=(0, 5))
        self.delete_button.configure(default='disabled')
        self.delete_button.configure()
        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=1, padx=(5), pady=(0, 5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=1, padx=(5), pady=(0, 5))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)
        self.tab_control.bind('<<NotebookTabChanged>>', self.__tab_selected)
        self.month_edit = None


    def __tab_selected(self, event):
        if self.tab_control.index(self.tab_control.select()) == 0:
            self.delete_button.configure(state='disabled')
        else:
            self.delete_button.configure(state='normal')


    def __click_button_delete(self):
        logger.debug('Delete button clicked')
        self.tab_file_settings.delete_item()
        

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
                        eval(item[4])) for item in file_settings])
        if not self.config.__eq__(new_config):
            logger.debug('Not equals')
            json_config.save_json_config(self.config_path, new_config.__dict__)
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
        "wait_time_min" : 15,
        "files_per_cicle" : 1500,
        "month_name" : [
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
                    "destin" : "./Destin",
                    "extension" : "",
                    "days_from_today" : 0,
                    "copy" : "False"
                }
            ]
        }"""
        config = json_config.load_json_config(config_path, config_template)
        return Configuration_Values(int(config['wait_time_min']),
                int(config['files_per_cicle']),
                config['month_name'], 
                [Move_Settings(normpath(item['source']), 
                        normpath(item['destin']),
                        item['extension'],
                        int(item['days_from_today']),
                        eval(item['copy'])) for item in config['directory_list']])
    except Exception as error:
        logger.critical(f'Error loading configuration file. {error}')
        sleep(3)
        quit()


if __name__ == '__main__':
    config = __load_configuration('file_mover_backup.json')
    window = Config_Window(config, 'file_mover_backup.json')
    window.mainloop()