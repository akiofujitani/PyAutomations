from webbrowser import open as web_open
import tkinter
import tkinter.messagebox


class Main_App(tkinter.Tk):
    # Build main GUI
    def __init__(self, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title('Middleware Job Visualizer')
        self.geometry('400x300')

        self.text_label = tkinter.Label(self, text='Insira o número do pedido no campo abaixo e pressione o botão "OK"', justify='left', wraplength=350, font=('Arial', 10))
        self.text_label.place(x=15, y=10, height=40)

        self.input_text = tkinter.Entry(self, justify='center', font=('Arial', 10))
        self.input_text.place(x=15, y=50, width=300, height=25)
        self.input_text.focus()

        self.bind('<Return>', self.func)
        self.ok_button = tkinter.Button(self, text='OK', command=self.click_button_ok)
        self.ok_button.place(x=320, y=50, width=70, height=25)   


    # Button ok click action
    def click_button_ok(self):
        self.job_number = self.input_text.get()
        try:
            int(self.job_number)
            web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(self.job_number)}')
            self.input_text.delete(0, tkinter.END)
        except Exception as error:
            print(error)
            tkinter.messagebox.showerror('Middleware Job Visualizer', 'Somente números são aceitos, favor digitar novamente')


    # Action for "Enter" press keyboard event
    def func(self, event):
        self.click_button_ok()
        print(f'Enter hit {event}')


if __name__ == '__main__':
    window = Main_App()
    window.mainloop()
