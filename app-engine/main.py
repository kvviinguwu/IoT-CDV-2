import os
from flask import Flask, render_template, jsonify
from google.cloud import bigquery
from datetime import datetime, timedelta
import logging

# Konfiguracja loggingu
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
client = bigquery.Client()

# Konfiguracja połączenia z BigQuery
PROJECT_ID = "zaliczenie-iot"
DATASET_ID = "IoT"
TABLE_ID = "IoT"

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error in index route: {str(e)}")
        return "Internal Server Error", 500

@app.route('/data')
def get_data():
    try:
        query = f"""
        SELECT ROUND(AVG(temperatura), 2) as temperatura, 
               TIMESTAMP_TRUNC(timestamp, MINUTE) as timestamp
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        GROUP BY TIMESTAMP_TRUNC(timestamp, MINUTE)
        ORDER BY timestamp DESC
        LIMIT 60
        """
        
        query_job = client.query(query)
        results = query_job.result()
        
        data = []
        for row in results:
            data.append({
                'temperatura': float(row.temperatura),
                'timestamp': row.timestamp.isoformat()
            })
        
        # Odwróć dane, aby najstarsze były pierwsze
        data.reverse()
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error in data route: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Dodaj healthcheck endpoint
@app.route('/_ah/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)