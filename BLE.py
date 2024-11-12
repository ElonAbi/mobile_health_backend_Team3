import asyncio
from bleak import BleakClient
import pandas as pd
import time

# UUIDs für Service und Characteristic, die auch auf dem ESP32 definiert wurden
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# Setze die MAC-Adresse deines ESP32 hier ein
ESP32_ADDRESS = "54:32:04:22:52:1A"

async def run(raw_data):
    start = time.time()
    final = 10
    while True:  # Endlosschleife für automatische Wiederverbindung
        try:
            async with BleakClient(ESP32_ADDRESS) as client:
                print(f"Verbunden mit ESP32: {ESP32_ADDRESS}")

                # Überprüfen, ob der Service und die Characteristic verfügbar sind
                services = await client.get_services()
                if SERVICE_UUID not in [s.uuid for s in services]:
                    print("Service nicht gefunden!")
                    return

                # Benachrichtigungen von der Characteristic aktivieren
                def notification_handler(sender, data):
                    # Empfange die Sensordaten und dekodiere sie als UTF-8-String
                    sensor_data = data.decode("utf-8")
                    raw_data.append(sensor_data) #does not work. trying for a solution
                    print(f"Empfangene Daten: {sensor_data}")

                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                print("Warte auf Daten...")

                # Endlosschleife, um die Verbindung offen zu halten
                while True:
                    await asyncio.sleep(1)
            timer = 10 # 60 seconds times 15 mins
            while timer > 0:
                time.sleep(0.985) # don't sleep for a full second or else you'll be off
                timer -= 1
                if timer == 0:
                    timer = 15 * 60
                    raw_data.to_csv("raw_data.csv", index=False)
        except Exception as e:
            print(f"Verbindung verloren: {e}, versuche neu zu verbinden...")
            await asyncio.sleep(5)  # Warte kurz, bevor erneut verbunden wird
    

# Hauptprogramm starten

raw_data = pd.DataFrame()
asyncio.run(run(raw_data))
