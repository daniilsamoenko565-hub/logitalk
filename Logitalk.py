import threading
from socket import *
from customtkinter import *
from random import choice

LANGUAGES = {
    "uk": {
        "title": "Чат-додаток",
        "menu": {
            "change_name": "Змінити імʼя:",
            "placeholder": "Нове імʼя",
            "save": "Зберегти",
            "theme": "Тема:",
            "language": "Мова:"
        },
        "chat": {
            "placeholder": "Напишіть повідомлення...",
            "joined": " приєднався(лась) до чату!",
            "name_changed": "Користувач {} змінив нік на {}",
            "connection_error": "Не вдалося підключитися до сервера: {}",
            "image_sent": " надіслав(ла) зображення: {}"
        },
        "themes": {
            "dark": "Темна",
            "light": "Світла",
            "purple": "Фіолетова",
            "green": "Зелена",
            "ocean": "Океан"
        },
        "languages": {
            "uk": "Українська",
            "en": "Англійська"
        }
    },
    "en": {
        "title": "Chat Application",
        "menu": {
            "change_name": "Change name:",
            "placeholder": "New name",
            "save": "Save",
            "theme": "Theme:",
            "language": "Language:"
        },
        "chat": {
            "placeholder": "Write a message...",
            "joined": " has joined the chat!",
            "name_changed": "User {} changed nickname to {}",
            "connection_error": "Failed to connect to server: {}",
            "image_sent": " sent an image: {}"
        },
        "themes": {
            "dark": "Dark",
            "light": "Light",
            "purple": "Purple",
            "green": "Green",
            "ocean": "Ocean"
        },
        "languages": {
            "uk": "Ukrainian",
            "en": "English"
        }
    }
}

THEME_COLORS = {
    "dark": {
        "main": "#2b2b2b",
        "secondary": "#3a3a3a",
        "text": "#e0e0e0",
        "button": "#FF8C00",
        "button_hover": "#FF6B00",
        "entry_bg": "#3a3a3a",
        "entry_fg": "#ffffff"
    },
    "light": {
        "main": "#ffffff",
        "secondary": "#e0e0e0",
        "text": "#000000",
        "button": "#1E90FF",
        "button_hover": "#187BCD",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000"
    },
    "purple": {
        "main": "#2a1a3a",
        "secondary": "#3a2a4a",
        "text": "#e0d0f0",
        "button": "#9b59b6",
        "button_hover": "#8e44ad",
        "entry_bg": "#3a2a4a",
        "entry_fg": "#ffffff"
    },
    "green": {
        "main": "#1a3a2a",
        "secondary": "#2a4a3a",
        "text": "#d0f0e0",
        "button": "#2ecc71",
        "button_hover": "#27ae60",
        "entry_bg": "#2a4a3a",
        "entry_fg": "#ffffff"
    },
    "ocean": {
        "main": "#1a2a3a",
        "secondary": "#2a3a4a",
        "text": "#d0e0f0",
        "button": "#3498db",
        "button_hover": "#2980b9",
        "entry_bg": "#2a3a4a",
        "entry_fg": "#ffffff"
    }
}

adjectives = [
    "Швидкий", "Темний", "Легкий", "Сильний", "Вогняний", "Холодний", "Яскравий", "Мудрий", "Злий", "Добрий",
    "Глибокий", "Кольоровий", "Тихий", "Шалений", "Летючий", "Срібний", "Золотий", "Старий", "Новий", "Веселий",
    "Сумний", "Твердий", "М'який", "Різкий", "Блискучий", "Темпераментний", "Мрійливий", "Солодкий", "Гіркий", "Сірий",
    "Казковий", "Лісовий", "Морський", "Небесний", "Прозорий", "Буйний", "Легковажний", "Зухвалий", "Спокійний",
    "Вірний",
    "Броньований", "Пряний", "Чистий", "Могутній", "Легендарний", "Потаємний", "Стриманий", "Неочікуваний",
    "Безстрашний", "Величний"
]

