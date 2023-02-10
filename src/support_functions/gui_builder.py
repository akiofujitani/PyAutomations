import tkinter, json_config, file_mover_backup
from tkinter import ttk
import logger as log
from os.path import normpath
from time import sleep
from tkinter import filedialog
import tkinter.messagebox as msgbox


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


class Edit_Values(tkinter.Tk):
    def __init__(self, parent=ttk.Treeview, key_list=list, edit_title=str, values_disabled=None, path_keys=None, focus_force=None, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.parent = parent
        self.title(edit_title)
        self.minsize(width=350, height=28 * (len(key_list) + 1))

        self.selected_item = self.parent.selection()[0]
        self.record_value = [str(value) for value in self.parent.item(self.selected_item)['values']]
        self.entry_dict = {}
        for key_index in range(len(key_list)):
            ttk.Label(self, text=key_list[key_index], justify='left').grid(column=0, row=key_index, padx=(5), pady=(5, 0))
            entry = ttk.Entry(self, width=50, justify='center')
            entry_column_span = 3
            if not path_keys == None:
                if key_list[key_index] in path_keys:
                    entry_column_span = 2
                    entry.grid(column=1, row=key_index, sticky='nesw', columnspan=entry_column_span, padx=(5), pady=(5, 0))
                    browse_button = tkinter.Button(self, text='...', width=3, command=self.__browse_files)
                    browse_button.grid(column=3, row=key_index, padx=(5), pady=(5, 0))
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
    

    def __click_button_save(self, event):
        logger.debug('Button save')
        new_record = []
        for entry in self.entry_dict.values():
            new_record.append(entry.get())
        for i in range(len(new_record)):
            if not self.record_value[i] == new_record[i]:
                self.parent.item(self.selected_item, values=new_record)
        logger.debug(f'Button save {new_record[1]}')
        self.destroy()


    def __browse_files(self):
        logger.debug('Browser files')
        file_path = filedialog.askdirectory(initialdir='/', title='Select the file path')
        logger.debug('File path')

class Main_Frame(tkinter.Frame):
    def __init__(self, config=file_mover_backup.Configuration_Values, *args, **kwargs) -> None:
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
    def __init__(self, config=file_mover_backup.Configuration_Values, *args, **kwargs) -> None:
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.config = config
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

class Edit_Month(tkinter.Tk):
    def __init__(self, parent=ttk.Frame, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.parent = parent
        self.title('Edit month description')
        self.minsize(width=350, height=100)
        logger.debug(parent)
        self.selected_item = self.parent.selection()[0]
        self.record_value = [str(value) for value in self.parent.item(self.selected_item)['values']]

        ttk.Label(self, text='Month number', justify='left').grid(column=0, row=0, padx=(5), pady=(5, 0))
        self.gui_month_num = ttk.Entry(self, width=50, justify='center')
        self.gui_month_num.grid(column=1, row=0, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
        self.gui_month_num.insert(tkinter.END, self.record_value[0])
        self.gui_month_num.configure(state='disabled')

        ttk.Label(self, text='Month Description', justify='left').grid(column=0, row=1, padx=(5), pady=(5, 0))
        self.gui_month_descr = ttk.Entry(self, width=50, justify='center')
        self.gui_month_descr.grid(column=1, row=1, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
        self.gui_month_descr.insert(tkinter.END, self.record_value[1])
        self.gui_month_descr.focus_force()
        self.gui_month_descr.select_clear()
        self.gui_month_descr.select_range(0, tkinter.END)
        self.bind("<Return>", self.__click_button_save)
        self.bind("<Escape>", lambda *ignore: self.destroy())


        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=2, padx=(5), pady=(5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=2, padx=(5), pady=(5))          


    def __click_button_cancel(self):
        logger.debug('Button cancel')
        self.destroy()
    

    def __click_button_save(self, event):
        self.record_value[1] = self.gui_month_descr.get()
        self.parent.item(self.selected_item, values=self.record_value)
        logger.debug(f'Button save {self.record_value[1]}')
        self.destroy()
        return

class Config_Window(tkinter.Tk):
    def __init__(self, config=file_mover_backup.Configuration_Values, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.config = config
        self.title('Configuration')
        self.minsize(width=400, height=300)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tab_control = ttk.Notebook(self)

        # Tab Main
        tab_main = Main_Frame(self.config)
        tab_file_settings = File_Settings(self.config)
        self.tab_control.add(tab_main, text='Main')
        self.tab_control.add(tab_file_settings, text='File Settings')
        self.tab_control.grid(column=0, 
                        row=0, 
                        columnspan=4, 
                        sticky='nesw', 
                        padx=(5, 0), 
                        pady=(5, 0))

        # Tab File Settings
        tab_file_settings.columnconfigure(1, weight=1)
        tab_file_settings.rowconfigure(0, weight=1)
        


        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=1, padx=(5), pady=(0, 5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=1, padx=(5), pady=(0, 5))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)
        self.month_edit = None


    def __click_button_cancel(self):
        logger.debug('Cancel click')
        self.__on_window_close()


    def __click_button_save(self):
        logger.debug('Save click')


    def __on_window_close(self):
        logger.debug('On close click')
        self.destroy()


    def __validade_values(self, value=str):
        if value.isnumeric() or value == '':
            logger.debug(f'{value} is true')
            return True
        else:
            logger.debug(f'{value} is false')
            return False
    

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
        return file_mover_backup.Configuration_Values(int(config['wait_time_min']),
                int(config['files_per_cicle']),
                config['month_name'], 
                [file_mover_backup.Move_Settings(normpath(item['source']), 
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
    window = Config_Window(config)
    window.mainloop()