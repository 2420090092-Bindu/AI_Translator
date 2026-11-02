import customtkinter as ctk
from services.ai_translation import translate_text


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Translator")
        self.geometry("900x600")

        self.source_text = ctk.CTkTextbox(self, width=350, height=300)
        self.source_text.pack(side="left", padx=20, pady=20)

        self.target_text = ctk.CTkTextbox(self, width=350, height=300)
        self.target_text.pack(side="right", padx=20, pady=20)

        self.translate_btn = ctk.CTkButton(
            self,
            text="Translate",
            command=self.translate
        )

        self.translate_btn.pack(pady=20)

    def translate(self):

        text = self.source_text.get("1.0", "end")

        result = translate_text(text)

        self.target_text.delete("1.0", "end")
        self.target_text.insert("end", result)