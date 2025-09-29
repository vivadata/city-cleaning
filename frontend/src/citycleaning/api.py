import ast
import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from google.cloud import bigquery
from google.oauth2 import service_account
from openaq import OpenAQ
import requests

# Load the env
load_dotenv()

# We need the config to connect
gc_config = ast.literal_eval(os.getenv("GCLOUD_CONFIG"))
oaq_config = os.getenv("OPENAQ_DEFAULT_TOKEN")

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
async def get_all_dropoff():
    output = []

    for table in gc_project_tables:
        if table != "dmr":
            dropoffs = await get_dropoff(table)
            output.extend(dropoffs)

    return output

# Get the dropoff points for one type of trash
@api.route("/dropoff/<type>", methods=["GET"])
async def get_dropoff(type):
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

# Get the air quality
@api.route("/air_quality", methods=["GET"])
async def get_air_quality():
    # First get the data from the api
    output = []
    client = OpenAQ(api_key=oaq_config)
    loc_response = client.locations.list(
        coordinates=[48.8534, 2.3488],
        radius=4000,
        limit=1000
    )

    # And extract the specifics of the locations
    loc_data = loc_response.dict()
    locations = loc_data["results"]

    # And from the locations the sensors
    sensors = list()
    for loc in locations:
        if loc["sensors"]:
            sensors.extend(loc["sensors"])

    # Useful columns
    columns = [
        "latest.value",
        "parameter.units",
        "parameter.displayName",
        "datetime_last.local",
        "latest.coordinates.latitude",
        "latest.coordinates.longitude",
    ]

    # Then get the data from the sensors
    for sns in sensors:
        sensor_response = client.sensors.get(sns['id'])
        sensor_data = sensor_response.dict()

        for data in sensor_data['results']:
            is_data = dict()
            is_full = True

            # Only the columns that interest us
            for key in columns:
                # Extract their indentation
                path = key.split(".")
                new_key = "_".join(path)

                # And their value
                value = data

                # If it exists
                for indent in path:
                    if value:
                        value = value[indent]
                    
                    else:
                        value = None

                # And if it is filled
                if not value:
                    is_full = False
                
                else:
                    is_data[new_key] = value
            
            if is_full:
                output.append(is_data)

    return output

# Get the water quality
@api.route("/water_quality", methods=["GET"])
async def get_water_quality():
    output = []
    water_url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc"
    options = [
        "code_departement=75",
        "date_debut_prelevement=2024-12-01"
    ]

    # Those are the columns that interest us
    columns = [
        "date_prelevement",
        "libelle_parametre",
        "resultat",
        "symbole_unite",
        "latitude", 
        "longitude"
    ]

    # The request
    response = requests.get(f"{water_url}?{"&".join(options)}").json()

    # Add all the data to output
    for data in response["data"]:
        is_data = dict()
        is_full = True

        # Only the columns that interest us
        for key in columns:
            # And only if they are filled
            if not data[key]:
                is_full = False
            
            else:
                is_data[key] = data[key]
        
        if is_full:
            output.append(is_data)
    
    return output

async def main():
    api.run(debug=True, host=url_host, port=port_api)

if __name__ == "__main__":
    asyncio.run(main())
