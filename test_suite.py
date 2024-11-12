import sqlite3
import unittest
import os
import json
from io import StringIO
from unittest.mock import patch

import pandas as pd

# Importiere die zu testenden Module und Funktionen
from data_processing import parse_csv_data, preprocess_data, detect_drinking_events
from database import create_connection, create_table, insert_drinking_event, get_all_drinking_events
from app import app
from temperature import get_temperature, adjust_daily_need


class TestDataProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('dummy_data.csv', 'r') as file:
            cls.csv_data = file.read()
        cls.df = parse_csv_data(cls.csv_data)

    def test_parse_csv_data(self):
        # Test if the CSV data is read correctly
        self.assertEqual(list(self.df.columns), ['ax', 'ay', 'az', 'gx', 'gy', 'gz'])
        self.assertEqual(len(self.df), 286)

    def test_preprocess_data(self):
        # Test data preprocessing
        df_processed = preprocess_data(self.df)
        # Since the rolling window is 5, after dropna only 1 row should remain
        self.assertEqual(len(df_processed), 282)

    def test_detect_drinking_events(self):
        # Test drinking event detection
        df_processed = preprocess_data(self.df)
        event_count = detect_drinking_events(df_processed)
        # Expected value depends on the detection logic; here as an example 0
        self.assertEqual(event_count, 0)

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        # Erstelle eine temporäre Datenbank für die Tests
        self.db_path = 'test_drinking_data.db'

        # Passe die create_connection Funktion an, um die Testdatenbank zu verwenden
        def test_create_connection():
            conn = sqlite3.connect(self.db_path)
            return conn

        # Überschreibe die Funktion in database.py
        global create_connection
        create_connection = test_create_connection
        # Erstelle die Tabelle
        create_table()

    def tearDown(self):
        # Entferne die temporäre Datenbank nach den Tests
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_insert_and_get_drinking_event(self):
        # Testet das Einfügen und Abrufen von Trinkereignissen
        insert_drinking_event(event_count=3, duration=10)
        events = get_all_drinking_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0][2], 3)  # event_count
        self.assertEqual(events[0][3], 10)  # duration


class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        # Setze die Flask-App in den Testmodus
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Erstelle die Datenbanktabelle
        create_table()

    def test_detect_drinking_endpoint(self):
        # Testet den /detect_drinking Endpunkt
        csv_data = """ax,ay,az,gx,gy,gz
        15000,-2300,8500,-12000,-10000,-8000
        16000,-2200,8600,-13000,-11000,-9000
        17000,-2100,8700,-14000,-12000,-10000
        18000,-2000,8800,-15000,-13000,-11000
        19000,-1900,8900,-16000,-14000,-12000
        """
        response = self.app.post('/detect_drinking', data=csv_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('drinking_events', data)
        # Erwarteter Wert hängt von der Erkennungslogik ab
        # Hier gehen wir davon aus, dass ein Trinkvorgang erkannt wurde
        self.assertGreaterEqual(data['drinking_events'], 1)

    def test_get_drinking_data_endpoint(self):
        # Testet den /get_drinking_data Endpunkt
        # Füge ein Ereignis hinzu
        insert_drinking_event(event_count=2, duration=15)
        response = self.app.get('/get_drinking_data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('drinking_events', data)
        self.assertEqual(len(data['drinking_events']), 1)
        self.assertEqual(data['drinking_events'][0]['event_count'], 2)
        self.assertEqual(data['drinking_events'][0]['duration'], 15)

    def test_get_daily_need_endpoint(self):
        # Testet den /get_daily_need Endpunkt
        response = self.app.get('/get_daily_need')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('base_need', data)
        self.assertIn('temperature', data)
        self.assertIn('adjusted_need', data)
        self.assertGreater(data['base_need'], 0)
        self.assertGreater(data['adjusted_need'], 0)

    def tearDown(self):
        # Entferne die Testdatenbank nach den Tests
        if os.path.exists('drinking_data.db'):
            os.remove('drinking_data.db')

class TestTemperature(unittest.TestCase):
    @patch('temperature.requests.get')
    def test_get_temperature(self, mock_get):
        # Mock the API response
        mock_response = {
            'main': {
                'temp': 20.0
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # Call the function
        temperature = get_temperature()

        # Assert the temperature is as expected
        self.assertEqual(temperature, 20.0)

class TestAdjustDailyNeed(unittest.TestCase):
    def test_adjust_daily_need_cold_temperature(self):
        # Testet die Funktion bei niedrigen Temperaturen
        base_need = 2.0
        temperature = 10  # Unter 25°C, Bedarf sollte nicht steigen
        adjusted_need = adjust_daily_need(base_need, temperature)
        self.assertEqual(adjusted_need, 2.0)

    def test_adjust_daily_need_high_temperature(self):
        # Testet die Funktion bei hohen Temperaturen
        base_need = 2.0
        temperature = 30  # Über 25°C, Bedarf sollte steigen
        adjusted_need = adjust_daily_need(base_need, temperature)
        expected_need = 2.0 + (30 - 25) * 0.03  # 2.15 Liter
        self.assertEqual(adjusted_need, round(expected_need, 2))


if __name__ == '__main__':
    unittest.main()
