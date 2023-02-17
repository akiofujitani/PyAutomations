from webbrowser import open as web_open
import logger as log
import tkinter, logging
import tkinter.messagebox
import tkinter.scrolledtext

logger = logging.getLogger('middleware_job_visualizer')

class Main_App(tkinter.Tk):
    # Build main GUI
    def __init__(self, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title('Middleware Job Visualizer')
        self.minsize(width=500, height=400)

        self.text_label = tkinter.Label(self, text='Insira o número do pedido no campo abaixo e pressione o botão "OK"', justify='left', font=('Arial', 10))
        self.text_label.grid(sticky='nesw', padx=(3), column=0, row=0, columnspan=2)
        self.grid_rowconfigure(0, minsize=50)
        self.grid_columnconfigure(0, weight=1, minsize=100)
        self.grid_rowconfigure(2, weight=1)

        self.input_text = tkinter.Entry(self, justify='center', font=('Arial', 10))
        self.input_text.grid(sticky='nesw', padx=(3), pady=(3), column=0, row=1)
        self.input_text.focus()

        self.bind('<Return>', self.func)
        self.ok_button = tkinter.Button(self, text='OK', command=self.click_button_ok, width=15) 
        self.ok_button.grid(column=1, row=1, padx=(3), pady=(3), sticky='nesw')

        scrolled_text = tkinter.scrolledtext.ScrolledText(self, state='disabled')
        scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        scrolled_text.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=(3), pady=(3))
        text_handler = log.TextHandler(scrolled_text)

        logger.addHanlder(text_handler)

    # Button ok click action
    def click_button_ok(self):
        self.job_number = self.input_text.get()
        try:
            int(self.job_number)
            web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(self.job_number)}')
            self.input_text.delete(0, tkinter.END)
            logger.info(f'Job {self.job_number}')
        except Exception as error:
            logger.error(error)
            tkinter.messagebox.showerror('Middleware Job Visualizer', 'Somente números são aceitos, favor digitar novamente')

    # Action for "Enter" press keyboard event
    def func(self, event):
        self.click_button_ok()
        logger.debug(f'Event {event}')


if __name__ == '__main__':
    logger = log.logger(logging.getLogger())
    window = Main_App()
    window.mainloop()
