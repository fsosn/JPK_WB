from src.utils import reader
from datetime import datetime
from src.models.naglowek import Naglowek
from src.models.salda import Salda
from src.models.wyciag_ctrl import WyciagCtrl
from src.utils.generator import generate_xml


def main():

    podmiot = reader.get_podmiot("data/podmiot.txt")
    numer_rachunku, kod_waluty = reader.get_rachunek_data("data/rachunek.txt")
    since_date = datetime.strptime("11.03.2024", "%d.%m.%Y")
    to_date = datetime.strptime("15.03.2024", "%d.%m.%Y")
    wyciag_wiersze = reader.get_wyciag_wiersz_list(
        "data/operacje.txt", since=since_date, to=to_date
    )
    naglowek = Naglowek("JPK_WB", 1, 1, since_date, since_date, to_date, kod_waluty, 1)

    saldo_poczatkowe = float(wyciag_wiersze[0].saldo_operacji) - float(
        wyciag_wiersze[0].kwota_operacji
    )
    saldo_koncowe = wyciag_wiersze[-1].saldo_operacji
    salda = Salda(saldo_poczatkowe, saldo_koncowe)

    suma_obciazen = 0
    suma_uznan = 0
    for wiersz in wyciag_wiersze:
        kwota_operacji = float(wiersz.kwota_operacji)
        if kwota_operacji < 0:
            suma_uznan += abs(kwota_operacji)
        else:
            suma_obciazen += kwota_operacji

    wyciag_ctrl = WyciagCtrl(len(wyciag_wiersze), suma_obciazen, suma_uznan)


if __name__ == "__main__":
    main()
