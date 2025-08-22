import customtkinter as ctk
from .frames import LeftFrame, Noise2SelfFrame, Care2DFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PALM Denoisers Interface")
        self.geometry("400x600")
        self.minsize(400, 600)

        # Left side
        self.left_frame = LeftFrame(self, controller=self)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Right side
        self.right_frame = None

    def show_right_frame(self, frame_type: str):
        if not hasattr(self, 'frames'):
            self.frames = {}
        if frame_type not in self.frames:
            if frame_type == "Noise2Self-CB":
                self.frames[frame_type] = Noise2SelfFrame(self)
            elif frame_type == "2D CARE":
                self.frames[frame_type] = Care2DFrame(self)
        for f in self.frames.values():
            f.pack_forget()

        self.right_frame = self.frames[frame_type]
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.geometry("900x400")
