from utils import reader
from datetime import datetime
from models.naglowek import Naglowek
from models.salda import Salda
from models.wyciag_ctrl import WyciagCtrl
from utils.generator import generate_xml


def main():

    podmiot = reader.get_podmiot("../data/input/podmiot.txt")
    numer_rachunku, kod_waluty = reader.get_rachunek_data("../data/input/rachunek.txt")

    since_date = datetime.strptime("01.03.2024", "%d.%m.%Y")
    to_date = datetime.strptime("31.03.2024", "%d.%m.%Y")
    wyciag_wiersze = reader.get_wyciag_wiersz_list(
        "../data/input/operacje.txt", since=since_date, to=to_date
    )
    naglowek = Naglowek(
        "JPK_WB", "1", "1", datetime.now(), since_date, to_date, kod_waluty, "1"
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

    wyciag_ctrl = WyciagCtrl(
        len(wyciag_wiersze), "{:.2f}".format(suma_obciazen), "{:.2f}".format(suma_uznan)
    )

    generate_xml(
        "../data/output/JPK_WB_{}_{}.xml".format(
            podmiot.nip, datetime.now().strftime("%Y%m%d%H%M")
        ),
        podmiot,
        numer_rachunku,
        naglowek,
        salda,
        wyciag_wiersze,
        wyciag_ctrl,
    )


if __name__ == "__main__":
    main()
