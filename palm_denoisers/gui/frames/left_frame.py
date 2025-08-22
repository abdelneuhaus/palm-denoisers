import os
import sys
import customtkinter as ctk

from tkinter import filedialog
from palm_denoisers.gui.console import Console


class LeftFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, width=400)
        self.controller = controller
        self.save_folder = None

        # Config
        config_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=1, corner_radius=5)
        config_frame.pack(pady=10, padx=10, fill="x")
        config_label = ctk.CTkLabel(config_frame, text="Configuration", font=("Arial", 12, "bold"))
        config_label.pack(anchor="w", padx=5, pady=(5,2))

        # Project name typing zone
        self.project_name_entry = ctk.CTkEntry(config_frame, placeholder_text="Project name", width=200)
        self.project_name_entry.pack(pady=5, padx=5)

        # Select or create project folder
        button_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        button_frame.pack(pady=5)
        self.select_button = ctk.CTkButton(button_frame, text="Select project directory", width=100, command=self.select_folder)
        self.select_button.pack(side="left", padx=5)
        self.create_button = ctk.CTkButton(button_frame, text="Create project directory", width=100, command=self.create_folder)
        self.create_button.pack(side="left", padx=5)

        # Denoising algos-
        method_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=1, corner_radius=5)
        method_frame.pack(pady=10, padx=10, fill="x")

        method_label = ctk.CTkLabel(method_frame, text="Denoising Method Selection", font=("Arial", 12, "bold"))
        method_label.pack(anchor="w", padx=5, pady=(5,2))

        self.noise2self_button = ctk.CTkButton(
            method_frame, text="NOISE2SELF-CB", width=150, height=100,
            command=self.launch_noise2self, state="disabled"
        )
        self.noise2self_button.pack(pady=10)

        self.care2d_button = ctk.CTkButton(
            method_frame, text="2D CARE", width=150, height=100,
            command=self.launch_care2d, state="disabled"
        )
        self.care2d_button.pack(pady=10)

        # Console widget
        console_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=1, corner_radius=5)
        console_frame.pack(pady=10, padx=10, fill="both", expand=True)
        console_label = ctk.CTkLabel(console_frame, text="Console", font=("Arial", 12, "bold"))
        console_label.pack(anchor="w", padx=5, pady=(5,2))
        self.console = Console(console_frame, height=150)
        self.console.pack(fill="both", expand=True, padx=5, pady=5)
        sys.stdout = self.console
        sys.stderr = self.console


    def create_folder(self):
        project_name = self.project_name_entry.get().strip()
        if project_name:
            os.makedirs(project_name, exist_ok=True)
            self.save_folder = project_name
            print(f"Folder created: {project_name}")
            self.update_denoising_buttons()
        else:
            print("Please enter a valid project name.")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_folder = folder
            print(f"Selected folder: {folder}")
            self.update_denoising_buttons()

    def update_denoising_buttons(self):
        """Active ou désactive les boutons selon que save_folder soit défini."""
        state = "normal" if self.save_folder else "disabled"
        self.noise2self_button.configure(state=state)
        self.care2d_button.configure(state=state)

    # Callbacks to activate denoising algo buttons
    def launch_noise2self(self):
        if self.save_folder:
            self.controller.show_right_frame("Noise2Self-CB")
        else:
            print("Please create or select a project folder first!")

    def launch_care2d(self):
        if self.save_folder:
            self.controller.show_right_frame("2D CARE", project_name=self.save_folder)
        else:
            print("Please create or select a project folder first!")