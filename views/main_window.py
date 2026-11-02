import customtkinter as ctk
from tkinter import messagebox
from services.ai_translation import translate_text

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Translator")
        self.geometry("1500x850")
        self.resizable(False, False)

        self.languages = {
            "English": "en",
            "Hindi": "hi",
            "Telugu": "te",
            "Tamil": "ta",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Japanese": "ja",
            "Korean": "ko"
        }

        self.favorites_list = []

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

       
        sidebar = ctk.CTkFrame(main_frame, width=300)
        sidebar.pack(side="left", fill="y")

        logo = ctk.CTkLabel(
            sidebar,
            text="🌐 Translator App",
            font=("Segoe UI", 30, "bold")
        )
        logo.pack(pady=30)

        buttons = [
            ("🏠 Home", self.go_home),
            ("🌍 Translator", self.go_home),
            ("🕒 History", self.show_history),
            ("⭐ Favorites", self.show_favorites),
            ("🎤 Voice Translate", self.voice_message),
            ("⚙ Settings", self.open_settings),
            ("ℹ About", self.show_about)
        ]

        for text, cmd in buttons:
            ctk.CTkButton(
                sidebar,
                text=text,
                command=cmd,
                height=50,
                anchor="w",
                font=("Segoe UI", 18)
            ).pack(fill="x", padx=20, pady=8)

        quote = ctk.CTkTextbox(sidebar, width=250, height=180)
        quote.insert("1.0", "Daily Quote\n\n\"Language is the bridge between hearts.\"")
        quote.configure(state="disabled")
        quote.pack(side="bottom", pady=30)

        
        right = ctk.CTkFrame(main_frame)
        right.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            right,
            text="Hello Developer! 👋",
            font=("Segoe UI", 35, "bold")
        ).pack(anchor="w", padx=40, pady=(30, 5))

        ctk.CTkLabel(
            right,
            text="Choose languages and translate instantly",
            font=("Segoe UI", 18)
        ).pack(anchor="w", padx=40)

        
        lang_frame = ctk.CTkFrame(right)
        lang_frame.pack(fill="x", padx=40, pady=25)

        self.source_lang = ctk.CTkComboBox(
            lang_frame,
            values=list(self.languages.keys()),
            width=250
        )
        self.source_lang.set("English")
        self.source_lang.pack(side="left", padx=30)

        ctk.CTkButton(
            lang_frame,
            text="⇄",
            width=60,
            command=self.swap_languages
        ).pack(side="left", padx=20)

        self.target_lang = ctk.CTkComboBox(
            lang_frame,
            values=list(self.languages.keys()),
            width=250
        )
        self.target_lang.set("Hindi")
        self.target_lang.pack(side="left", padx=30)

        text_frame = ctk.CTkFrame(right)
        text_frame.pack(fill="both", expand=True, padx=40, pady=10)

        left_panel = ctk.CTkFrame(text_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(left_panel, text="Input Text",
                     font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20, pady=10)

        self.source_text = ctk.CTkTextbox(left_panel, font=("Segoe UI", 18))
        self.source_text.pack(fill="both", expand=True, padx=20, pady=20)

        right_panel = ctk.CTkFrame(text_frame)
        right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(right_panel, text="Translation",
                     font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=20, pady=10)

        self.target_text = ctk.CTkTextbox(right_panel, font=("Segoe UI", 18))
        self.target_text.pack(fill="both", expand=True, padx=20, pady=20)

        btn_frame = ctk.CTkFrame(right)
        btn_frame.pack(fill="x", padx=40, pady=20)

        ctk.CTkButton(btn_frame, text="Translate", height=60, width=180,
                      command=self.translate).pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="Copy", height=60, width=180,
                      command=self.copy_text).pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="Clear", height=60, width=180,
                      command=self.clear_text).pack(side="left", padx=15)

        ctk.CTkButton(btn_frame, text="⭐ Save Favorite", height=60, width=200,
                      command=self.save_favorite).pack(side="left", padx=15)

        history_frame = ctk.CTkFrame(right)
        history_frame.pack(fill="x", padx=40, pady=20)

        ctk.CTkLabel(history_frame, text="Recent Translations",
                     font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=20)

        self.history_box = ctk.CTkTextbox(history_frame, height=120)
        self.history_box.pack(fill="both", expand=True, padx=20, pady=10)


    def translate(self):
        text = self.source_text.get("1.0", "end").strip()
        target_code = self.languages[self.target_lang.get()]
        result = translate_text(text, target_code)

        self.target_text.delete("1.0", "end")
        self.target_text.insert("end", result)

        self.history_box.insert("end", f"{text} ➜ {result}\n\n")

    def clear_text(self):
        self.source_text.delete("1.0", "end")
        self.target_text.delete("1.0", "end")

    def copy_text(self):
        text = self.target_text.get("1.0", "end")
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Text copied successfully!")

    def swap_languages(self):
        s = self.source_lang.get()
        t = self.target_lang.get()
        self.source_lang.set(t)
        self.target_lang.set(s)


    def save_favorite(self):
        text = self.target_text.get("1.0", "end").strip()

        if not text:
            messagebox.showwarning("Favorites", "Nothing to save!")
            return

        self.favorites_list.append(text)

        with open("favorites.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

        messagebox.showinfo("Favorites", "Saved successfully!")

    def show_favorites(self):
        if not self.favorites_list:
            messagebox.showinfo("Favorites", "No favorites saved yet.")
        else:
            messagebox.showinfo("Favorites", "\n\n".join(self.favorites_list))


    def go_home(self):
        messagebox.showinfo("Home", "Already on Home")

    def show_history(self):
        messagebox.showinfo("History", self.history_box.get("1.0", "end"))

    def voice_message(self):
        messagebox.showinfo("Voice", "Coming soon")

    def open_settings(self):
        messagebox.showinfo("Settings", "Dark mode enabled")

    def show_about(self):
        messagebox.showinfo("About", "AI Translator Project using Python + CustomTkinter")