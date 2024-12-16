from google.cloud import bigquery
from scipy.signal import find_peaks
import numpy as np
from datetime import datetime, timedelta

def get_temperature_data():
    """Pobiera dane temperatury z BigQuery."""
    client = bigquery.Client()
    
    query = """
    SELECT temperatura, timestamp
    FROM `zaliczenie-iot.IoT.IoT`
    ORDER BY timestamp ASC
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    temperatures = []
    timestamps = []
    for row in results:
        temperatures.append(float(row.temperatura))
        timestamps.append(row.timestamp)
    
    return temperatures, timestamps

def find_local_maxima(temperatures, timestamps):
    """Znajduje lokalne maksima w danych temperatury."""
    # Konwersja na numpy array
    temp_array = np.array(temperatures)
    
    # Znalezienie lokalnych maksimów
    # prominence=0.5 oznacza, że maksimum musi być o 0.5°C wyższe od otaczających minimów
    # distance=10 oznacza minimalna odległość 10 próbek między maksimami
    peaks, _ = find_peaks(temp_array, prominence=0.5, distance=10)
    
    print("\nZnalezione lokalne maksima temperatury:")
    print("---------------------------------------")
    for peak_idx in peaks:
        print(f"Timestamp: {timestamps[peak_idx]}")
        print(f"Temperatura: {temperatures[peak_idx]:.2f}°C")
        print("---------------------------------------")
    
    return peaks

def main():
    print("Rozpoczynam analizę danych temperatury...")
    
    # Pobranie danych
    temperatures, timestamps = get_temperature_data()
    
    if not temperatures:
        print("Nie znaleziono danych temperatury!")
        return
    
    print(f"\nPrzeanalizowano {len(temperatures)} pomiarów temperatury")
    
    # Znalezienie lokalnych maksimów
    peaks = find_local_maxima(temperatures, timestamps)
    
    print(f"\nZnaleziono {len(peaks)} lokalnych maksimów temperatury")

if __name__ == "__main__":
    main()