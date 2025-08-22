import customtkinter as ctk
from .frames import LeftFrame, Noise2SelfFrame, Care2DFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("2D CARE Interface")
        self.geometry("400x600")
        self.minsize(400, 600)

        # --- Partie gauche ---
        self.left_frame = LeftFrame(self, controller=self)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # --- Partie droite ---
        self.right_frame = None

    def show_right_frame(self, frame_type: str):
        """Affiche la frame correspondante à droite."""
        if self.right_frame:
            self.right_frame.destroy()

        if frame_type == "Noise2Self":
            self.right_frame = Noise2SelfFrame(self)
        elif frame_type == "2D CARE":
            self.right_frame = Care2DFrame(self)

        if self.right_frame:
            self.right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            self.geometry("900x400")  # agrandir la fenêtre
