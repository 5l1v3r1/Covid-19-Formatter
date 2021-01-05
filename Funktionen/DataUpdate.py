from datetime import datetime, timedelta
from os import path

import pandas as pd
import requests
import json


# RKI_BUNDESLAND_DATA_URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"
# RKI_IMPF_DATA_URL = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx;jsessionid=46E44493F4E05F1EE65EF1D70BB53D44.internet101?__blob=publicationFile"
# RKI_LANDKREIS_DATA_URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"
# AUSTRIA_DATA_URL = "https://services1.arcgis.com/YfxQKFk1MjjurGb5/arcgis/rest/services/AUSTRIA_COVID19_Cases/FeatureServer/2/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"


def store_data(api_json: dict, json_type: str) -> None:
    date_object = datetime.now()
    str_date = date_object.strftime("%d.%m.%Y")
    if json_type == "Ger_BL":
        if not path.exists(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json", "w") as file:
                json.dump(api_json["features"], file)
    elif json_type == "Ger_LK":
        if not path.exists(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json", "w") as file:
                json.dump(api_json["features"], file)
    elif json_type == "Au_Bez":
        if not path.exists(f"Daten/Austria/Austria-Bezirk/data-{str_date}.json"):
            with open(f"Daten/Austria/Austria-Bezirk/data-{str_date}.json", "w") as file:
                json.dump(api_json["features"], file)
    elif json_type == "Ger_Impf":
        if not path.exists(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.json", "w") as file:
                json.dump(api_json, file)


def get_data_from_api(url: str) -> json:
    response = requests.get(url)
    return response.json()


def get_and_store_impf_data_from_rki(url: str) -> dict:
    helper = dict()
    date_object = datetime.now()
    str_date = date_object.strftime("%d.%m.%Y")
    yesterday_str_date = (date_object - timedelta(days=1)).strftime("%d.%m.%Y")
    impf_data_table_name = f"Impfungen_bis_einschl_{(date_object - timedelta(days=1)).strftime('%d.%m.%y')}"

    response = requests.get(url)

    with open(f"Daten/Deutschland/Deutschland-Impfung/data-{yesterday_str_date}.xlsx", "rb")as file:
        yesterday_data = file.read()

    if yesterday_data != response.content:
        if not path.exists(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.xlsx"):
            with open(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.xlsx", "wb") as file:
                file.write(response.content)

            data = pd.read_excel(response.content, sheet_name=impf_data_table_name)
            for i in range(0, 17):
                temp_data = data.loc[[i]]
                # Build a Dict with "Bundeslandname" as key and number of "geimpften" persons as value.
                helper[temp_data["Bundesland"].values[0].replace("*", "")] = int(temp_data["Impfungen kumulativ"].values[0])

            return helper
