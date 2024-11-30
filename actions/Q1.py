import tkinter as tk
from utils import display
from tkinter import ttk

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q1 : départements de la zone climatique H1')
        display.defineGridDisplay(self, 2, 1)
        
        #TODO Q1 Modifier la suite du code (en se basant sur le code de F1) pour répondre à Q1

        # On définit les colonnes que l'on souhaite afficher dans la fenêtre et la requête
        columns = ('code_departement', 'nom_departement')
        query = """SELECT code_departement, nom_departement
                    FROM Departements
                    WHERE zone_climatique = 'H1'
                """

        # On utilise la fonction createTreeViewDisplayQuery pour afficher les résultats de la requête
        tree = display.createTreeViewDisplayQuery(self, columns, query,200)
        tree.grid(row=0, sticky="nswe")
