import requests
import csv
import json
from io import StringIO

def lambda_handler(event, context):
    url = "https://s3.us-east-1.amazonaws.com/pacientex.com.ar/tickets.csv"
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        csvfile = StringIO(content)
        reader = csv.DictReader(csvfile)
        'lalal'
        # Por defecto: devuelve las primeras 5 filas
        rows = []
        for i, row in enumerate(reader):
            if i >= 500:
                break
            rows.append(row)

        result = {
            "rows": rows,
            "message": f"Devueltas {len(rows)} filas del CSV"
        }

        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }