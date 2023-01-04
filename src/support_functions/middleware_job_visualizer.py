from webbrowser import open as web_open
import tkinter
import tkinter.messagebox


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('Middleware Job Visualizer')
    window.geometry('400x300')

    text_label = tkinter.Label(window, text='Insira o número do pedido no campo abaixo e pressione o botão "OK"', justify='left', wraplength=350, font=('Arial', 10))
    text_label.place(x=15, y=10, height=40)

    input_text = tkinter.Entry(window, justify='center', font=('Arial', 10))
    input_text.place(x=15, y=50, width=300, height=25)
    input_text.focus()

    def click_button_ok():
        job_number = input_text.get()
        try:
            int(job_number)
            web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(job_number)}')
            input_text.delete(0, tkinter.END)
        except Exception as error:
            print(error)
            tkinter.messagebox.showerror('Middleware Job Visualizer', 'Somente números são aceitos, favor digitar novamente')


    def func(event):
        click_button_ok()
        print(f'Enter hit {event}')

    window.bind('<Return>', func)
    ok_button = tkinter.Button(window, text='OK', command=click_button_ok)
    ok_button.place(x=320, y=50, width=70, height=25)     



    window.mainloop()
    # job_number = 2677872

    # web_open(f'http://lab.optview.com.br/impressao.laboratorio.ws.php?job={str(job_number)}')