import tkinter
import tkinter.ttk
import tkinter.scrolledtext
import pystray
from PIL import Image
from os.path import abspath




if __name__ == '__main__':
    # Create window
    window = tkinter.Tk()

    window.title('Test fuck the name')
    window.geometry('700x400')


    def new_command():
        print('Menu New clicked')


    def open_command():
            print('Menu New clicked')
    

    def save_command():
        print('Menu New clicked')


    def help_index_command():
        print('Menu New clicked')


    def about_command():
        print('Menu New clicked')


    menu_bar = tkinter.Menu(window)
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='New', command=new_command)
    file_menu.add_command(label='Open', command=open_command)
    file_menu.add_command(label='Save', command=save_command)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=window.quit)
    menu_bar.add_cascade(label='File', menu=file_menu)

    help_menu = tkinter.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label='Help Index', command=help_index_command)
    help_menu.add_command(label='About', command=about_command)
    menu_bar.add_cascade(label='Help', menu=help_menu)


    window.config(menu=menu_bar)

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

    text_2 = tkinter.Entry(window, width=30, state='disabled')
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

    Button_2 = tkinter.Button(window, text='Second Button', command=combo_box_get)
    Button_2.grid(column=1, row=2)
    Button_2.configure(bg='red', fg='white')

    # Create combobox

    combo_box = tkinter.ttk.Combobox(window, width=10)
    combo_box['values'] = ('banana', 'apple', 'orange', 'strawberry', 'pineapple', 'tomato')
    combo_box.current(5)
    combo_box.set('strawberry')
    combo_box.grid(column=1, row=3)

    # Check button

    check_button_state = tkinter.BooleanVar()
    check_button_state.set(False)
    check_button = tkinter.ttk.Checkbutton(window, text='Choose', variable=check_button_state)

    check_button.grid(column=1, row=4)


    # Radio Button

    radio_selected = tkinter.IntVar()
    radio_selected.set(2)

    def radio_clicked():
        print(radio_selected.get() + 1)

    radio_button = {}
    for i in range(4):
        radio_button[f'radio_{i}'] = tkinter.ttk.Radiobutton(window, text=f'Radio {i + 1}', value=i, variable=radio_selected, command=radio_clicked)
        radio_button[f'radio_{i}'].grid(column=2, row=i)


    radio_bool = tkinter.BooleanVar()
    radio_bool.set(False)

    def radio_bool_clicked():
        print(radio_bool.get())
    
    boolean_name = ('True', 'False')
    radio_bool_button = {}
    for i in range(len(boolean_name)):
        radio_bool_button[i] = tkinter.ttk.Radiobutton(window, text=boolean_name[i], value=eval(boolean_name[i]), variable=radio_bool, command=radio_bool_clicked)
        radio_bool_button[i].grid(column=3, row=i)
    

    # ScrolledText

    scroll_text = tkinter.scrolledtext.ScrolledText(window, width=40, height=15)
    scroll_text.grid(column=0, row=5)
    counter = 0
    for i in range(30):
        scroll_text.insert(tkinter.INSERT, f'{"{:02d}".format(i)}: Your text goes here\n')
        counter += 1
    # scroll_text.delete(1.0, tkinter.END) # clear scroll text field contents.
    num_lines = scroll_text.index('end')
    scroll_text_value = scroll_text.get('1.0', '2.0')
    scroll_text.delete('1.0', '5.0')
    print(scroll_text_value)

    list_box = tkinter.ttk.Treeview(window, columns=('lang', 'status', 'like'), show='headings')
    list_box.heading('lang', text='Language')
    list_box.heading('status', text='Status')
    list_box.heading('like', text='Like')
    list_box.insert('', tkinter.END, values=('Pearl', 'No', 'No'))
    list_box.grid(column=0, row=6, columnspan=3)

    # Message box

    import tkinter.messagebox

    def msgbox_click():
        tkinter.messagebox.showinfo('Message box', 'You did shit!!!')

    msgbox_button = tkinter.Button(window, text='Msgbox', command=msgbox_click)
    msgbox_button.grid(column=2, row=5)
    

    def quit_window(tray_icon):
        tray_icon.stop()
        window.destroy()
    

    def show_window(tray_icon):
        tray_icon.stop()
        window.after(150, window.deiconify)


    def __hide_window_to_tray():
        window.withdraw()
        icon_image = Image.open(abspath('./Icon/tiger.ico'))
        tray_menu = (pystray.MenuItem('Quit', lambda: quit_window), pystray.MenuItem('Show', lambda: show_window))
        tray_icon = pystray.Icon('Tkinter GUI', icon_image, 'System tray icon', tray_menu)
        tray_icon.run()


    hide_window_button = tkinter.Button(window, text='Hide window', width= 10, command=__hide_window_to_tray).grid(column=1, row=7)
    window.protocol('WM_DELETE_WINDOW', __hide_window_to_tray)

    # Run GUI

    window.mainloop()