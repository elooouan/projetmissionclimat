import tkinter as tk
from tkinter import ttk
from utils import display, db  # Importer `display` pour la gestion des widgets et `db` pour la base de données.

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définir la taille et la position de la fenêtre
        display.centerWindow(600, 400, self)
        self.title("Gérer les travaux de rénovation")

        # Configuration de la grille
        display.defineGridDisplay(self, 3, 1)

        # Section : Gérer les travaux
        frame_travaux = ttk.LabelFrame(self, text="Gérer les Travaux")
        frame_travaux.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        display.defineGridDisplay(frame_travaux, 7, 2)

        # Ajout des labels et champs d'entrée
        labels = ["ID Travaux", "Code Departement", "Coût Total", "Coût Induit", "Année Travaux", "Type Logement", "Année Construction"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            ttk.Label(frame_travaux, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = ttk.Entry(frame_travaux)
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=2)
            self.entries[label_text] = entry

        # Boutons pour les actions
        button_frame = ttk.Frame(frame_travaux)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Ajouter", command=self.ajouter_travaux).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Modifier", command=self.modifier_travaux).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.supprimer_travaux).grid(row=0, column=2, padx=5)

        # Section : Affichage des travaux existants
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
        display.defineGridDisplay(tree_frame, 1, 1)

        columns = ("ID Travaux", "Code Departement", "Coût Total", "Coût Induit", "Année Travaux", "Type Logement", "Année Construction")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nswe")

        # Charger les données initiales dans le treeview
        self.loadTravaux()

    def loadTravaux(self):
        """Charge les travaux dans le treeview."""
        # Vider les données existantes
        self.tree.delete(*self.tree.get_children())

        # Requête pour récupérer les travaux
        query = "SELECT * FROM Travaux ORDER BY id_travaux"
        try:
            cursor = db.data.cursor()
            for row in cursor.execute(query):
                self.tree.insert('', tk.END, values=row)
        except Exception as e:
            print("Erreur lors du chargement des travaux :", repr(e))

    def ajouter_travaux(self):
        """Ajoute un nouveau travail dans la base de données."""
        try:
            # Valider les champs
            id_travaux = self.validate_int(self.entries["ID Travaux"].get(), "ID Travaux")
            code_departement = self.entries["Code Departement"].get().strip()
            cout_total = self.validate_float(self.entries["Coût Total"].get(), "Coût Total")
            cout_induit = self.validate_float(self.entries["Coût Induit"].get(), "Coût Induit")
            annee_travaux = self.validate_int(self.entries["Année Travaux"].get(), "Année Travaux")
            type_logement = self.entries["Type Logement"].get().strip()
            annee_construction = self.validate_int(self.entries["Année Construction"].get(), "Année Construction")

            # Requête SQL pour insérer les données
            query = """
                INSERT INTO Travaux (id_travaux, code_departement, cout_total, cout_induit, annee_travaux, type_logement, annee_construction_logement)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor = db.data.cursor()
            cursor.execute(query, (id_travaux, code_departement, cout_total, cout_induit, annee_travaux, type_logement, annee_construction))
            db.data.commit()

            self.loadTravaux()  # Rafraîchir les données affichées
            print("Travail ajouté avec succès.")

        except ValueError as e:
            print("Erreur de validation :", e)
        except Exception as e:
            print("Erreur lors de l'ajout :", repr(e))

    def validate_int(self, value, field_name):
        """Valide qu'une entrée est un entier."""
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"{field_name} doit être un entier.")

    def validate_float(self, value, field_name):
        """Valide qu'une entrée est un flottant."""
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"{field_name} doit être un nombre (entier ou flottant).")


    def modifier_travaux(self):
        """Modifie un travail existant dans la base de données."""
        try:
            # Valider les champs
            id_travaux = self.validate_int(self.entries["ID Travaux"].get(), "ID Travaux")
            code_departement = self.entries["Code Departement"].get().strip()
            cout_total = self.validate_float(self.entries["Coût Total"].get(), "Coût Total")
            cout_induit = self.validate_float(self.entries["Coût Induit"].get(), "Coût Induit")
            annee_travaux = self.validate_int(self.entries["Année Travaux"].get(), "Année Travaux")
            type_logement = self.entries["Type Logement"].get().strip()
            annee_construction = self.validate_int(self.entries["Année Construction"].get(), "Année Construction")

            # Vérifier si l'ID existe avant de tenter une mise à jour
            cursor = db.data.cursor()
            cursor.execute("SELECT COUNT(*) FROM Travaux WHERE id_travaux = ?", (id_travaux,))
            if cursor.fetchone()[0] == 0:
                raise ValueError(f"Aucun travail avec l'ID {id_travaux} n'existe.")

            # Requête SQL pour mettre à jour les données
            query = """
                UPDATE Travaux
                SET code_departement = ?, cout_total = ?, cout_induit = ?, annee_travaux = ?, type_logement = ?, annee_construction_logement = ?
                WHERE id_travaux = ?
            """
            cursor.execute(query, (code_departement, cout_total, cout_induit, annee_travaux, type_logement, annee_construction, id_travaux))
            db.data.commit()

            self.loadTravaux()  # Rafraîchir les données affichées
            print("Travail modifié avec succès.")

        except ValueError as e:
            print("Erreur de validation :", e)
        except Exception as e:
            print("Erreur lors de la modification :", repr(e))


    def supprimer_travaux(self):
        """Supprime un travail existant dans la base de données."""
        id_travaux = self.entries["ID Travaux"].get()
        query = "DELETE FROM Travaux WHERE id_travaux = ?"
        try:
            cursor = db.data.cursor()
            cursor.execute(query, (id_travaux,))
            db.data.commit()
            self.loadTravaux()
        except Exception as e:
            print("Erreur lors de la suppression :", repr(e))
