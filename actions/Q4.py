import tkinter as tk
from utils import display
from tkinter import ttk

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q4 : compléter la BD fournie (relations et données)')
        display.defineGridDisplay(self, 1, 1)
        ttk.Label(
            self,
            text=(
                "On peut tester l'implementation des tableaux avec Delete, Create et Insert DB"
            ),
            wraplength=500,
            anchor="center",
            font=('Helvetica', '10', 'bold')
        ).grid(sticky="we", row=0)
