from webbrowser import open as web_open
from queue import Queue
from os.path import join, abspath, normpath
from PIL import Image, ImageTk
from tkinter import Tk, Label, Menu, Entry, Button, WORD, END, Toplevel
import logger as log
import logging, sys
import tkinter.messagebox
import tkinter.scrolledtext


logger = logging.getLogger('middleware_job_visualizer')

class Main_App(Tk):
    # Build main GUI
    def __init__(self, log_queue=Queue, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        self.log_queue = log_queue
        self.title('Middleware Job Visualizer')
        self.minsize(width=500, height=400)
        try:
            self.icon_path = self.resource_path('./Icon/walrus.ico')
        except Exception:
            logger.error('Could not load icon')
        self.iconbitmap(self.icon_path)

        text_label = Label(self, text='Insira o número do pedido no campo abaixo e pressione o botão "OK"', justify='left', font=('Arial', 10))
        text_label.grid(sticky='nesw', padx=(3), column=0, row=0, columnspan=2)
        self.grid_rowconfigure(0, minsize=50)
        self.grid_columnconfigure(0, weight=1, minsize=100)
        self.grid_rowconfigure(2, weight=1)

        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Sair   ', command=self.__quit_window)
        menu_bar.add_cascade(label='Arquivo ', menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Sobre   ', command=self.__about_command)
        menu_bar.add_cascade(label='Ajuda   ', menu=help_menu)

        self.config(menu=menu_bar)


        self.input_text = Entry(self, justify='center', font=('Arial', 10))
        self.input_text.grid(sticky='nesw', padx=(3), pady=(3), column=0, row=1)
        self.input_text.focus()

        self.bind('<Return>', self.func)
        ok_button = Button(self, text='OK', command=self.click_button_ok, width=15) 
        ok_button.grid(column=1, row=1, padx=(3), pady=(3), sticky='nesw')

        self.scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        self.scrolled_text.configure(wrap=WORD, font=('Arial', 9))
        self.scrolled_text.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=(3), pady=(3))
        self.protocol('WM_DELETE_WINDOW', self.__quit_window)
        self.after(100, self.__pull_log_queue)



    def __display(self, message):
        self.scrolled_text.configure(state='normal')
        line_count = int(float(self.scrolled_text.index('end')))
        if line_count > 300:
            self.scrolled_text.delete('1.0', str("{:0.1f}".format(line_count - 299)))
        self.scrolled_text.insert(END, f'{message}\n')
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview(END)
    

    def __pull_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get(block=False)
            self.__display(message)
        self.after(100, self.__pull_log_queue)

    # Button ok click action
    def click_button_ok(self):
        self.job_number = self.input_text.get()
        try:
            int(self.job_number)
            web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(self.job_number)}')
            self.input_text.delete(0, END)
            logger.info(f'Job {self.job_number}')
        except Exception as error:
            logger.error(error)
            tkinter.messagebox.showerror('Middleware Job Visualizer', 'Somente números são aceitos, favor digitar novamente')

    # Action for "Enter" press keyboard event
    def func(self, event):
        self.click_button_ok()
        logger.debug(f'Event {event}')
    

    def resource_path(self, relavite_path=str):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = abspath('.')
        return normpath(join(base_path, relavite_path))


    def __quit_window(self):
        if tkinter.messagebox.askokcancel('Sair', 'Tem certeza que deseja sair?'):
            self.destroy()


    def __about_command(self):
        logger.info('About clicked')
        self.about = About('Sobre', '''
        Nome do aplicativo: Middleware job visualizer
        Versão: 0.10.00
        Desenvolvido por: Akio Fujitani
        e-mail: akiofujitani@gmail.com
        ''', self.resource_path('./Icon/Bedo.jpg'), self.icon_path)
        logger.debug(f'About {self.grab_status}')


class About(Toplevel):
    def __init__(self, title=str, label_values=str, image_file=str, icon_path=str, *args, **kwargs) -> None:
        Toplevel.__init__(self, *args, **kwargs)
        self.last_grab = self.grab_current()
        self.grab_set()
        self.geometry('450x400')
        self.title(title)
        self.resizable(width=False, height=False)
        self.icon_path = icon_path
        self.iconbitmap(self.icon_path)
        image = Image.open(image_file)
        image_tk = ImageTk.PhotoImage(image=image)
        image_label = Label(self, image=image_tk, justify='center')
        image_label.image = image_tk
        image_label.grid(column=0, row=0, columnspan=2, padx=(10), pady=(5, 0))

        text_label = Label(self, text=label_values, justify='left')
        text_label.grid(column=0, row=1, rowspan=2, sticky='nw', padx=(5), pady=(5, 0))

        ok_button = Button(self, text='Ok', width=15, command=self.__pressed_ok_button)
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


if __name__ == '__main__':
    log_queue = Queue()
    logger = logging.getLogger()
    log.logger_setup(logger, log_queue)
    
    window = Main_App(log_queue)
    window.mainloop()
