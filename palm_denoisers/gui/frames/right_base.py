import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import filedialog
from PIL import Image


class RightBaseFrame(ctk.CTkFrame):
    def __init__(self, parent, title: str, unsupervised=False):
        super().__init__(parent, width=400)

        self.network_label = ctk.CTkLabel(self, text=title, font=("Arial", 16, "bold"))
        self.network_label.pack(pady=5)

        # --- Boutons images ---
        hl_frame = ctk.CTkFrame(self, fg_color="transparent")
        hl_frame.pack(pady=5)

        if unsupervised:
            self.low_image_button = ctk.CTkButton(hl_frame, text="Load Low Image", width=260)
            self.low_image_button.pack(side="left", padx=5)
            self.low_image_button.configure(command=lambda: self.load_and_show_image("low"))
        else:
            self.high_image_button = ctk.CTkButton(hl_frame, text="Load High Image", width=120)
            self.high_image_button.pack(side="left", padx=5)
            self.high_image_button.configure(command=lambda: self.load_and_show_image("high"))

            self.low_image_button = ctk.CTkButton(hl_frame, text="Load Low Image", width=120)
            self.low_image_button.pack(side="left", padx=5)
            self.low_image_button.configure(command=lambda: self.load_and_show_image("low"))

        # Parameters
        self.params_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.params_frame.pack(pady=10, fill="both", expand=True)

        # Customize button
        # self.customize_button = ctk.CTkButton(self, text="PERSONALISER RESEAU")
        # self.customize_button.pack(pady=5)

        # self.preview_button = ctk.CTkButton(self, text="PREVIEW")
        # self.preview_button.pack(pady=5)


    def load_and_show_image(self, image_type="low"):
        """
        Load an image file and display it using matplotlib.
        """
        file_path = filedialog.askopenfilename(
            title=f"Select {image_type.upper()} IMAGE",
            filetypes=[("Image Files", "*.tif *.tiff *.stk")]
        )
        if not file_path:
            return
        
        img = Image.open(file_path)
        plt.figure(f"{image_type.upper()} IMAGE")
        plt.imshow(img, cmap="gray")  # ou cmap="viridis" si tu veux
        plt.axis("off")
        plt.show()