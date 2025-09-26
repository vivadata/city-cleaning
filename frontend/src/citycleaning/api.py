import ast
import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from google.cloud import bigquery
from google.oauth2 import service_account

# Load the env
load_dotenv()

# We need the config to connect
gc_config = ast.literal_eval(os.getenv("GCLOUD_CONFIG"))

# And to know what we connect to
gc_project = os.getenv("GCLOUD_PROJECT")
gc_project_datasets = ast.literal_eval(os.getenv("GCLOUD_DATASETS"))
gc_project_tables = ast.literal_eval(os.getenv("GCLOUD_TABLES"))

# Where will we send it
url_host = os.getenv("URL_HOST")
port_api = int(os.getenv("PORT_API"))

# Instance the backend and allow communication
api = Flask(__name__)
CORS(api)

# Get the credentials
credentials = \
    service_account.Credentials.from_service_account_info(
        gc_config
    )

# And instance the client with them
client = bigquery.Client(credentials=credentials, project=gc_project)

# You can get the latest pickup points
@api.route("/pickup/latest", methods=["GET"])
async def get_latest_pickup():
    current_year = datetime.now().year
    current_month = datetime.now().month

    output = await get_pickup(current_year, current_month)

    return output

# You can get the pickup points for a specific year and month
@api.route("/pickup/<year>/<month>", methods=["GET"])
async def get_pickup(year, month):
    sql_query = f"""
    SELECT 
        `TYPE DECLARATION` as type
        , SPLIT(`geo_point_2d`, ',')[OFFSET(1)] AS longitude
        , SPLIT(`geo_point_2d`, ',')[OFFSET(0)] AS latitude
    FROM 
        `{gc_project}.{gc_project_datasets[0]}.{gc_project_tables[0]}` 
    WHERE 
        `ANNEE DECLARATION` = {year} 
        AND `MOIS DECLARATION` = {month}
    LIMIT
        100
    ;
    """

    output = list()
    query_job = client.query(sql_query)

    # Create a dict from each row of the result
    for row in query_job.result():
        output.append({
            "type": row["type"],
            "longitude": row["longitude"],
            "latitude": row["latitude"],
        })
    
    # If you get nothing try before
    if len(output) == 0:
        # If there is a before
        if year <= 2024 and month <= 3:
            pass

        # First by month if not January
        elif month > 1:
            output = await get_pickup(year, month - 1)
        
        #Then by year if no 2024
        elif year > 2024:
            output = await get_pickup(year - 1, 12)

    return output

# Get all the dropoff points
@api.route("/dropoff/all", methods=["GET"])
def get_all_dropoff():
    output = []

    for table in gc_project_tables:
        if table != "dmr":
            dropoffs = get_dropoff(table)
            output.extend(dropoffs)

    return output

# Get the dropoff points for one type of trash
@api.route("/dropoff/<type>", methods=["GET"])
def get_dropoff(type):
    # This is the table
    table_id = f"{gc_project}.{gc_project_datasets[0]}.{type}"

    # Write the query variable
    sql_query = f"""
    SELECT
        *
    FROM
        {table_id}
    ;
    """

    # Fetch the table metadata
    table = client.get_table(table_id)

    # Extract column names
    columns = [field.name for field in table.schema]

    # Either we have the values
    if "Longitude" in columns and "Latitude" in columns:
        sql_query = f"""
        SELECT
            `Longitude` as longitude
            , `Latitude` as latitude
        FROM
            `{table_id}`
        ;
        """
    
    # Or we extract them
    elif "geo_point_2d" in columns:
        sql_query = f"""
        SELECT
            SPLIT(`geo_point_2d`, ',')[OFFSET(1)] AS longitude
            , SPLIT(`geo_point_2d`, ',')[OFFSET(0)] AS latitude
        FROM
            `{table_id}`
        ;
        """

    output = list()
    query_job = client.query(sql_query)

    # Create a dict from each row of the result
    for row in query_job.result():
        output.append({
            "longitude": row["longitude"],
            "latitude": row["latitude"],
        })

    return output

async def main():
    api.run(debug=True, host=url_host, port=port_api)

if __name__ == "__main__":
    asyncio.run(main())