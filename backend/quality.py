from fastapi import FastAPI
from openaq import OpenAQ
from pandas import json_normalize
import pandas as pd
import requests
from google.cloud import bigquery

app = FastAPI()

@app.get("/air_quality")
async def get_air_quality():
    client = OpenAQ(api_key="c038bcbd306c3fcbcb37a220a9ed9fd2829af6a317cc59334c22e8d6a49291a9")
    data = response.dict()
    df = json_normalize(data['results'])
    df_sensor = pd.DataFrame()
    
    for i in range(len(df)):
        df_sensor = pd.concat([df_sensor, pd.json_normalize(df.sensors[i])], ignore_index=True)
        df_latest = pd.DataFrame()
    
    for i in range(len(df_sensor)):
        response = client.sensors.get(df_sensor['id'][i])
        data = response.dict()
        df = json_normalize(data['results'])
        df_latest = pd.concat([df_latest, df], ignore_index=True)
    
    df_latest = df_latest[['latest.value', 'parameter.units', 'parameter.displayName', 
           'datetime_last.local', 
           'latest.coordinates.latitude', 'latest.coordinates.longitude']]
    df_latest = df_latest.dropna()
    
    return df_latest


@app.get("/water_quality")
async def get_water_quality():
    response=requests.get('https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc?code_departement=75&date_debut_prelevement=2024-12-01').json()
    df=pd.DataFrame(response['data'])
    df[["date_prelevement","libelle_parametre","resultat","symbole_unite","latitude", "longitude"]]
    
    return df