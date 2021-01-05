from datetime import datetime, timedelta
from os import path, mkdir
from typing import Tuple

from beautifultable import BeautifulTable

import Funktionen.DataLoader


def german_landkreise_with_zero_infections_deaths_and_lk_over_200(timedelta=0) -> Tuple[str, str]:
    german_landkreis_data = Funktionen.DataLoader.get_data("Ger_LK_All", 0 + timedelta)
    german_landkreis_data_from_yesterday = Funktionen.DataLoader.get_data("Ger_LK_All", 1 + timedelta)

    i = 0
    landkreise = dict()
    landkreise_inzidenz = dict()
    landkreise_all = list()
    landkreise_inzidenz_all = list()

    for data in german_landkreis_data:
        new_infections = data['attributes']['cases'] - german_landkreis_data_from_yesterday[i]['attributes']['cases']
        new_deaths = data['attributes']['deaths'] - german_landkreis_data_from_yesterday[i]['attributes']['deaths']
        seven_days_inzidenz = data['attributes']['cases7_per_100k']

        if new_infections == 0 and new_deaths == 0:
            if data['attributes']['BL'] in landkreise.keys():
                landkreise[data['attributes']['BL']].append(data["attributes"]["county"])
                landkreise_all.append(data["attributes"]["county"])
            else:
                landkreise[data['attributes']['BL']] = list()
                landkreise[data['attributes']['BL']].append(data["attributes"]["county"])
                landkreise_all.append(data["attributes"]["county"])

        if seven_days_inzidenz >= 200:
            if data['attributes']['BL'] in landkreise_inzidenz.keys():
                landkreise_inzidenz[data['attributes']['BL']].append(data["attributes"]["county"])
                landkreise_inzidenz_all.append(data["attributes"]["county"])
            else:
                landkreise_inzidenz[data['attributes']['BL']] = list()
                landkreise_inzidenz[data['attributes']['BL']].append(data["attributes"]["county"])
                landkreise_inzidenz_all.append(data["attributes"]["county"])


        i += 1
    landkreis_out = list()
    landkreis_out.append("Folgende Landkreise melden keine Neuinfektionen und keine Neuverstorbenden:")
    for bl in landkreise.keys():
        landkreis_out.append(f"**{bl}**: {', '.join(sorted(landkreise[bl], key=lambda str: str[3:]))}")
    landkreis_out.append(f"Das sind {len(landkreise_all)} von {len(german_landkreis_data)} ({round(len(landkreise_all)/len(german_landkreis_data)*100, 2)}%)")

    landkreis_inzidenz_out = list()
    landkreis_inzidenz_out.append("Folgende Landkreise melden einen höheren 7 Tage Inzidenzwert als 200:")
    for bl in landkreise_inzidenz.keys():

        landkreis_inzidenz_out.append(f"**{bl}**: {', '.join(sorted(landkreise_inzidenz[bl], key=lambda str: str[3:]))}")
    landkreis_inzidenz_out.append(f"Das sind {len(landkreise_inzidenz_all)} von {len(german_landkreis_data)} ({round(len(landkreise_inzidenz_all) / len(german_landkreis_data) * 100, 2)}%)")

    landkreis_str = "\n".join(landkreis_out)
    landkreise_inzidenz_str = "\n".join(landkreis_inzidenz_out)
    return landkreis_str, landkreise_inzidenz_str


def group_by_bundesland(german_landkreis_data: list) -> Tuple[int, dict]:
    group_by_bundesland = dict()
    group_by_landkreis = 0

    for landkeis_dict in german_landkreis_data:
        if landkeis_dict["attributes"]["BL"] in group_by_bundesland.keys():
            group_by_bundesland[landkeis_dict["attributes"]["BL"]] += landkeis_dict["attributes"]["cases"]
        else:
            group_by_bundesland[landkeis_dict["attributes"]["BL"]] = landkeis_dict["attributes"]["cases"]
        group_by_landkreis += landkeis_dict["attributes"]["cases"]

    return group_by_landkreis, group_by_bundesland


