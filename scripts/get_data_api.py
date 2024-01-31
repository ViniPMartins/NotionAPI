import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

def get_data_Notion_API():
    API_TOKEN = os.getenv("API_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")
    URL_API = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    headers = {
        "Authorization":"Bearer " + API_TOKEN,
        "Notion-Version":"2022-06-28",
        "Content-Type":"application/json"
    }

    response = requests.post(URL_API, headers=headers)

    data = response.json()
    return data

def transform_API_data(data):
    data_transform = {
        'project_ID':[],
        'project_name':[],
        'project_status':[]
    }

    for result in data['results']:
        id_project = result['id']
        name_project = result['properties']['Project name']['title'][0]['text']['content']
        status = result['properties']['Status']['status']['name']
        
        data_transform['project_ID'].append(id_project)
        data_transform['project_name'].append(name_project)
        data_transform['project_status'].append(status)

    return data_transform