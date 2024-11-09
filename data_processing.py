import pandas as pd
from io import StringIO
import numpy as np


def parse_csv_data(csv_string):
    """
    Liest CSV-Daten aus einem String und gibt einen DataFrame zurück.
    """
    df = pd.read_csv(StringIO(csv_string), sep='\t')
    #print("Spaltennamen im DataFrame:", df.columns.tolist())
    return df


def preprocess_data(df):
    """
    Führt eine Vorverarbeitung der IMU-Daten durch.
    Glättet die Daten mittels gleitendem Durchschnitt.
    """
    # Liste der Sensorkolumnen basierend auf den tatsächlichen Spaltennamen
    sensor_columns = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    for col in sensor_columns:
        if col in df.columns:
            df[col] = df[col].rolling(window=5).mean()
        else:
            print(f"Warnung: Spalte {col} nicht in den Daten gefunden.")
    # Entferne Zeilen mit NaN-Werten, die durch das Rolling entstehen
    df = df.dropna()
    return df


def detect_drinking_events(df):
    """
    Erkennt Trinkvorgänge basierend auf Sensorfusion von Beschleunigungs- und Gyroskopdaten.
    """

    # Überprüfen, ob die erforderlichen Spalten vorhanden sind
    required_columns = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Erforderliche Spalte {col} fehlt in den Daten.")

    # Berechne die Beschleunigungsmagnitude
    df['accel_magnitude'] = np.sqrt(df['ax'] ** 2 + df['ay'] ** 2 + df['az'] ** 2)
    # Berechne die Gyroskop-Magnitude
    df['gyro_magnitude'] = np.sqrt(df['gx'] ** 2 + df['gy'] ** 2 + df['gz'] ** 2)

    # Definiere Schwellenwerte (müssen ggf. angepasst werden)
    accel_threshold = 15000  # Beispielwert für Beschleunigung
    gyro_threshold = 10000  # Beispielwert für Gyroskop

    # Erkenne mögliche Trinkereignisse basierend auf den Schwellenwerten
    df['potential_event'] = (df['accel_magnitude'] > accel_threshold) & (df['gyro_magnitude'] > gyro_threshold)

    # Gruppiere aufeinanderfolgende Ereignisse
    df['event_group'] = (df['potential_event'] != df['potential_event'].shift()).cumsum()

    # Filtere die tatsächlichen Ereignisse
    events = df[df['potential_event']].groupby('event_group').size()

    # Anzahl der erkannten Trinkvorgänge
    event_count = len(events)

    return event_count
