import datetime
import time
import pyperclip
from pynput.keyboard import Key, Controller


BUNDESLANDAPI = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"
LANDKREISAPI = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"
VACCINATIONDATA = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx"

subs = ["@Richard#3948", "@ManuInDenWolken#5404", "@lausi#0001", "@Centa#8781", "@ExtraLimo#5719"]

date_objekt = datetime.datetime.now()
str_date = date_objekt.strftime("%d.%m.%Y")
outputs = list()

outputs.append(":flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de:")
outputs.append("Guten Morgen Genossen,")
outputs.append("die Schnitzel-Universität für nicht wissenschaftlich begründete Tatsachen veröffentlicht den Report des Tages.")

with open(f"Reports/Deutschland/Deutschland/Deutschland-Report-{str_date}.txt", "r") as file:
    tables = file.read().split("\n\n")

for table in tables:
    outputs.append(table)

outputs.append(f"Quellen vom {str_date}:")
outputs.append(f"{BUNDESLANDAPI=}")
outputs.append(f"{LANDKREISAPI=}")
outputs.append(f"{VACCINATIONDATA=}")
outputs.append(f"Abonnenten: {', '.join(subs)}")
outputs.append(":flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de: :flag_de:")


time.sleep(5)

for output in outputs:
    if output == "":
        continue
    elif output[0] == "+":
        pyperclip.copy(f"```\n{output}```")
    elif output is not None:
        pyperclip.copy(f"{output}")
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press('v')
    keyboard.release('v')
    keyboard.release(Key.ctrl)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(2)