def generate_table_for_germany(timedelta_local: int) -> None:
    date_objekt = datetime.now() - timedelta(days=timedelta_local)
    str_date = date_objekt.strftime("%d.%m.%Y")

    data_lk = Funktionen.DataLoader.get_data("Ger_LK_All", 0 + timedelta_local)
    data = Funktionen.DataLoader.get_data("Ger_BL_All", 0 + timedelta_local)
    data_from_yesterday = Funktionen.DataLoader.get_data("Ger_BL_All", 1 + timedelta_local)
    data_from_7_days = Funktionen.DataLoader.get_data("Ger_BL_All", 7 + timedelta_local)
    lk_data_from_7_days = Funktionen.DataLoader.get_data("Ger_LK_All", 7 + timedelta_local)
    data_from_8_days = Funktionen.DataLoader.get_data("Ger_BL_All", 8 + timedelta_local)

    impf_data = Funktionen.DataLoader.get_data("Ger_Impf", 1)
    impf_data_yesterday = Funktionen.DataLoader.get_data("Ger_Impf", 2)
    impf_data_from_7_days = Funktionen.DataLoader.get_data("Ger_Impf", 7)
    impf_data_from_8_days = Funktionen.DataLoader.get_data("Ger_Impf", 8)

    count_by_landkreis, count_by_bundesland = group_by_bundesland(data_lk)
    count_by_landkreis_old, count_by_bundesland_old = group_by_bundesland(lk_data_from_7_days)

    ranking_dict = dict()
    table_list = list()
    i = 0

    bl_all_infections_ger = 0
    bl_all_infections_old_ger = 0

    lk_all_infections_ger = 0
    lk_all_infections_old_ger = 0

    new_infections_ger = 0
    new_infections_old_ger = 0

    all_deaths_ger = 0
    all_deaths_old_ger = 0

    all_new_deaths_ger = 0
    all_new_deaths_old_ger = 0

    cases_last_7_days_ger = 0
    cases_last_7_days_old_ger = 0

    cases_per_100k_ger = 0
    cases_per_100k_old_ger = 0

    EWZ_ger = 0

    for bundesland in data:
        german_bundesland_name = bundesland["attributes"]["LAN_ew_GEN"]

        bl_all_infections = bundesland['attributes']['Fallzahl']
        bl_all_infections_ger += bl_all_infections
        bl_all_infections_old = data_from_7_days[i]['attributes']['Fallzahl']
        bl_all_infections_old_ger += bl_all_infections_old

        lk_all_infections = count_by_bundesland[bundesland['attributes']['LAN_ew_GEN']]
        lk_all_infections_ger += lk_all_infections
        lk_all_infections_old = count_by_bundesland_old[bundesland['attributes']['LAN_ew_GEN']]
        lk_all_infections_old_ger += lk_all_infections_old

        new_infections = bundesland['attributes']['Fallzahl'] - data_from_yesterday[i]['attributes']['Fallzahl']
        new_infections_ger += new_infections
        new_infections_old = data_from_7_days[i]['attributes']['Fallzahl'] - data_from_8_days[i]['attributes'][
            'Fallzahl']
        new_infections_old_ger += new_infections_old

        all_deaths = bundesland['attributes']['Death']
        all_deaths_ger += all_deaths
        all_deaths_old = data_from_7_days[i]['attributes']['Death']
        all_deaths_old_ger += all_deaths_old

        all_new_deaths = bundesland['attributes']['Death'] - data_from_yesterday[i]['attributes']['Death']
        all_new_deaths_ger += all_new_deaths
        all_new_deaths_old = data_from_7_days[i]['attributes']['Death'] - data_from_8_days[i]['attributes']['Death']
        all_new_deaths_old_ger += all_new_deaths_old

        cases_last_7_days = bundesland['attributes']['cases7_bl']
        cases_last_7_days_ger += cases_last_7_days
        cases_last_7_days_old = data_from_7_days[i]['attributes']['cases7_bl']
        cases_last_7_days_old_ger += cases_last_7_days_old

        cases_per_100k = bundesland['attributes']['cases7_bl_per_100k']
        cases_per_100k_ger += cases_per_100k
        ranking_dict[bundesland["attributes"]["LAN_ew_GEN"]] = cases_per_100k
        cases_per_100k_old = data_from_7_days[i]['attributes']['cases7_bl_per_100k']
        cases_per_100k_old_ger += cases_per_100k_old

        EWZ_ger += bundesland["attributes"]["LAN_ew_EWZ"]

        impfungen_ges = impf_data[german_bundesland_name]
        impfungen_neu = impf_data[german_bundesland_name] - impf_data_yesterday[german_bundesland_name]
        impfungen_ges_old = impf_data_from_7_days[german_bundesland_name]
        impfungen_neu_old = impf_data_from_7_days[german_bundesland_name] - impf_data_from_8_days[german_bundesland_name]

        table = BeautifulTable()
        table.columns.header = [german_bundesland_name, "Aktuell", "Vor 7 Tagen"]
        table.rows.append(["Gesamtzahl BL", f"{bl_all_infections:,}", f"{bl_all_infections_old:,}"])
        table.rows.append(["Gesamtzahl LK", f"{lk_all_infections:,}", f"{lk_all_infections_old:,}"])
        table.rows.append(["Neuinfektionen zum Vortag", f"{new_infections:,}", f"{new_infections_old:,}"])
        table.rows.append(["Gesamtzahl der Verstorbenen", f"{all_deaths:,}", f"{all_deaths_old:,}"])
        table.rows.append(["Neuverstorbene zum Vortag", f"{all_new_deaths:,}", f"{all_new_deaths_old:,}"])
        table.rows.append(["Fälle in einer Woche", f"{cases_last_7_days:,}", f"{cases_last_7_days_old:,}"])
        table.rows.append(["Fälle pro 100k Einwohner / 7 Tage", f"{cases_per_100k:,}", f"{cases_per_100k_old:,}"])
        table.rows.append(["Impfungen Gesamt", f"{impfungen_ges:,}", f"{impfungen_ges_old:,}"])
        table.rows.append(["Impfungen Neu", f"{impfungen_neu:,}", f"{impfungen_neu_old:,}"])

        table_list.append(table)
        if not path.exists(f"Reports/Deutschland/Bundesland/{german_bundesland_name}"):
            mkdir(f"Reports/Deutschland/Bundesland/{german_bundesland_name}")
        if not path.exists(f"Reports/Deutschland/Bundesland/{german_bundesland_name}/{german_bundesland_name}-Report-{str_date}.txt"):
            with open(f"Reports/Deutschland/Bundesland/{german_bundesland_name}/{german_bundesland_name}-Report-{str_date}.txt", "a") as file:
                file.write(str(table) + "\n\n")

        i += 1

    impfungen_ges = impf_data["Gesamt"]
    impfungen_neu = impf_data["Gesamt"] - impf_data_yesterday["Gesamt"]
    impfungen_ges_old = impf_data_from_7_days["Gesamt"]
    impfungen_neu_old = impf_data_from_7_days["Gesamt"] - impf_data_from_8_days["Gesamt"]

    table = BeautifulTable()
    table.columns.header = ["Deutschland", "Aktuell", "Vor 7 Tagen"]
    table.rows.append(["Gesamtzahl BL Aktuell", f"{bl_all_infections_ger:,}", f"{bl_all_infections_old_ger:,}"])
    table.rows.append(["Gesamtzahl LK Aktuell", f"{lk_all_infections_ger:,}", f"{lk_all_infections_old_ger:,}"])
    table.rows.append(["Neuinfektionen zum Vortag", f"{new_infections_ger:,}", f"{new_infections_old_ger:,}"])
    table.rows.append(["Gesamtzahl der Verstorbenen", f"{all_deaths_ger:,}", f"{all_deaths_old_ger:,}"])
    table.rows.append(["Neuverstorbene zum Vortag", f"{all_new_deaths_ger:,}", f"{all_new_deaths_old_ger:,}"])
    table.rows.append(["Fälle in einer Woche / 7 Tage", f"{cases_last_7_days_ger:,}", f"{cases_last_7_days_old_ger:,}"])
    table.rows.append(["Impfungen Gesamt", f"{impfungen_ges:,}", f"{impfungen_ges_old:,}"])
    table.rows.append(["Impfungen Neu", f"{impfungen_neu:,}", f"{impfungen_neu_old:,}"])
    table.rows.append(
        [f"Wie viel Prozent sind Geimpft?({EWZ_ger=:,})", f"{round(impfungen_ges / EWZ_ger * 100, 2)}", f""])

    table_list.append(table)

    table = BeautifulTable()
    table.columns.header = ["Ranking by 7 Days Inzidenz", "Value"]
    i = 1
    for element in dict(sorted(ranking_dict.items(), key=lambda item: item[1])):
        table.rows.append([f"{i}. {element}", f"{ranking_dict[element]:,}"])
        i += 1
    table_list.append(table)

    lk_zero_deaths_and_infektion_str, lk_over_200 = german_landkreise_with_zero_infections_deaths_and_lk_over_200()

    table_list.append(lk_zero_deaths_and_infektion_str)

    table_list.append(lk_over_200)

    if not path.exists(f"Reports/Deutschland/Deutschland/Deutschland-Report-{str_date}.txt"):
        with open(f"Reports/Deutschland/Deutschland/Deutschland-Report-{str_date}.txt", "a") as file:
            for table in table_list:
                file.write(str(table) + "\n\n")


