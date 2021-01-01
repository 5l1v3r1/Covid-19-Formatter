import Funktionen.DataLoader
import Funktionen.TableGenerator

if __name__ == "__main__":
    Funktionen.DataLoader.update_all_data()
    Funktionen.TableGenerator.generate_table_for_germany(0)
    data = Funktionen.DataLoader.get_data("Ger_LK_All", 0)
    for i in data:
        Funktionen.TableGenerator.germany_landkreis_report(i["attributes"]["GEN"], 0)
    Funktionen.TableGenerator.generate_austria_report(0)