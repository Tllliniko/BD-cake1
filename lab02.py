import os
import subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import configparser
from lab03 import open_browser, create_gallery_data  # Импортируем новые функции
def folder():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        load_BD()
def close_program():
    form1.destroy()
def load_BD():
    config = configparser.ConfigParser()
    ini_path = os.path.join(folder_selected, 'index.ini')
    if not os.path.exists(ini_path):
        messagebox.showerror("Ошибка", "INI файл не найден в выбранной папке.")
        return
    try:
        with open(ini_path, 'r', encoding='utf-8') as f:
            config.read_file(f)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать INI файл: {e}")
        return
    # Удаляем старые метки если они есть
    for widget in frame1.winfo_children():
        widget.destroy()
    for section in config.sections():
        cake_name = section
        cake_label = Label(frame1, text=cake_name, cursor="hand2", bg="#FFB6C1")
        cake_label.pack(pady=5)
        cake_label.bind("<Enter>", lambda event, label=cake_label: label.config(fg="blue"))
        cake_label.bind("<Leave>", lambda event, label=cake_label: label.config(fg="black"))
        cake_label.bind("<Button-1>", lambda event, name=cake_name: show_cake(name))
def show_cake(cake_name):
    global current_image
    config = configparser.ConfigParser()
    ini_path = os.path.join(folder_selected, 'index.ini')
    try:
        with open(ini_path, 'r', encoding='utf-8') as f:
            config.read_file(f)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать INI файл: {e}")
        return
    current_image = os.path.join(folder_selected, config[cake_name]['image'])
    info_path = os.path.join(folder_selected, config[cake_name]['info'])
    display_image()
    try:
        with open(info_path, 'r', encoding='utf-8') as f: # Load and display description
            description = f.read()
        text_description.config(state=NORMAL)
        text_description.delete('1.0', END)
        text_description.insert(END, description)
        text_description.config(state=DISABLED)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить описание: {e}")
def display_image():
    try:
        img = PhotoImage(file=current_image)        # Load and display image
        img = img.subsample(int(img.width() / frame2.winfo_width()), int(img.height() / frame2.winfo_height()))
        label_image.config(image=img)
        label_image.image = img
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")
def on_resize(event):
    if current_image:
        display_image()
def show_menu(event):
    menu.post(event.x_root, event.y_root)
def show_info_about():
    messagebox.showinfo("О программе", 'Программа визуализации файловой базы данных: "РЕЦЕПТЫ ТОРТОВ" \n (c)Tolmachev, Moscow, 2024')
def show_help():
    help_window = Toplevel(form1)
    help_window.title("Справка")
    help_window.geometry("400x200")
    help_window.resizable(False, False)
    # Центрируем окно на экране
    screen_width = help_window.winfo_screenwidth()
    screen_height = help_window.winfo_screenheight()
    window_width = 400
    window_height = 150
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    help_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    help_label = Label(help_window, text="О программе...\nПрограмма визуализации файловой системы базы данных\nБаза данных представляет собой папку с файлами\nАвторские права:\n(c)Tolmachev, Moscow, 2024\n Отдельная благодарность родителям разработчика \nТолмачёвой Елене и Толмачёву Илье, они самые лучшие", justify=LEFT)
    help_label.pack(padx=10, pady=10)
def on_enter_label(event, label):
    label.config(bg="lightgrey")
def on_leave_label(event, label):
    label.config(bg="white")
def gallery():
    global gallery_folder
    gallery_folder = filedialog.askdirectory()
    if gallery_folder:
        show_gallery_window(gallery_folder)
