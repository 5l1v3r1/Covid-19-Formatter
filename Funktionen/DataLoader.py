import json
from datetime import datetime, timedelta
from os import path
from typing import Optional
import Funktionen.DataUpdate


RKI_BUNDESLAND_DATA_URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"
RKI_IMPF_DATA_URL = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx;jsessionid=46E44493F4E05F1EE65EF1D70BB53D44.internet101?__blob=publicationFile"
RKI_LANDKREIS_DATA_URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"
AUSTRIA_DATA_URL = "https://services1.arcgis.com/YfxQKFk1MjjurGb5/arcgis/rest/services/AUSTRIA_COVID19_Cases/FeatureServer/2/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"


def update_all_data() -> None:
    date = datetime.now()
    str_date = date.strftime("%d.%m.%Y")
    if not path.exists(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json"):
        germany_landkreis_data_from_yesterday = get_data("Ger_LK_All", 1)
        germany_landkreis_data = Funktionen.DataUpdate.get_data_from_api(RKI_LANDKREIS_DATA_URL)
        if germany_landkreis_data_from_yesterday != germany_landkreis_data["features"]:
            Funktionen.DataUpdate.store_data(germany_landkreis_data, "Ger_LK")

    if not path.exists(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json"):
        germany_bundesland_data_from_yesterday = get_data("Ger_BL_All", 1)
        germany_bundesland_data = Funktionen.DataUpdate.get_data_from_api(RKI_BUNDESLAND_DATA_URL)
        if germany_bundesland_data_from_yesterday != germany_bundesland_data["features"]:
            Funktionen.DataUpdate.store_data(germany_bundesland_data, "Ger_BL")

    if not path.exists(f"Daten/Austria/Austria_Bezirk/data-{str_date}.json"):
        austria_data = Funktionen.DataUpdate.get_data_from_api(AUSTRIA_DATA_URL)
        austria_data_from_yesterday = get_data("Au_Bez", 1)
        if austria_data_from_yesterday != austria_data["features"]:
            Funktionen.DataUpdate.store_data(austria_data, "Au_Bez")

    if not path.exists(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.json"):
        germany_impf_data = Funktionen.DataUpdate.get_and_store_impf_data_from_rki(RKI_IMPF_DATA_URL)
        if germany_impf_data is not None:
            Funktionen.DataUpdate.store_data(germany_impf_data, "Ger_Impf")


def get_data(data_option: str, timedelta_days: int, region=None) -> Optional[dict]:
    date = datetime.now() - timedelta(days=timedelta_days)
    str_date = date.strftime("%d.%m.%Y")

    if data_option == "Ger_LK_All":
        if path.exists(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json", "r") as file:
                data = json.loads(file.read())
            return data
    elif data_option == "Ger_LK":
        if path.exists(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Landkreis/data-{str_date}.json", "r") as file:
                data = json.loads(file.read())
                for landkreis in data:
                    if landkreis["attributes"]["GEN"] == region:
                        return landkreis
                print(f"Landkreis {region} nicht gefunden")
    elif data_option == "Ger_BL_All":
        if path.exists(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json", "r") as file:
                data = json.loads(file.read())
            return data
    elif data_option == "Ger_BL":
        if path.exists(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Bundesland/data-{str_date}.json", "r") as file:
                data = json.loads(file.read())
                for bundesland in data:
                    if bundesland["attributes"]["LAN_ew_GEN"] == region:
                        return bundesland
                print(f"Bundesland {region} nicht gefunden")
    elif data_option == "Ger_Impf":
        if path.exists(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.json"):
            with open(f"Daten/Deutschland/Deutschland-Impfung/data-{str_date}.json", "r") as file:
                data = json.loads(file.read())
            return data
    elif data_option == "Au_Bez":
        if path.exists(f"Daten/Austria/Austria-Bezirk/data-{str_date}.json"):
            with open(f"Daten/Austria/Austria-Bezirk/data-{str_date}.json", "r") as file:
                data = json.loads(file.read())
            return data
        else:
            return None