def germany_landkreis_report(landkreis, timedelta_local):
        data = Funktionen.DataLoader.get_data("Ger_LK", 0 + timedelta_local, region=landkreis)
        data_from_yesterday = Funktionen.DataLoader.get_data("Ger_LK", 1 + timedelta_local, region=landkreis)
        data_from_7_days = Funktionen.DataLoader.get_data("Ger_LK", 7 + timedelta_local, region=landkreis)
        data_from_8_days = Funktionen.DataLoader.get_data("Ger_LK", 8 + timedelta_local, region=landkreis)

        i = 0

        lk_all_infections = data['attributes']['cases']
        lk_all_infections_old = data_from_7_days['attributes']['cases']

        new_infections = data['attributes']['cases'] - data_from_yesterday['attributes']['cases']
        new_infections_old = data_from_7_days['attributes']['cases'] - data_from_8_days['attributes']['cases']

        all_deaths = data['attributes']['deaths']
        all_deaths_old = data_from_7_days['attributes']['deaths']

        all_new_deaths = data['attributes']['deaths'] - data_from_yesterday['attributes']['deaths']
        all_new_deaths_old = data_from_7_days['attributes']['deaths'] - data_from_8_days['attributes']['deaths']

        cases_last_7_days = data['attributes']['cases7_lk']
        cases_last_7_days_old = data_from_7_days['attributes']['cases7_lk']

        cases_per_100k = data['attributes']['cases7_per_100k_txt']
        cases_per_100k_old = data_from_7_days['attributes']['cases7_per_100k_txt']

        date_objekt = datetime.now() - timedelta(days=timedelta_local)
        str_date = date_objekt.strftime("%d.%m.%Y")

        table = BeautifulTable()
        table.columns.header = [f'{data["attributes"]["GEN"]} ({str_date})', "Aktuell", "Vor 7 Tagen"]
        table.rows.append(["Gesamtzahl", f"{lk_all_infections:,}", f"{lk_all_infections_old:,}"])
        table.rows.append(["Neuinfektionen zum Vortag", f"{new_infections:,}", f"{new_infections_old:,}"])
        table.rows.append(["Gesamtzahl der Verstorbenen", f"{all_deaths:,}", f"{all_deaths_old:,}"])
        table.rows.append(["Neuverstorbene zum Vortag", f"{all_new_deaths:,}", f"{all_new_deaths_old:,}"])
        table.rows.append(["Fälle in einer Woche", f"{cases_last_7_days:,}", f"{cases_last_7_days_old:,}"])
        table.rows.append(["Fälle pro 100k Einwohner / 7 Tage", f"{cases_per_100k}", f"{cases_per_100k_old}"])

        if not path.exists(f"Reports/Deutschland/Landkreise/{data['attributes']['BL']}"):
            mkdir(f"Reports/Deutschland/Landkreise/{data['attributes']['BL']}")
        if not path.exists(f"Reports/Deutschland/Landkreise/{data['attributes']['BL']}/{data['attributes']['GEN']}"):
            mkdir(f"Reports/Deutschland/Landkreise/{data['attributes']['BL']}/{data['attributes']['GEN']}")
        if not path.exists(f"Reports/Deutschland/Landkreise/{data['attributes']['BL']}/{data['attributes']['GEN']}/{data['attributes']['GEN']}-Report-{str_date}.txt"):
            with open(f"Reports/Deutschland/Landkreise/{data['attributes']['BL']}/{data['attributes']['GEN']}/{data['attributes']['GEN']}-Report-{str_date}.txt", "w") as file:
                file.write(str(table) + "\n\n")


