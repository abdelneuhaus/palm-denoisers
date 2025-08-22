import os
import customtkinter as ctk
from .frames import LeftFrame, Noise2SelfFrame, Care2DFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PALM Denoisers Interface")
        self.geometry("400x700")
        self.minsize(400, 700)

        # Initialize left and right frames
        self.left_frame = LeftFrame(self, controller=self)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = None


    def show_right_frame(self, frame_type: str, project_name: str = "default_project"):
        if not hasattr(self, 'frames'):
            self.frames = {}
        if frame_type not in self.frames:
            if frame_type == "Noise2Self-CB":
                self.frames[frame_type] = Noise2SelfFrame(self)
            elif frame_type == "2D CARE":
                self.frames[frame_type] = Care2DFrame(self)
                high_path = os.path.join(project_name, "data", "Training", "High")
                low_path = os.path.join(project_name, "data", "Training", "Low")
                os.makedirs(high_path, exist_ok=True)
                os.makedirs(low_path, exist_ok=True)
                print(f"Subfolders created: {high_path}, {low_path}")
        for f in self.frames.values():
            f.pack_forget()

        self.right_frame = self.frames[frame_type]
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.geometry("900x400")
