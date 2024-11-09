from flask import Flask, request, jsonify
from data_processing import parse_csv_data, preprocess_data, detect_drinking_events
from database import create_table, insert_drinking_event, get_all_drinking_events
from utils import calculate_duration, send_signal_to_watch, update_frontend

app = Flask(__name__)

# Erstelle die Datenbanktabelle beim Starten der App
create_table()


@app.route('/detect_drinking', methods=['POST'])
def detect_drinking():
    """
    Empfängt CSV-Daten, verarbeitet sie und erkennt Trinkvorgänge.
    Speichert das Ergebnis in der Datenbank, sendet ein Signal an die Smartwatch
    und aktualisiert das Frontend.
    """
    # Empfange die CSV-Daten aus der Anfrage
    csv_data = request.data.decode('utf-8')

    # Verarbeite die Daten
    df = parse_csv_data(csv_data)

    # Debug: Ausgabe der Spaltennamen
    print("Spaltennamen im DataFrame:", df.columns.tolist())

    # Vorverarbeitung
    df = preprocess_data(df)

    # Trinkvorgangserkennung
    try:
        event_count = detect_drinking_events(df)
    except KeyError as e:
        return jsonify({'error': str(e)}), 400

    # Berechne die Dauer in Sekunden
    duration = calculate_duration(df)

    # Speichere das Ergebnis in der Datenbank
    insert_drinking_event(event_count, duration)

    # Sende Signal an die Smartwatch
    send_signal_to_watch()

    # Aktualisiere das Frontend
    update_frontend(event_count, duration)

    # Rückgabe an den Client
    return jsonify({'drinking_events': event_count, 'duration': duration})


@app.route('/get_drinking_data', methods=['GET'])
def get_drinking_data():
    """
    Gibt alle gespeicherten Trinkdaten aus der Datenbank zurück.
    """
    events = get_all_drinking_events()
    events_list = []
    for event in events:
        events_list.append({
            'id': event[0],
            'timestamp': event[1],
            'event_count': event[2]
        })
    return jsonify({'drinking_events': events_list})


# @app.route('/get_daily_need', methods=['GET'])
# def get_daily_need():
#     """
#     Berechnet den täglichen Flüssigkeitsbedarf basierend auf der Temperatur.
#     """
#     base_need = 2.0  # Basisbedarf in Litern
#
#     # Hole die aktuelle Temperatur
#     temperature = get_temperature()
#
#     # Berechne den angepassten Bedarf
#     adjusted_need = adjust_daily_need(base_need, temperature)
#
#     return jsonify({
#         'base_need': base_need,
#         'temperature': temperature,
#         'adjusted_need': adjusted_need
#     })


if __name__ == '__main__':
    app.run(debug=True)
