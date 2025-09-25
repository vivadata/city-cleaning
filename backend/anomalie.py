from fastapi import FastAPI
from google.cloud import bigquery

app = FastAPI()
client = bigquery.Client()

@app.get("/anomalie")
async def get_anomalie():
    sql_query = """
    SELECT * FROM `rue-de-paris-472314.datasets.dmr`
    """

    query_job = client.query(sql_query)

    for row in query_job.result():
        for i in range(len(query_job.result()._field_to_index)):
            print(row[i])
            

@app.get("/anomalie/{type}")
async def get_anomalie_type(type):
    sql_query = f"""
    SELECT * FROM `rue-de-paris-472314.datasets.{type}`
    """

    query_job = client.query(sql_query)

    for row in query_job.result():
        for i in range(len(query_job.result()._field_to_index)):
            print(row[i])

