import customtkinter as ctk

class Console(ctk.CTkTextbox):
    def __init__(self, parent, height=150):
        super().__init__(parent, height=height)
        self.configure(state="disabled")
    def write(self, message):
        self.configure(state="normal")
        self.insert("end", message)
        self.see("end")
        self.configure(state="disabled")

    def flush(self):
        pass
