import requests

def get_temperature():
    """
    Gibt die aktuelle Temperatur zurück.
    Platzhalter: Verwendet die Temperatur in Hamburg.
    """
    # TODO: Eventuelle Implementiere das Auslesen der Temperatur von der Smartwatch

    #Abrufen der Temperatur in Hamburg von einer Wetter-API

    # TODO: api_key sollte nicht im Code stehen -> Umgebungsvariable
    api_key = 'f51453d1b20d463ebb2f66d16fdc84f6'  # Du benötigst einen API-Schlüssel
    city = 'Hamburg'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'

    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']

    return temperature


def adjust_daily_need(base_need, temperature):
    """
    Passt den täglichen Flüssigkeitsbedarf basierend auf der Temperatur an.
    """
    # Beispielhafte lineare Anpassung
    if temperature > 25:
        adjusted_need = base_need + (temperature - 25) * 0.03  # pro Grad über 25°C +30 ml
    else:
        adjusted_need = base_need
    return round(adjusted_need, 2)
