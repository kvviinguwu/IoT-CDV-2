from google.cloud import bigquery
import functions_framework
from flask import jsonify
from datetime import datetime

client = bigquery.Client()

# Konfiguracja połączenia z BigQuery
PROJECT_ID = "zaliczenie-iot"  # Twój projekt
DATASET_ID = "IoT"            # Twój dataset
TABLE_ID = "IoT"     # Twoja tabela

@functions_framework.http
def iot_rest(request):
    """HTTP Cloud Function."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    try:
        if request.method == 'POST':
            request_json = request.get_json(silent=True)
            
            if not request_json or 'temperatura' not in request_json:
                return (jsonify({'error': 'Missing temperatura field'}), 400, headers)
            
            # Prawidłowe formatowanie identyfikatora tabeli
            table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
            
            # Formatowanie temperatury do 2 miejsc po przecinku
            temperatura = round(float(request_json['temperatura']), 2)
            
            rows_to_insert = [{
                'temperatura': temperatura,
                'timestamp': datetime.utcnow().isoformat()
            }]
            
            errors = client.insert_rows_json(table_id, rows_to_insert)
            
            if errors == []:
                return (jsonify({'status': 'success'}), 200, headers)
            else:
                return (jsonify({'error': str(errors)}), 500, headers)

        elif request.method == 'GET':
            # Prawidłowe formatowanie identyfikatora tabeli w zapytaniu
            query = f"""
            SELECT ROUND(temperatura, 2) as temperatura, timestamp
            FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            ORDER BY timestamp DESC
            LIMIT 100
            """
            
            query_job = client.query(query)
            results = query_job.result()
            
            temperatures = [
                {
                    'temperatura': round(float(row.temperatura), 2),
                    'timestamp': row.timestamp.isoformat()
                }
                for row in results
            ]
            
            return (jsonify({'temperatures': temperatures}), 200, headers)
            
    except Exception as e:
        return (jsonify({'error': str(e)}), 500, headers)