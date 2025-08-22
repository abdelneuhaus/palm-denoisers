import customtkinter as ctk
from tkinter import filedialog
import os


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, width=400)
        self.controller = controller
        self.save_folder = None

        # Entrée nom projet
        self.project_name_entry = ctk.CTkEntry(self, placeholder_text="Saisir nom projet", width=200)
        self.project_name_entry.pack(pady=10)

        # Boutons SELECT et CREATE
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=5)
        self.select_button = ctk.CTkButton(button_frame, text="SELECT", width=100, command=self.select_folder)
        self.select_button.pack(side="left", padx=5)
        self.create_button = ctk.CTkButton(button_frame, text="CREATE", width=100, command=self.create_folder)
        self.create_button.pack(side="left", padx=5)

        # Boutons Noise2Self et 2D CARE
        self.noise2self_button = ctk.CTkButton(
            self, text="NOISE 2 SELF", width=150, height=100,
            command=lambda: self.controller.show_right_frame("Noise2Self")
        )
        self.noise2self_button.pack(pady=10)

        self.care2d_button = ctk.CTkButton(
            self, text="2D CARE", width=150, height=100,
            command=lambda: self.controller.show_right_frame("2D CARE")
        )
        self.care2d_button.pack(pady=10)

        # Bouton Alignement
        self.alignment_button = ctk.CTkButton(self, text="ALIGNEMENT ?")
        self.alignment_button.pack(pady=20, fill="x")

    def create_folder(self):
        project_name = self.project_name_entry.get().strip()
        if project_name:
            os.makedirs(project_name, exist_ok=True)
            self.save_folder = project_name
            print(f"Dossier créé : {project_name}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_folder = folder
            print(f"Dossier sélectionné : {folder}")