nouns = [
    "Дракон", "Лев", "Вовк", "Вогонь", "Ліс", "Моряк", "Шторм", "Меч", "Маг", "Лицар",
    "Фенікс", "Тигр", "Яструб", "Грім", "Місяць", "Зірка", "Хижак", "Рицар", "Кіт", "Ворон",
    "Мороз", "Буревій", "Гроза", "Вітрило", "Кристал", "Чарівник", "Борець", "Рейнджер", "Король", "Принц",
    "Самурай", "Ніндзя", "Орк", "Ельф", "Гоблін", "Гладіатор", "Гігант", "Тролль", "Кентавр", "Русалка",
    "Паладин", "Берсерк", "Сокол", "Орел", "Лицарка", "Привид", "Чаклун", "Ангел", "Демон", "Вартовий"
]


class MainWindow(CTk):
    def __init__(self):
        super().__init__()

        self.current_language = "uk"
        self.current_theme = "dark"

        self.init_ui()

        self.connect_to_server()

    def init_ui(self):
        self.title(LANGUAGES[self.current_language]["title"])
        self.geometry('500x350')

        self.font_main = ("Arial", 12)
        self.font_bold = ("Arial", 12, "bold")
        self.font_labels = ("Arial", 14, "underline")

        self.set_theme(self.current_theme)

        self.label = None
        self.theme_label = None
        self.language_label = None
        self.theme_option = None
        self.language_option = None

        self.menu_frame = CTkFrame(self,
                                   width=30,
                                   height=300,
                                   fg_color=THEME_COLORS[self.current_theme]["secondary"],
                                   corner_radius=0)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)

        self.is_show_menu = False
        self.speed_animate_menu = -5

        self.btn = CTkButton(self,
                             text='☰',
                             command=self.toggle_show_menu,
                             width=30,
                             height=30,
                             font=self.font_bold,
                             fg_color="transparent",
                             hover_color=THEME_COLORS[self.current_theme]["button_hover"])
        self.btn.place(x=5, y=5)

        self.chat_field = CTkTextbox(self,
                                     font=self.font_main,
                                     state='disabled',
                                     wrap='word',
                                     fg_color=THEME_COLORS[self.current_theme]["main"],
                                     text_color=THEME_COLORS[self.current_theme]["text"])
        self.chat_field.place(x=0, y=0)

        self.message_entry = CTkEntry(self,
                                      placeholder_text=LANGUAGES[self.current_language]["chat"]["placeholder"],
                                      height=40,
                                      font=self.font_main,
                                      border_width=2,
                                      corner_radius=10,
                                      fg_color=THEME_COLORS[self.current_theme]["entry_bg"],
                                      text_color=THEME_COLORS[self.current_theme]["entry_fg"])
        self.message_entry.place(x=0, y=0)

        self.send_button = CTkButton(self,
                                     text='➤',
                                     width=50,
                                     height=40,
                                     command=self.send_message,
                                     font=self.font_bold,
                                     corner_radius=10,
                                     fg_color=THEME_COLORS[self.current_theme]["button"],
                                     hover_color=THEME_COLORS[self.current_theme]["button_hover"])
        self.send_button.place(x=0, y=0)

        self.adaptive_ui()

    def connect_to_server(self):
        self.username = choice(adjectives) + ' ' + choice(nouns)
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 8080))
            hello = f"TEXT@{self.username}@[СИСТЕМА] {self.username}{LANGUAGES[self.current_language]['chat']['joined']}\n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(LANGUAGES[self.current_language]["chat"]["connection_error"].format(e))

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.btn.configure(text='☰')
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.btn.configure(text='✕')
            self.show_menu()

            self.label = CTkLabel(self.menu_frame,
                                  text=LANGUAGES[self.current_language]["menu"]["change_name"],
                                  font=self.font_labels,
                                  text_color=THEME_COLORS[self.current_theme]["text"])
            self.label.pack(pady=20)

            self.entry = CTkEntry(self.menu_frame,
                                  font=self.font_main,
                                  placeholder_text=LANGUAGES[self.current_language]["menu"]["placeholder"],
                                  width=150,
                                  fg_color=THEME_COLORS[self.current_theme]["entry_bg"],
                                  text_color=THEME_COLORS[self.current_theme]["entry_fg"])
            self.entry.pack(pady=10)

            self.saveNameBtn = CTkButton(self.menu_frame,
                                         text=LANGUAGES[self.current_language]["menu"]["save"],
                                         command=self.saveName,
                                         font=self.font_main,
                                         corner_radius=8,
                                         fg_color=THEME_COLORS[self.current_theme]["button"],
                                         hover_color=THEME_COLORS[self.current_theme]["button_hover"])
            self.saveNameBtn.pack(pady=10)

            self.theme_label = CTkLabel(self.menu_frame,
                                        text=LANGUAGES[self.current_language]["menu"]["theme"],
                                        font=self.font_labels,
                                        text_color=THEME_COLORS[self.current_theme]["text"])
            self.theme_label.pack(pady=(20, 5))

            self.theme_option = CTkOptionMenu(self.menu_frame,
                                              values=[LANGUAGES[self.current_language]["themes"]["dark"],
                                                      LANGUAGES[self.current_language]["themes"]["light"],
                                                      LANGUAGES[self.current_language]["themes"]["purple"],
                                                      LANGUAGES[self.current_language]["themes"]["green"],
                                                      LANGUAGES[self.current_language]["themes"]["ocean"]],
                                              command=self.change_theme,
                                              width=150,
                                              fg_color=THEME_COLORS[self.current_theme]["button"],
                                              button_color=THEME_COLORS[self.current_theme]["button"],
                                              button_hover_color=THEME_COLORS[self.current_theme]["button_hover"])
            self.theme_option.pack(pady=5)
            self.theme_option.set(LANGUAGES[self.current_language]["themes"][self.current_theme])

            self.language_label = CTkLabel(self.menu_frame,
                                           text=LANGUAGES[self.current_language]["menu"]["language"],
                                           font=self.font_labels,
                                           text_color=THEME_COLORS[self.current_theme]["text"])
            self.language_label.pack(pady=(20, 5))

            self.language_option = CTkOptionMenu(self.menu_frame,
                                                 values=[LANGUAGES[self.current_language]["languages"]["uk"],
                                                         LANGUAGES[self.current_language]["languages"]["en"]],
                                                 command=self.change_language,
                                                 width=150,
                                                 fg_color=THEME_COLORS[self.current_theme]["button"],
                                                 button_color=THEME_COLORS[self.current_theme]["button"],
                                                 button_hover_color=THEME_COLORS[self.current_theme]["button_hover"])
            self.language_option.pack(pady=5)
            self.language_option.set(LANGUAGES[self.current_language]["languages"][self.current_language])

    def saveName(self):
        if self.entry.get().strip():
            message = LANGUAGES[self.current_language]["chat"]["name_changed"].format(self.username, self.entry.get())
            self.add_message(message)
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
            self.username = self.entry.get()

    def change_theme(self, choice):

        for theme_key, theme_name in LANGUAGES[self.current_language]["themes"].items():
            if theme_name == choice:
                self.current_theme = theme_key
                break

        self.set_theme(self.current_theme)
        self.update_ui_theme()

    def change_language(self, choice):
        lang_key = "uk" if choice == LANGUAGES[self.current_language]["languages"]["uk"] else "en"
        if lang_key != self.current_language:
            self.current_language = lang_key
            self.update_ui_texts()

    def set_theme(self, theme):
        if theme == "dark":
            set_appearance_mode("Dark")
        elif theme == "light":
            set_appearance_mode("Light")
        else:

            set_appearance_mode("System")


        self.configure(bg=THEME_COLORS[self.current_theme]["main"])

    def update_ui_theme(self):

        colors = THEME_COLORS[self.current_theme]


        self.menu_frame.configure(fg_color=colors["secondary"])
        self.btn.configure(hover_color=colors["button_hover"])
        self.chat_field.configure(fg_color=colors["main"], text_color=colors["text"])
        self.message_entry.configure(fg_color=colors["entry_bg"], text_color=colors["entry_fg"])
        self.send_button.configure(fg_color=colors["button"], hover_color=colors["button_hover"])

        if self.is_show_menu:
            if self.label:
                self.label.configure(text_color=colors["text"])
            if self.entry:
                self.entry.configure(fg_color=colors["entry_bg"], text_color=colors["entry_fg"])
            if self.saveNameBtn:
                self.saveNameBtn.configure(fg_color=colors["button"], hover_color=colors["button_hover"])
            if self.theme_label:
                self.theme_label.configure(text_color=colors["text"])
            if self.theme_option:
                self.theme_option.configure(fg_color=colors["button"],
                                            button_color=colors["button"],
                                            button_hover_color=colors["button_hover"])
            if self.language_label:
                self.language_label.configure(text_color=colors["text"])
            if self.language_option:
                self.language_option.configure(fg_color=colors["button"],
                                               button_color=colors["button"],
                                               button_hover_color=colors["button_hover"])

    def update_ui_texts(self):
        self.title(LANGUAGES[self.current_language]["title"])
        self.message_entry.configure(placeholder_text=LANGUAGES[self.current_language]["chat"]["placeholder"])

        if self.is_show_menu:
            if self.label:
                self.label.configure(text=LANGUAGES[self.current_language]["menu"]["change_name"])
            if self.entry:
                self.entry.configure(placeholder_text=LANGUAGES[self.current_language]["menu"]["placeholder"])
            if self.saveNameBtn:
                self.saveNameBtn.configure(text=LANGUAGES[self.current_language]["menu"]["save"])
            if self.theme_label:
                self.theme_label.configure(text=LANGUAGES[self.current_language]["menu"]["theme"])
            if self.language_label:
                self.language_label.configure(text=LANGUAGES[self.current_language]["menu"]["language"])

            self.theme_option.configure(values=[LANGUAGES[self.current_language]["themes"]["dark"],
                                                LANGUAGES[self.current_language]["themes"]["light"],
                                                LANGUAGES[self.current_language]["themes"]["purple"],
                                                LANGUAGES[self.current_language]["themes"]["green"],
                                                LANGUAGES[self.current_language]["themes"]["ocean"]])
            self.theme_option.set(LANGUAGES[self.current_language]["themes"][self.current_theme])

            self.language_option.configure(values=[LANGUAGES[self.current_language]["languages"]["uk"],
                                                   LANGUAGES[self.current_language]["languages"]["en"]])
            self.language_option.set(LANGUAGES[self.current_language]["languages"][self.current_language])

    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)
        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.label:
                self.label.destroy()
                self.label = None
            if self.entry:
                self.entry.destroy()
                self.entry = None
            if self.saveNameBtn:
                self.saveNameBtn.destroy()
                self.saveNameBtn = None
            if self.theme_label:
                self.theme_label.destroy()
                self.theme_label = None
            if self.theme_option:
                self.theme_option.destroy()
                self.theme_option = None
            if self.language_label:
                self.language_label.destroy()
                self.language_label = None
            if self.language_option:
                self.language_option.destroy()
                self.language_option = None

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width(),
                                  height=self.winfo_height() - 50)
        self.send_button.place(x=self.winfo_width() - 55, y=self.winfo_height() - 45)
        self.message_entry.place(x=self.menu_frame.winfo_width() + 5, y=self.send_button.winfo_y())
        self.message_entry.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width() - 10)

        self.after(50, self.adaptive_ui)

    def add_message(self, text):
        self.chat_field.configure(state='normal')
        self.chat_field.insert(END, text + '\n')
        self.chat_field.configure(state='disabled')
        self.chat_field.see(END)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_entry.delete(0, END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]

        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                author = parts[1]
                filename = parts[2]
                self.add_message(f"{author}{LANGUAGES[self.current_language]['chat']['image_sent'].format(filename)}")
        else:
            self.add_message(line)


if __name__ == "__main__":
    win = MainWindow()
    win.mainloop()