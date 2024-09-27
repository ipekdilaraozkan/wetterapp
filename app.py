import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from meteostat import Point, Daily
import pandas as pd

# Hauptfunktion zur Steuerung der App
def hauptprogramm():
    
    st.title("Historische Wetterdaten für Aachen")
    standort = Point(50.7753, 6.0839, 200)
    option = st.selectbox(
        "Wählen Sie einen Zeitraum für die historischen Wetterdaten:",
        ['Letzte Woche', 'Letzter Monat', 'Letzte drei Monate', 'Letzte sechs Monate', 'Letztes Jahr']
    )
    startdatum, enddatum = zeitraum_bestimmen(option)
    daten = wetterdaten_verarbeiten(standort, startdatum, enddatum)
    wetterdaten_visualisieren(daten, startdatum, enddatum)

# Funktion zur Bestimmung des Start- und Enddatums basierend auf der Auswahl des Benutzers
def zeitraum_bestimmen(option):
    perioden = {
        'Letzte Woche': 7,
        'Letzter Monat': 30,
        'Letzte drei Monate': 90,
        'Letzte sechs Monate': 180,
        'Letztes Jahr': 365
    }
    heute = datetime.today()
    startdatum = heute - timedelta(days=perioden[option])
    return startdatum, heute

# Funktion zur Datenverarbeitung
def wetterdaten_verarbeiten(standort, startdatum, enddatum):
    daten = Daily(standort, start=startdatum, end=enddatum)
    daten = daten.fetch()
    daten.index = pd.to_datetime(daten.index)
    return daten

# Funktion zur Visualisierung der Wetterdaten
def wetterdaten_visualisieren(daten, startdatum, enddatum):
    st.subheader(f"Wetterdaten von {startdatum.date()} bis {enddatum.date()}")
    st.subheader(f"Durchschnittliche tägliche Temperatur in Aachen")
    wetterdaten_anzeigen(daten, 'tavg', 'Temperatur (°C)')
    st.subheader(f"Täglicher Niederschlag in Aachen")
    wetterdaten_anzeigen(daten, 'prcp', 'Niederschlag (mm))
    st.subheader(f"Täglicher Schneefall in Aachen")

    if daten['snow'].sum() == 0:
        st.info("Kein Schneefall im ausgewählten Zeitraum aufgezeichnet.")
    else:
        wetterdaten_anzeigen(daten, 'snow', 'Schneefall (mm))

# Funktion zum Plotten der Wetterdaten (Temperatur, Regen, Schnee)
def wetterdaten_anzeigen(daten, datentyp, y_beschriftung, titel):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daten.index, daten[datentyp], marker='o')
    ax.set_title(titel)
    ax.set_ylabel(y_beschriftung)
    ax.set_xlabel('Datum')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Startpunkt der App
if __name__ == "__main__":
    hauptprogramm()
