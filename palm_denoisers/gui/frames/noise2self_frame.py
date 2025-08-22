from .right_base import RightBaseFrame


class Noise2SelfFrame(RightBaseFrame):
    def __init__(self, parent):
        super().__init__(parent, title="Noise2Self-CB", unsupervised=True)

