import requests


def send_signal_to_watch():
    """
    Sendet ein Signal an die Smartwatch, um die Lampe zum Leuchten zu bringen.
    Platzhalterfunktion, die später implementiert wird.
    """
    # TODO: Implementiere die Logik, um ein Signal an die Smartwatch zu senden
    print("Signal an die Smartwatch gesendet, um die Lampe zu aktivieren.")


def update_frontend(event_count, duration):
    """
    Ruft die Methode 'update_drink_data' im Frontend auf, um die Daten zu aktualisieren.
    """
    # URL des Frontend-Endpunkts
    frontend_url = 'http://localhost:3000/update_drink_data'  # Passe die URL entsprechend an

    # Daten, die an das Frontend gesendet werden
    data = {
        'event_count': event_count,
        'duration': duration
    }

    try:
        response = requests.post(frontend_url, json=data)
        if response.status_code == 200:
            print("Frontend erfolgreich aktualisiert.")
        else:
            print(f"Fehler beim Aktualisieren des Frontends: {response.status_code}")
    except Exception as e:
        print(f"Exception beim Aktualisieren des Frontends: {e}")


def calculate_duration(df):
    """
    Berechnet die Dauer in Sekunden, über die die Daten gesammelt wurden.
    Annahme: Es gibt eine Spalte 'timestamp' oder die Indexe sind sequenziell.
    """
    # print(df).head()
    # print(df).tail()
    # print(df).columns
    # Wenn es eine Zeitstempelspalte gibt
    if 'timestamp' in df.columns:
        start_time = df['timestamp'].iloc[0]
        end_time = df['timestamp'].iloc[-1]
        duration = end_time - start_time
        duration_seconds = duration.total_seconds()
    else:
        # Annahme: Jede Messung entspricht einer bestimmten Zeitdifferenz, z.B. 0.1s
        time_per_sample = 0.01  # Beispielwert, anpassen je nach Sampling-Rate
        duration_seconds = len(df) * time_per_sample

    # Runde auf ganze Sekunden
    duration_seconds = duration_seconds

    return duration_seconds



