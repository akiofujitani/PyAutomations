import tkinter
import tkinter.ttk
import tkinter.scrolledtext

    

if __name__ == '__main__':
    # Create window
    window = tkinter.Tk()

    window.title('Test fuck the name')
    window.geometry('500x400')

    #Create label with text

    label = tkinter.Label(window, text='Please enter your name and click in the Button OK', font=('Arial', 10))
    label.grid(column=0, row=0)

    # Create text input field

    text = tkinter.Entry(window, width=30)
    text.grid(column=0, row=1)
    text.focus()

    label_2 = tkinter.Label(window, font=('Arial Bold', 20))
    label_2.grid(column=0, row=3)

    # Create text input field disabled

    text_2 = tkinter.Entry(window,width=30, state='disabled')
    text_2.grid(column=0, row=4)

    # Button click action

    def click_button_ok():
        text_value = f'Fuck you {text.get()}'
        label_2.configure(text=text_value)


    def combo_box_get():
        text_value = f'Value from combobox {combo_box.get()}'
        print(text_value)
        text_2.configure(state='normal')
        text_2.delete(0, tkinter.END)
        text_2.insert(0, text_value)
        text_2.configure(state='disabled')


    # Create button

    Button = tkinter.Button(window, text='Ok', command=click_button_ok, width=5)
    Button.grid(column=1, row=1)

    Button_2 = tkinter.Button(window, text='Second Button', command=combo_box_get, bg='red', fg='white')
    Button_2.grid(column=1, row=2)

    # Create combobox

    combo_box = tkinter.ttk.Combobox(window, width=10)
    combo_box['values'] = ('banana', 'apple', 'orange', 'strawberry', 'pineapple', 'tomato')
    combo_box.current(5)
    combo_box.grid(column=1, row=3)

    # Check button

    check_button_state = tkinter.BooleanVar()
    check_button_state.set(False)
    check_button = tkinter.ttk.Checkbutton(window, text='Choose', variable=check_button_state)

    check_button.grid(column=1, row=4)


    # Radio Button

    radio_selected = tkinter.IntVar()

    def radio_clicked():
        print(radio_selected.get() + 1)

    radio_button = {}
    for i in range(4):
        radio_button[f'radio_{i}'] = tkinter.ttk.Radiobutton(window, text=f'Radio {i + 1}', value=i, variable=radio_selected, command=radio_clicked)
        radio_button[f'radio_{i}'].grid(column=2, row=i)

    # ScrolledText

    scroll_text = tkinter.scrolledtext.ScrolledText(window, width=40, height=15)
    scroll_text.grid(column=0, row=5)
    scroll_text.insert(tkinter.INSERT, 'Your text goes here')
    scroll_text.delete(1.0, tkinter.END) # clear scroll text field contents.

    # Message box

    import tkinter.messagebox

    def msgbox_click():
        tkinter.messagebox.showinfo('Message box', 'You did shit!!!')

    msgbox_button = tkinter.Button(window, text='Msgbox', command=msgbox_click)
    msgbox_button.grid(column=2, row=5)
    

    # Run GUI

    window.mainloop()