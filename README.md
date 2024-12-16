# IoT Temperature Monitoring System

System monitorowania temperatury wykorzystujący różne usługi Google Cloud Platform.

## Struktura projektu
```
/
├── cloud-run/               # Kod dla Cloud Run
│   ├── main.py             # REST API 
│   └── requirements.txt     # Zależności Python
│
├── esp32/                   # Kod dla ESP32
│   └── temperature_sender/  # Główny program ESP32
│
├── cloud-vm/               # Kod dla Google Cloud VM
│   ├── main.py            # Analiza maksimów lokalnych
│   └── requirements.txt    # Zależności Python
│
├── app-engine/             # Kod dla Google App Engine
│   ├── main.py            # Aplikacja Flask
│   ├── requirements.txt    # Zależności Python
│   ├── app.yaml           # Konfiguracja App Engine
│   └── templates/         # Szablony HTML
│       └── index.html     # Strona główna z wykresem
│
└── README.md              # Dokumentacja projektu
```

## Komponenty systemu

### 1. Cloud Run (REST API)
- Endpoint REST API do odbierania i przechowywania pomiarów temperatury
- Integracja z BigQuery do zapisu danych

### 2. ESP32
- Program odczytujący temperaturę z czujnika DHT11
- Wysyłanie danych do Cloud Run co 5 sekund

### 3. BigQuery
- Tabela do przechowywania pomiarów temperatury
- Struktura: temperatura (FLOAT) i timestamp (TIMESTAMP)

### 4. Google Looker
- Wizualizacja danych w czasie rzeczywistym
- Wykresy temperatury agregowane minutowo

### 5. Cloud VM (Analiza danych)
- Analiza lokalnych maksimów temperatury
- Wykorzystanie biblioteki scipy do analizy sygnałów

### 6. App Engine (Wizualizacja web)
- Aplikacja Flask wyświetlająca wykresy temperatury
- Wykorzystanie Chart.js do dynamicznych wykresów

## Konfiguracja i uruchomienie

### Cloud Run
```bash
cd cloud-run
pip install -r requirements.txt
gcloud run deploy
```

### ESP32
1. Zainstaluj wymagane biblioteki w Arduino IDE
2. Ustaw dane WiFi w kodzie
3. Wgraj program na ESP32

### Cloud VM
```bash
cd cloud-vm
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### App Engine
```bash
cd app-engine
pip install -r requirements.txt
gcloud app deploy
```

## Wymagania
- Python 3.9+
- Arduino IDE z obsługą ESP32
- Konto Google Cloud Platform
- Czujnik temperatury DHT11

## Autor
Łukasz Kanigowski

## Licencja
MIT