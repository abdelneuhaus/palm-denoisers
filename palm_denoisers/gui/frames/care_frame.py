import os
import threading

import customtkinter as ctk
import tifffile as tiff
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider
from tkinter import filedialog
from .right_base import RightBaseFrame
from palm_denoisers.care.preprocessing import launch_preprocessing_thread


class Care2DFrame(RightBaseFrame):
    def __init__(self, parent):
        super().__init__(parent, title="2D CARE", unsupervised=False)

        self.project_name = None
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

        # Network architecture selection
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

        # Data Preprocessing Options
        self.preprocessing_button = ctk.CTkButton(self, text="Data Preparation", fg_color="#4CAF50", hover_color="#45A049")
        self.preprocessing_button.pack(pady=10, fill="x")
        self.preprocessing_button.configure(command=self.launch_preprocessing)
    
        # Launch training button
        self.train_button = ctk.CTkButton(self, text="Launch Training", fg_color="#4CAF50", hover_color="#45A049")
        self.train_button.pack(pady=10, fill="x")
        self.train_button.configure(command=self.launch_training)
        

    def set_project(self, project_name: str):
        self.project_name = project_name
        print(f"Now running 2D-CARE in project: {self.project_name}")

    def select_model(self, model_name):
        self.selected_model.set(model_name)
        self.model_params_memory[model_name] = self.models[model_name].copy()

    # def split_and_order_image(self):
    #     if self.image_paths.get("low") is None or self.image_paths.get("high") is None:
    #         print("Both Low and High images must be loaded before splitting.")
    #         return
    #     for image_type in ["low", "high"]:
    #         stack = tiff.TiffFile(self.image_paths[image_type]).asarray()            
    #         total_slices = stack.shape[0]
    #         subfolder = "High" if image_type == "high" else "Low"
    #         save_path = os.path.join(self.project_name, "data", "Training", subfolder)
    #         os.makedirs(save_path, exist_ok=True)
    #         for i in range(total_slices):
    #             tiff.imwrite(os.path.join(save_path, f"Training_{i:04d}.tif"), stack[i])

    def split_and_order_image(self, callback=None):
        if self.image_paths.get("low") is None or self.image_paths.get("high") is None:
            print("Both Low and High images must be loaded before splitting.")
            return
        worker = threading.Thread(target=self._do_split_and_order, args=(callback,), daemon=True)
        worker.start()

    def _do_split_and_order(self, callback=None):
        for image_type in ["low", "high"]:
            with tiff.TiffFile(self.image_paths[image_type]) as tif:
                stack = tif.asarray()
            total_slices = stack.shape[0]
            subfolder = "High" if image_type == "high" else "Low"
            save_path = os.path.join(self.project_name, "data", "Training", subfolder)
            os.makedirs(save_path, exist_ok=True)
            for i in range(total_slices):
                tiff.imwrite(os.path.join(save_path, f"Training_{i:04d}.tif"), stack[i])
                if i % 500 == 0 or i == total_slices - 1:
                    print(f"{image_type}: {i+1}/{total_slices} frames saved.")
            if callback:
                self.after(0, callback) 

    def launch_preprocessing(self):
        def run_preprocessing():
            img_shape = tiff.imread(self.image_paths["low"]).shape[1]
            print("Launching preprocessing...")
            launch_preprocessing_thread(str(self.project_name+"/data/Training/"),
                        patch_size=img_shape,
                        patches_per_image=1,
                        save_file=str(self.project_name+"/model_data.npz"))
            print("Preprocessing done.")
        self.split_and_order_image(callback=run_preprocessing)


    def launch_training(self):
        model_name = self.selected_model.get()
