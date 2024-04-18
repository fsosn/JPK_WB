from utils import reader
from datetime import datetime
from models.naglowek import Naglowek
from models.salda import Salda
from models.wyciag_ctrl import WyciagCtrl
from utils.generator import generate_xml
from database.database_manager import DatabaseManager
import os
import sys
from dotenv import load_dotenv


def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            date = datetime.strptime(date_str, "%d.%m.%Y")
            return date
        except ValueError:
            print("Nieprawidłowy format daty. Wprowadź datę w formacie DD.MM.RRRR.")


def get_int_input(prompt, choices):
    while True:
        try:
            choice = int(input(prompt))
            if choice in choices:
                return choice
            else:
                print("Nieprawidłowy wybór. Wybierz jedną z dostępnych opcji.")
        except ValueError:
            print("Nieprawidłowe dane. Wprowadź liczbę.")


def main():
    load_dotenv()

    db_manager = DatabaseManager(
        server=os.getenv("DB_SERVER"),
        database=os.getenv("DB_NAME"),
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
    )
    db_manager.connect()

    podmiot_path = input("Podaj ścieżkę do pliku z danymi podmiotu: ")
    if not os.path.exists(podmiot_path):
        print("Plik podmiotu nie istnieje.")
        sys.exit(1)

    rachunek_path = input("Podaj ścieżkę do pliku z danymi rachunku: ")
    if not os.path.exists(rachunek_path):
        print("Plik rachunku nie istnieje.")
        sys.exit(1)

    operacje_path = input("Podaj ścieżkę do pliku z danymi operacji: ")
    if not os.path.exists(operacje_path):
        print("Plik operacji nie istnieje.")
        sys.exit(1)

    print("Cel złożenia:")
    print("1 - Złożenie informacji na żądanie organu podatkowego")
    print("2 - Złożenie informacji na wniosek podatnika")
    print("3 - Złożenie korekty")
    print("4 - Złożenie informacji z innych przyczyn")
    cel_zlozenia = get_int_input("Wybierz cel złożenia (1-4): ", [1, 2, 3, 4])

    since_date = get_date_input("Podaj datę początkową (DD.MM.RRRR): ")

    to_date = get_date_input("Podaj datę końcową (DD.MM.RRRR): ")

    podmiot = reader.get_podmiot(podmiot_path)

    podmiot_id = db_manager.insert_podmiot(podmiot)

    numer_rachunku, kod_waluty = reader.get_rachunek_data(rachunek_path)

    db_manager.insert_numer_rachunku(numer_rachunku.numer_rachunku, podmiot_id)

    wyciag_wiersze = reader.get_wyciag_wiersz_list(
        operacje_path, since=since_date, to=to_date
    )

    naglowek = Naglowek(
        "JPK_WB",
        "1",
        str(cel_zlozenia),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        since_date,
        to_date,
        kod_waluty,
        "1435",
    )

    suma_obciazen = 0.0
    suma_uznan = 0.0
    if len(wyciag_wiersze) > 0:
        saldo_poczatkowe = float(wyciag_wiersze[0].saldo_operacji) - float(
            wyciag_wiersze[0].kwota_operacji
        )
        saldo_koncowe = wyciag_wiersze[-1].saldo_operacji
        salda = Salda(saldo_poczatkowe, saldo_koncowe)

        for wiersz in wyciag_wiersze:
            kwota_operacji = float(wiersz.kwota_operacji)
            if kwota_operacji < 0.0:
                suma_uznan += abs(kwota_operacji)
            else:
                suma_obciazen += kwota_operacji
    else:
        salda = Salda(0.00, 0.00)

    naglowek_id = db_manager.insert_naglowek(naglowek, numer_rachunku.numer_rachunku)

    db_manager.insert_salda(salda, naglowek_id)

    db_manager.insert_wyciag_wiersze(wyciag_wiersze, naglowek_id)

    wyciag_ctrl = WyciagCtrl(
        len(wyciag_wiersze), "{:.2f}".format(suma_obciazen), "{:.2f}".format(suma_uznan)
    )

    db_manager.insert_wyciag_ctrl(wyciag_ctrl, naglowek_id)

    db_manager.commit()

    data_dir_output = os.path.join(os.getcwd(), "data/output")

    data_wytworzenia_jpk = datetime.strptime(
        naglowek.data_wytworzenia_jpk, "%Y-%m-%d %H:%M:%S"
    )
    data_wytworzenia_jpk_formatted = data_wytworzenia_jpk.strftime("%Y%m%d%H%M")

    file_name = "JPK_WB_{}_{}.xml".format(podmiot.nip, data_wytworzenia_jpk_formatted)

    generate_xml(
        os.path.join(
            data_dir_output,
            file_name,
        ),
        podmiot,
        numer_rachunku,
        naglowek,
        salda,
        wyciag_wiersze,
        wyciag_ctrl,
    )

    print(
        "Wygenerowano plik XML:",
        os.path.join(
            data_dir_output,
            file_name,
        ),
    )


if __name__ == "__main__":
    main()