def generate_austria_report(timedelta_local: int) -> None:
    date_objekt = datetime.now() - timedelta(days=timedelta_local)
    str_date = date_objekt.strftime("%d.%m.%Y")

    data = Funktionen.DataLoader.get_data("Au_Bez", 0 + timedelta_local)
    data_from_yesterday = Funktionen.DataLoader.get_data("Au_Bez", 1 + timedelta_local)
    data_from_7_days = Funktionen.DataLoader.get_data("Au_Bez", 7 + timedelta_local)
    data_from_8_days = Funktionen.DataLoader.get_data("Au_Bez", 8 + timedelta_local)

    if data is None:
        return None

    ranking_dict = dict()
    table_list = list()
    i = 0

    all_infections_au = 0
    all_infections_old_au = 0

    all_aktive_infections_au = 0
    all_aktive_infections_old_au = 0

    new_infections_au = 0
    new_infections_old_au = 0

    all_deaths_au = 0
    all_deaths_old_au = 0

    all_new_deaths_au = 0
    all_new_deaths_old_au = 0

    for bundesland in data:
        all_infections = bundesland['attributes']['infizierte']
        all_infections_au += all_infections
        all_infections_old = data_from_7_days[i]['attributes']['infizierte']
        all_infections_old_au += all_infections_old

        all_aktive_infections = bundesland['attributes']['positiv']
        all_aktive_infections_au += all_aktive_infections
        all_aktive_infections_old = data_from_7_days[i]['attributes']['positiv']
        all_aktive_infections_old_au += all_aktive_infections_old

        new_infections = bundesland['attributes']['infizierte'] - data_from_yesterday[i]['attributes']['infizierte']
        new_infections_au += new_infections
        new_infections_old = data_from_7_days[i]['attributes']['infizierte'] - data_from_8_days[i]['attributes'][
            'infizierte']
        new_infections_old_au += new_infections_old

        all_deaths = bundesland['attributes']['verstorbene']
        all_deaths_au += all_deaths
        all_deaths_old = data_from_7_days[i]['attributes']['verstorbene']
        all_deaths_old_au += all_deaths_old

        all_new_deaths = bundesland['attributes']['verstorbene'] - data_from_yesterday[i]['attributes']['verstorbene']
        all_new_deaths_au += all_new_deaths
        all_new_deaths_old = data_from_7_days[i]['attributes']['verstorbene'] - data_from_8_days[i]['attributes'][
            'verstorbene']
        all_new_deaths_old_au += all_new_deaths_old

        ranking_dict[bundesland["attributes"]["bundesland"]] = round(all_aktive_infections / (bundesland["attributes"]["einwohner"] / 100000), 2)

        table = BeautifulTable()
        table.columns.header = [bundesland["attributes"]["bundesland"], "Aktuell", "Vor 7 Tagen"]
        table.rows.append(["Alle Infektionen", f"{all_infections:,}", f"{all_infections_old:,}"])
        table.rows.append(["Alle aktiven Fälle", f"{all_aktive_infections:,}", f"{all_aktive_infections_old:,}"])
        table.rows.append(["Neuinfektionen zum Vortag", f"{new_infections:,}", f"{new_infections_old:,}"])
        table.rows.append(["Gesamtzahl der Verstorbenen", f"{all_deaths:,}", f"{all_deaths_old:,}"])
        table.rows.append(["Neuverstorbene zum Vortag", f"{all_new_deaths:,}", f"{all_new_deaths_old:,}"])
        table_list.append(table)
        i += 1

    table = BeautifulTable()
    table.columns.header = ["Österreich", "Aktuell", "Vor 7 Tagen"]
    table.rows.append(["Gesamtzahl Infektionen", f"{all_infections_au:,}", f"{all_infections_old_au:,}"])
    table.rows.append(["Gesamtzahl aktive Fälle", f"{all_aktive_infections_au:,}", f"{all_aktive_infections_old_au:,}"])
    table.rows.append(["Neuinfektionen zum Vortag", f"{new_infections_au:,}", f"{new_infections_old_au:,}"])
    table.rows.append(["Gesamtzahl der Verstorbenen", f"{all_deaths_au:,}", f"{all_deaths_old_au:,}"])
    table.rows.append(["Neuverstorbene zum Vortag", f"{all_new_deaths_au:,}", f"{all_new_deaths_old_au:,}"])

    table_list.append(table)

    table = BeautifulTable()
    table.columns.header = ["Ranking von aktiven Infektionen pro 100k", "Value"]
    i = 1
    for element in dict(sorted(ranking_dict.items(), key=lambda item: item[1])):
        table.rows.append([f"{i}. {element}", f"{ranking_dict[element]:,}"])
        i += 1
    table_list.append(table)

    if not path.exists(f"Reports/Österreich/Österreich-Report-{str_date}.txt"):
        with open(f"Reports/Österreich/Österreich-Report-{str_date}.txt", "a") as file:
            for table in table_list:
                file.write(str(table) + "\n\n")