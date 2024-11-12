import asyncio
import csv
from datetime import datetime
from bleak import BleakClient

# UUIDs for Service and Characteristic, as defined on the ESP32
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# Set the MAC address of your ESP32 here
ESP32_ADDRESS = "54:32:04:22:52:1A"

# CSV file to store sensor data
CSV_FILE = "sensor_data.csv"

# Initialize the CSV file with headers
with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp;ax;ay;az;gx;gy;gz'])

async def run():
    while True:  # Infinite loop for automatic reconnection
        try:
            async with BleakClient(ESP32_ADDRESS) as client:
                print(f"Connected to ESP32: {ESP32_ADDRESS}")

                # Check if the service and characteristic are available
                services = await client.get_services()
                if SERVICE_UUID not in [s.uuid for s in services]:
                    print("Service not found!")
                    return

                # Enable notifications from the characteristic
                def notification_handler(sender, data):
                    # Receive sensor data and decode it as UTF-8 string
                    sensor_data = data.decode("utf-8")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Received data: {sensor_data}")

                    # Save the data to the CSV file
                    with open(CSV_FILE, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([timestamp, sensor_data])

                await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
                print("Waiting for data...")

                # Keep the connection open
                while True:
                    await asyncio.sleep(1)

        except Exception as e:
            print(f"Connection lost: {e}, attempting to reconnect...")
            await asyncio.sleep(5)  # Wait briefly before reconnecting

# Start the main program
asyncio.run(run())
