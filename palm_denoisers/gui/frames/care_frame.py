import customtkinter as ctk
import tifffile as tiff

from .right_base import RightBaseFrame
from palm_denoisers.care.preprocessing import preprocessing


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


    def select_model(self, model_name):
        self.selected_model.set(model_name)
        self.model_params_memory[model_name] = self.models[model_name].copy()

    
    def load_and_show_image_2dcare(self, image_type="low"):
        """
        Load a 3D image stack, display a slider for preview, and split slices into High/Low folders
        if it's 2D CARE.
        """
        file_path = filedialog.askopenfilename(
            title=f"Select {image_type.upper()} IMAGE",
            filetypes=[("Image Files", "*.tif *.tiff *.stk")]
        )
        if not file_path:
            return

        # Stocker le chemin du fichier
        self.image_paths[image_type] = file_path
        print(f"{image_type.upper()} image loaded: {file_path}")

        # Lire la stack avec tifffile
        stack = tifffile.imread(file_path)
        total_slices = stack.shape[0]
        end_idx = max(1, int(total_slices * 0.2))  # 20% pour la prévisualisation

        # --- Slider pour visualiser les slices ---
        slices_preview = stack[:end_idx]

        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        l = ax.imshow(slices_preview[0], cmap="gray")
        ax.axis("off")

        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
        slider = Slider(ax_slider, 'Slice', 0, len(slices_preview)-1, valinit=0, valstep=1)

        def update(val):
            idx = int(slider.val)
            l.set_data(slices_preview[idx])
            fig.canvas.draw_idle()

        slider.on_changed(update)
        plt.show()

        # --- Sauvegarder les slices si c'est 2D CARE ---
        if isinstance(self, Care2DFrame):  # ou autre moyen de vérifier le type
            base_folder = os.path.join(self.save_folder, "data", "Training")
            subfolder = "High" if image_type == "high" else "Low"
            save_path = os.path.join(base_folder, subfolder)

            # Créer le dossier si nécessaire
            os.makedirs(save_path, exist_ok=True)

            # Sauvegarder chaque slice
            for i in range(total_slices):
                filename = f"Training_{i:04d}.tif"
                tifffile.imwrite(os.path.join(save_path, filename), stack[i])
            print(f"{total_slices} slices saved to {save_path}")



    def launch_preprocessing(self):
        model_name = self.selected_model.get()
        img_shape = tiff.imread(self.image_paths["low"]).shape[1]
        preprocessing(self.save_folder, patch_size=img_shape, patches_per_image=1, save_file=str(self.save_folder+"/model_data.npz"))
        print(str(self.save_folder+"/model_data.npz"), img_shape)

    def launch_training(self):
        model_name = self.selected_model.get()