def show_gallery_window(folder_path):
    gallery_window = Toplevel(form1)
    gallery_window.title("Галерея")
    gallery_window.geometry("400x250")
    gallery_window.resizable(False, False)
    screen_width = gallery_window.winfo_screenwidth()
    screen_height = gallery_window.winfo_screenheight()
    window_width = 350
    window_height = 80
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    gallery_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    Label(gallery_window, text=folder_path).grid(row=0, column=0, columnspan=3, pady=10, sticky=W)
    check_var = IntVar()
    check_button = Checkbutton(gallery_window, text="Открыть в браузере", variable=check_var)
    check_button.grid(row=1, column=0, padx=5, pady=3, sticky=W)

    button_create = Button(gallery_window, text="Создать галерею", command=lambda: load_gallery(folder_path, check_var.get()))
    button_create.grid(row=1, column=1, padx=5, pady=3)

    button_close = Button(gallery_window, text="Закрыть", command=gallery_window.destroy)
    button_close.grid(row=1, column=2, padx=5, pady=3)

def load_gallery(folder_path, open_in_browser):
    global folder_selected
    folder_selected = folder_path
    if open_in_browser:
        gallery_data = create_gallery_data(folder_path)
        open_browser(gallery_data)
    else:
        load_BD()

current_image = None
form1 = Tk()
form1.title('ТОРТЫ')
form1.config(background="white")

screen_width = form1.winfo_screenwidth()
screen_height = form1.winfo_screenheight()
window_width = 700
window_height = 540
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
form1.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

top_frame = Frame(form1, bg="white")
top_frame.pack(side=TOP, anchor="w", padx=5, pady=5)
_frame = Frame(form1, bg="white")
_frame.pack(side=BOTTOM, anchor="w", padx=5, pady=5)
label_fondd = Label(_frame, text="F1-справка F2-Добавить F3-Удалить F4-Изменить F10-меню", font=("Arial", 12),bg="white")
label_fondd.pack(side=LEFT, padx=10)

label_fond = Label(top_frame, text="Фонд", font=("Arial", 12), cursor="hand2", bg="white")
label_fond.pack(side=LEFT, padx=10)
label_fond.bind("<Enter>", lambda event: on_enter_label(event, label_fond))
label_fond.bind("<Leave>", lambda event: on_leave_label(event, label_fond))

label_help = Label(top_frame, text="Справка", font=("Arial", 12), cursor="hand2", bg="white")
label_help.pack(side=LEFT, padx=10)
label_help.bind("<Enter>", lambda event: on_enter_label(event, label_help))
label_help.bind("<Leave>", lambda event: on_leave_label(event, label_help))

menu = Menu(form1, tearoff=0)
menu.add_command(label="Открыть папку", command=folder)
menu.add_command(label="Галерея", command=gallery)
menu.add_command(label="Закрыть программу", command=close_program)
label_fond.bind("<Button-1>", show_menu)

help_menu = Menu(form1, tearoff=0)
help_menu.add_command(label="Справка", command=show_help)
help_menu.add_command(label="О программе...", command=show_info_about)
label_help.bind("<Button-1>", lambda event: help_menu.post(event.x_root, event.y_root))

horizontal_paned_window = ttk.PanedWindow(form1, orient=HORIZONTAL)
horizontal_paned_window.pack(fill=BOTH, expand=True)
frame1 = Frame(horizontal_paned_window, bg="#FFB6C1", width=200)
horizontal_paned_window.add(frame1, weight=1)
vertical_paned_window = ttk.PanedWindow(horizontal_paned_window, orient=VERTICAL)
horizontal_paned_window.add(vertical_paned_window, weight=4)
frame2 = Frame(vertical_paned_window, bg="#FFFACD", width=470, height=200)
vertical_paned_window.add(frame2, weight=1)
frame3 = Frame(vertical_paned_window, bg="#E0FFFF", width=470, height=200)
vertical_paned_window.add(frame3, weight=1)
label_image = Label(frame2, bg="#FFFACD", height=28)
label_image.pack(expand=True, fill=BOTH)

text_description = Text(frame3, wrap=WORD, state=DISABLED, bg="#E0FFFF")
text_description.pack(expand=True, fill=BOTH)

frame2.bind("<Configure>", on_resize)
form1.mainloop()
