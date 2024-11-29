import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Nous avons copy paste la F4 en chageant uniquement la requete SQL
class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1500, 800, self)
        self.title('Q6: Records de temperatures historiques pour la zone H1 en 2018')
        display.defineGridDisplay(self, 1, 1)

        query = """
            WITH Historique AS (
                SELECT strftime('%m-%d', date_mesure) AS general, MIN(temperature_moy_mesure) AS min, MAX(temperature_moy_mesure) AS max
                FROM Mesures
                GROUP BY general
            ),
            AnnualAvg AS (
                SELECT code_departement, AVG(temperature_moy_mesure) AS avg_temp
                FROM Mesures
                JOIN Departements USING(code_departement)
                WHERE zone_climatique = 'H1' AND strftime('%Y', date_mesure) = '2018'
                GROUP BY code_departement
            ),
            Coldest AS (
                SELECT date_mesure, temperature_moy_mesure AS moy_cold
                FROM Mesures 
                JOIN Departements USING(code_departement)
                WHERE code_departement IN (
                    SELECT code_departement
                    FROM AnnualAvg
                    ORDER BY avg_temp ASC
                    LIMIT 1
                )
                AND zone_climatique = 'H1' AND strftime('%Y', date_mesure) = '2018'
            ),
            Hottest AS (
                SELECT date_mesure, temperature_moy_mesure AS moy_hot
                FROM Mesures 
                JOIN Departements USING(code_departement)
                WHERE code_departement IN (
                    SELECT code_departement
                    FROM AnnualAvg
                    ORDER BY avg_temp DESC
                    LIMIT 1
                )
                AND zone_climatique = 'H1' AND strftime('%Y', date_mesure) = '2018'
            )
            SELECT cold.date_mesure, min, max, moy_cold, moy_hot
            FROM Historique h
            JOIN Coldest cold ON general = strftime('%m-%d', cold.date_mesure)
            JOIN Hottest hot ON general = strftime('%m-%d', hot.date_mesure)
        """

        # Extraction des données et affichage dans le tableau
        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs à mettre sur le graphique
        graph1 = []
        graph2 = []
        graph3 = []
        graph4 = []
        tabx = []
        for row in result:
            tabx.append(row[0])
            graph1.append(row[1])
            graph2.append(row[2])
            graph3.append(row[3])
            graph4.append(row[4])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tabx]

        # Ajout de la figure et du subplot qui contiendront le graphique
        fig = Figure(figsize=(15, 8), dpi=100)
        plot1 = fig.add_subplot(111)

        # Affichage des courbes
        plot1.plot(range(len(datetime_dates)), graph1, color='#00FFFF', label='températures min historique')
        plot1.plot(range(len(datetime_dates)), graph2, color='#FF8300', label='températures max historique')
        plot1.plot(range(len(datetime_dates)), graph3, color='#0000FF', label='températures min en zone H1 en 2018')
        plot1.plot(range(len(datetime_dates)), graph4, color='#FF0000', label='températures max en zone H1 en 2018')

        # Configuration de l'axe x pour n'afficher que le premier jour de chaque mois
        xticks = [i for i, date in enumerate(datetime_dates) if date.day == 1]
        xticklabels = [date.strftime('%Y-%m-%d') for date in datetime_dates if date.day == 1]
        plot1.set_xticks(xticks)
        plot1.set_xticklabels(xticklabels, rotation=45)
        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig,  master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()