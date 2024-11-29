import tkinter as tk
from tkinter import ttk
from utils import display
from utils import db

class Window(tk.Toplevel):

    # Attributs de la classe (pour être en mesure de les utiliser dans les différentes méthodes)
    treeView = None
    combobox = None
    errorLabel = None

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre et des lignes/colonnes
        display.centerWindow(700, 500, self)
        self.title('Q3 : nombre de mesures prises et moyenne des temperatures [...] (version dynamique)')
        display.defineGridDisplay(self, 3, 3)
        self.grid_rowconfigure(3, weight=10) #On donne un poids plus important à la dernière ligne pour l'affichage du tableau
        ttk.Label(self,
                  text="",
                  wraplength=500,
                  anchor="center",
                  font=('Helvetica', '10', 'bold')
                  ).grid(sticky="we", row=0,columnspan=3)

        # Affichage du label et du combobox pour la sélection de la région
        ttk.Label(self,
                  text='Veuillez indiquer une région :',
                  anchor="center",
                  font=('Helvetica', '10', 'bold')
                  ).grid(row=1, column=0)

        # Combobox pour le choix dynamique de la région
        self.combobox = ttk.Combobox(self, state="readonly")
        self.combobox.grid(row=1, column=1)
        self.combobox.bind('<<ComboboxSelected>>', self.searchRegion)  # Bind de la sélection d'une région

        # On place un label sans texte, il servira à afficher les erreurs
        self.errorLabel = ttk.Label(self, anchor="center", font=('Helvetica', '10', 'bold'))
        self.errorLabel.grid(columnspan=3, row=2, sticky="we")

        # Préparation du treeview pour l'affichage des résultats
        columns = ('code_departement', 'nom_departement','num_mesures','moy_temp_moyenne')
        self.treeView = ttk.Treeview(self, columns=columns, show='headings')
        for column in columns:
            self.treeView.column(column, anchor=tk.CENTER, width=15)
            self.treeView.heading(column, text=column)
        self.treeView.grid(columnspan=3, row=3, sticky='nswe')

        # Charger les régions dans le combobox
        self.loadRegions()

        # Fonction qui charge les régions dans le combobox au démarrage
    def loadRegions(self):
        try:
            cursor = db.data.cursor()
            result = cursor.execute("SELECT nom_region FROM Regions ORDER BY nom_region")

            # Ajouter chaque région dans le combobox
            regions = [row[0] for row in result]
            self.combobox['values'] = regions
        except Exception as e:
            self.errorLabel.config(foreground='red', text="Erreur lors du chargement des régions : " + repr(e))

    # Fonction qui récupère la région sélectionnée, exécute la requête et affiche les résultats
    #Q3 Modifier la fonction searchRegion pour un choix dynamique de la région
    def searchRegion(self, event=None):

        # On vide le treeView pour rafraîchir les données
        self.treeView.delete(*self.treeView.get_children())

        # On récupère la valeur saisie dans la case
        region = self.combobox.get()

        # Si la saisie est vide, on affiche une erreu
        if len(region) == 0:
            self.errorLabel.config(foreground='red', text="Veuillez sélectionner une région !")

        # Si la saisie contient quelque chose
        else:
            # On essai d'exécuter notre requête
            try:
                cursor = db.data.cursor()
                result = cursor.execute(""" SELECT D.code_departement, D.nom_departement, COUNT(M.date_mesure) AS num_mesures, AVG(M.temperature_moy_mesure) AS moy_temp_moyenne
                                            FROM Departements D JOIN Regions R ON D.code_region = R.code_region
                                            LEFT JOIN Mesures M ON D.code_departement = M.code_departement
                                            WHERE R.nom_region = ?
                                            GROUP BY D.code_departement
                                            ORDER BY D.code_departement""", [region])
            
            # S'il y a une erreur, on l'affiche à l'utilisateur
            except Exception as e:
                self.errorLabel.config(foreground='red', text="Erreur : " + repr(e))
            
            # Si tout s'est bien passé
            else:
                
                # On affiche les résultats de la requête dans le tableau
                i = 0
                for row in result:
                    self.treeView.insert('', tk.END, values=row)
                    i += 1

                # On affiche un message à l'utilisateur en fonction du nombre de résultats de la requête
                if i == 0:
                    self.errorLabel.config(foreground='orange', text="Aucun résultat pour la région \"" + region + "\" !")
                else:
                    self.errorLabel.config(foreground='green', text="Voici les résultats pour la région \"" + region + "\" :")