from logic import WindowLogic, clear_stored
from graphic import DCPWindow


class DCP:
    def __init__(self):
        print("MAYBE xclip HAS TO BE INSTALLED.\nHOW TO INSTALL:\n\tIN TERMINAL -> sudo apt install xclip")
        DCPWindow(clear_stored, WindowLogic())
