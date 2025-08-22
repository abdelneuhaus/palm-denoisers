import customtkinter as ctk
from .right_base import RightBaseFrame


class Care2DFrame(RightBaseFrame):
    def __init__(self, parent):
        super().__init__(parent, title="2D CARE", unsupervised=False)

        self.selected_model = ctk.StringVar(value=None)
        self.models = {
            "Small Simple Dataset": {"unet_depth":3, "kernel_size":128, "batch_size":8, "steps_per_epoch":40, "n_epochs":100},
            "Small Complex Dataset": {"unet_depth":4, "kernel_size":64,  "batch_size":8,"steps_per_epoch":40, "n_epochs":100},
            "Medium Simple Dataset": {"unet_depth":3, "kernel_size":128, "batch_size":16, "steps_per_epoch":60, "n_epochs":100},
            "Medium Complex Dataset": {"unet_depth":4, "kernel_size":256, "batch_size":16, "steps_per_epoch":60, "n_epochs":100},
            "Big Simple Dataset": {"unet_depth":4, "kernel_size":128, "batch_size":32,"steps_per_epoch":80, "n_epochs":100},
            "Big Complex Dataset": {"unet_depth":6, "kernel_size":64,  "batch_size":32, "steps_per_epoch":80, "n_epochs":100},
        }
        self.model_params_memory = {}

        dropdown_frame = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        dropdown_frame.pack(pady=5, fill="x")
        label = ctk.CTkLabel(dropdown_frame, text="Select a Network Architecture")
        label.pack(pady=(0,5))
        self.model_dropdown = ctk.CTkOptionMenu(
            dropdown_frame,
            values=list(self.models.keys()),
            variable=self.selected_model,
            command=self.select_model,
            width=200,
            height=40
        )
        self.model_dropdown.pack(pady=0)

    
    def select_model(self, model_name):
        self.selected_model.set(model_name)
        self.model_params_memory[model_name] = self.models[model_name].copy()