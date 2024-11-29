import tkinter as tk
from tkinter import ttk
from utils import display

class Window(tk.Toplevel):

    # Fonction pour créer un affichage dans un onglet donné
    def createTab(self, tab, columns, query):
        tree = display.createTreeViewDisplayQuery(tab, columns, query)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(800, 500, self)
        self.title('Consultation des données de la base')
        display.defineGridDisplay(self, 1, 1)

        # Définition des onglets
        #TODO Q4 Créer des nouveaux onglets pour les nouvelles tables
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl) # Communes
        tab5 = ttk.Frame(tabControl) # Travaux
        tab6 = ttk.Frame(tabControl) # Chauffage
        tab7 = ttk.Frame(tabControl) # Isolation
        tab8 = ttk.Frame(tabControl) # Photovoltaique
        tabControl.add(tab1, text='Mesures (1000 1ères valeurs)')
        tabControl.add(tab2, text='Départements')
        tabControl.add(tab3, text='Régions')
        tabControl.add(tab4, text='Communes')
        tabControl.add(tab5, text='Travaux')
        tabControl.add(tab6, text='Chauffage')
        tabControl.add(tab7, text='Isolation')
        tabControl.add(tab8, text='Photovoltaique')
        display.defineGridDisplay(tab1, 1, 2)
        display.defineGridDisplay(tab2, 1, 2)
        display.defineGridDisplay(tab3, 1, 2)
        display.defineGridDisplay(tab4, 1, 2)
        display.defineGridDisplay(tab5, 1, 2)
        display.defineGridDisplay(tab6, 1, 2)
        display.defineGridDisplay(tab7, 1, 2)
        display.defineGridDisplay(tab8, 1, 2)
        tabControl.grid(row=0, column=0, sticky="nswe")

        # Mesures
        columns = ('code_departement', 'date_mesure', 'temperature_min_mesure', 'temperature_max_mesure', 'temperature_moy_mesure')
        query = """
            SELECT code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure
            FROM Mesures
            ORDER BY date_mesure
            LIMIT 1,1000
        """
        self.createTab(tab1, columns, query)

        # Départements
        columns = ('code_departement', 'nom_departement', 'code_region', 'zone_climatique')
        query = """
            SELECT code_departement, nom_departement, code_region, zone_climatique
            FROM Departements
            ORDER BY code_departement
        """
        self.createTab(tab2, columns, query)

        # Régions
        columns = ('code_region', 'nom_region')
        query = """
            SELECT code_region, nom_region
            FROM Regions
            ORDER BY code_region
        """
        self.createTab(tab3, columns, query)

        #TODO Q4 Afficher les données des nouvelles tables

        # Communes
        columns = ('code_commune', 'code_departement', 'nom_commune', 'statut_commune', 'altitude_moyenne_commune', 'population_commune', 'superficie_commune', 'code_canton_commune', 'code_arrondissement_commune')
        query = """
            SELECT code_commune, code_departement, nom_commune, statut_commune, altitude_moyenne_commune, population_commune, superficie_commune, code_canton_commune, code_arrondissement_commune
            FROM Commune
            ORDER BY code_commune
            """
        self.createTab(tab4, columns, query)

        # Travaux
        columns = ('id_travaux', 'cout_total', 'cout_induit', 'annee_travaux', 'type_logement', 'annee_construction_logement')
        query = """
            SELECT id_travaux, cout_total, cout_induit, annee_travaux, type_logement, annee_construction_logement
            FROM Travaux
            ORDER BY id_travaux
            """
        self.createTab(tab5, columns, query)
        
        # Chauffage
        columns = ('id_travaux', 'energie_avant_travaux_chauffage', 'energie_installee_chauffage', 'generateur_chauffage', 'type_chaudiere_chauffage')
        query = """
            SELECT id_travaux, energie_avant_travaux_chauffage, energie_installee_chauffage, generateur_chauffage, type_chaudiere_chauffage
            FROM Chauffage
            ORDER BY id_travaux
            """
        self.createTab(tab6, columns, query)

        # Isolation
        columns = ('id_travaux', 'poste_isolation', 'isolant_isolation', 'epaisseur_isolation', 'surface_isolation')
        query = """
            SELECT id_travaux, poste_isolation, isolant_isolation, epaisseur_isolation, surface_isolation
            FROM Isolation
            ORDER BY poste_isolation
            """
        self.createTab(tab7, columns, query)

        # Photovoltaique
        columns = ('id_travaux', 'puissance_photovoltaique', 'type_panneaux_photovoltaique')
        query = """
            SELECT id_travaux, puissance_photovoltaique, type_panneaux_photovoltaique
            FROM Photovoltaique
            ORDER BY id_travaux
            """
        self.createTab(tab8, columns, query)
