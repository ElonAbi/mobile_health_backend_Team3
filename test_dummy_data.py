import requests

# Lese die Dummy-Daten aus der Datei
with open('dummy_data.csv', 'r') as file:
    csv_data = file.read()

# URL des Flask-Endpunkts (achte darauf, dass die Flask-App läuft)
url = 'http://localhost:5000/detect_drinking'

# Sende die Daten per POST-Anfrage
response = requests.post(url, data=csv_data)

# Ausgabe der Antwort
print('Status Code:', response.status_code)
print('Response JSON:', response.json())
