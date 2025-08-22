import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Slider
from tkinter import filedialog
from PIL import Image


class RightBaseFrame(ctk.CTkFrame):
    def __init__(self, parent, title: str, unsupervised=False):
        super().__init__(parent, width=400)
        
        self.network_label = ctk.CTkLabel(self, text=title, font=("Arial", 16, "bold"))
        self.network_label.pack(pady=5)
        self.image_paths = {"low": None, "high": None}
        self.preview_enabled = ctk.BooleanVar(value=False) # preview loaded images or not

        # Image loading buttons
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

        # Row Preview (Label + Checkbox)
        preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        preview_frame.pack(pady=5, fill="x")
        ctk.CTkLabel(preview_frame, text="Preview").pack(side="left", padx=5)
        self.preview_checkbox = ctk.CTkCheckBox(
            preview_frame, 
            text="", 
            variable=self.preview_enabled, 
            onvalue=True, 
            offvalue=False
        )
        self.preview_checkbox.pack(side="left")

        # Pixel Alignement
        self.alignment_button = ctk.CTkButton(self, text="Perform Sub-Pixel Alignment")
        self.alignment_button.pack(pady=20, fill="x")

        # Model selection
        self.params_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.params_frame.pack(pady=10, fill="both", expand=True)


    def load_and_show_image(self, image_type="low"):
        """
        Load an image file, display it with matplotlib (if preview enabled),
        and store its path.
        """
        file_path = filedialog.askopenfilename(
            title=f"Select {image_type.upper()} IMAGE",
            filetypes=[("Image Files", "*.tif *.tiff *.stk")]
        )
        if not file_path:
            return
        self.image_paths[image_type] = file_path

        if not self.preview_enabled.get():  # no preview
            print(f"{image_type.upper()} image loaded (preview disabled): {file_path}")
            return

        img = Image.open(file_path)
        slices = []
        try:
            i = 0
            while True:
                slices.append(np.array(img))
                i += 1
                img.seek(i)
        except EOFError:
            pass

        end_idx = int(len(slices)*0.2)   # show 20% of the stack
        slices = slices[:end_idx] if end_idx > 0 else slices

        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)  # let space for slider
        l = ax.imshow(slices[0], cmap="gray")
        ax.axis("off")

        # Slider
        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # x, y, width, height
        slider = Slider(ax_slider, 'Slice', 0, len(slices)-1, valinit=0, valstep=1)
        def update(val):
            idx = int(slider.val)
            l.set_data(slices[idx])
            fig.canvas.draw_idle()
        slider.on_changed(update)
        plt.show()