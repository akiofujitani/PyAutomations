import tkinter, json_config, file_mover_backup
from tkinter import ttk
import logger as log
from os.path import normpath
from time import sleep
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
    def __init__(self, values_list=list, key_list=list, edit_title=str, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.values_list = values_list
        self.title(edit_title)
        self.minsize(width=350, height=30 * (len(key_list) + 1))

        values = []
        for key_index in range(len(key_list)):
            ttk.Label(self, text=key_list[key_index], justify='left').grid(column=0, row=key_index, padx=(5), pady=(5, 0))
            entry = ttk.Entry(self, width=50, justify='center')
            entry.grid(column=1, row=key_index, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
            entry.insert(tkinter.END, str(values_list[key_index]))
            values.append(entry)

        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=key_index + 1, padx=(5), pady=(5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=key_index + 1, padx=(5), pady=(5))       
        

    def __click_button_cancel(self):
        logger.debug('Button cancel')
        self.destroy()
    

    def __click_button_save(self):
        logger.debug('Button save')


class Edit_Month(tkinter.Tk):
    def __init__(self, parent, month_number=int, month_descroption=str, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.month_number = month_number
        self.month_description = month_descroption
        self.title('Edit month description')
        self.minsize(width=350, height=100)

        ttk.Label(self, text='Month number', justify='left').grid(column=0, row=0, padx=(5), pady=(5, 0))
        self.gui_month_num = ttk.Entry(self, width=50, justify='center')
        self.gui_month_num.grid(column=1, row=0, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
        self.gui_month_num.insert(tkinter.END, month_number)
        self.gui_month_num.configure(state='disabled')

        ttk.Label(self, text='Month Description', justify='left').grid(column=0, row=1, padx=(5), pady=(5, 0))
        self.gui_month_descr = ttk.Entry(self, width=50, justify='center')
        self.gui_month_descr.grid(column=1, row=1, sticky='nesw', columnspan=3, padx=(5), pady=(5, 0))
        self.gui_month_descr.insert(tkinter.END, month_descroption)

        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=2, padx=(5), pady=(5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=2, padx=(5), pady=(5))          


    def __click_button_cancel(self):
        logger.debug('Button cancel')
        self.destroy()
    

    def __click_button_save(self):
        logger.debug('Button save')
        text = self.gui_month_descr.get()
        return text


class Config_Window(tkinter.Tk):
    def __init__(self, config=file_mover_backup.Configuration_Values, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.config = config
        self.title('Configuration')
        self.minsize(width=400, height=300)
        self.rowconfigure(0, weight=1, )
        self.columnconfigure(0, weight=1)

        self.tab_control = ttk.Notebook(self)
        tab_main = ttk.Frame(self.tab_control)
        tab_file_settings = ttk.Frame(self.tab_control)

        self.tab_control.add(tab_main, text='Main')
        self.tab_control.add(tab_file_settings, text='File Settings')
        self.tab_control.grid(column=0, row=0, columnspan=4, sticky='nesw', padx=(5), pady=(5))

        ttk.Label(tab_main, text='Wait time', justify='left').grid(column=0, row=0, padx=(5), pady=(5, 0))
        ttk.Label(tab_main, text='Files per cicle', justify='left').grid(column=0, row=1, padx=(5), pady=(5, 0))
        ttk.Label(tab_main, text='Months naming', justify='left').grid(column=0, row=2, padx=(5), pady=(5, 0))

        valid_command = (tab_main.register(self.__validade_values))
        wait_time_entry = ttk.Entry(tab_main, 
                        width=40, 
                        justify='center', 
                        validate='key', 
                        validatecommand=(valid_command, '%P'))
        wait_time_entry.grid(column=1, 
                        row=0, 
                        columnspan=2, 
                        sticky='nesw', 
                        padx=(5), 
                        pady=(5, 0))
        wait_time_entry.insert(tkinter.END, str(self.config.wait_time))
        files_per_cicle = ttk.Entry(tab_main, 
                        width=40, 
                        justify='center', 
                        validate='key', 
                        validatecommand=(valid_command, '%P'))
        files_per_cicle.grid(column=1,
                        row=1, 
                        columnspan=2, 
                        sticky='nesw', 
                        padx=(5), 
                        pady=(5, 0))
        files_per_cicle.insert(tkinter.END, str(self.config.file_per_cicle))
        month_columns = ('month_number' , 'month_description')
        self.months_naming_tree = ttk.Treeview(tab_main, columns=month_columns, show='headings')
        self.months_naming_tree.heading('month_number', text='Month Number')
        self.months_naming_tree.heading('month_description', text='Month Description')
        for i in range(len(config.month_name_list)):
            self.months_naming_tree.insert('', tkinter.END, values=(i + 1, config.month_name_list[i]))
        self.months_naming_tree.bind('<Double-1>', self.__tree_item_edit)
        self.months_naming_tree.grid(column=1, 
                        row=2, 
                        columnspan=2,
                        rowspan=int(len(config.month_name_list)) + 1, 
                        sticky='nesw', 
                        padx=(5), 
                        pady=(5, 0))
        self.months_naming_tree.columnconfigure(1, weight=1)
        self.months_naming_tree.columnconfigure(0, weight=1)
        tab_main.columnconfigure(1, weight=1)
        tab_main.rowconfigure(2, weight=1)

        cancel_button = tkinter.Button(self, text='Cancel', command=self.__click_button_cancel, width=15)
        cancel_button.grid(column=2, row=1, padx=(5), pady=(0, 5))    
        save_button = tkinter.Button(self, text='Save', command=self.__click_button_save, width=15)
        save_button.grid(column=3, row=1, padx=(5), pady=(0, 5))
        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)


    def __tree_item_selected(self, event):
        for selected_item in self.months_naming_tree.selection():
            item = self.months_naming_tree.item(selected_item)
            record = [str(value) for value in item['values']]
            # show a message
            msgbox.showinfo(title='Information', message=','.join(record))


    def __tree_item_edit(self, event):
        selected_item = self.months_naming_tree.selection()[0]
        record = [str(value) for value in self.months_naming_tree.item(selected_item)['values']]
        edited_values = Edit_Month(record[0], record[1])
        logger.debug('Double click')


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