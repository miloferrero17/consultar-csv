import csv
import json
from io import StringIO
import requests

def lambda_handler(event, context):
    url = "https://s3.us-east-1.amazonaws.com/pacientex.com.ar/tickets.csv"

    # Extraer parametros desde el cuerpo del request
    body = event.get("body") or "{}"
    try:
        params = json.loads(body)
    except json.JSONDecodeError:
        params = {}

    limit = int(params.get("limit", 5))
    filtro_informador = params.get("Informador PAYAC") or params.get("informador_payac")

    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        csvfile = StringIO(content)
        reader = csv.DictReader(csvfile)

        rows = []
        for row in reader:
            if filtro_informador and row.get("Informador PAYAC") != filtro_informador:
                continue
            rows.append(row)
            if len(rows) >= limit:
                break

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
