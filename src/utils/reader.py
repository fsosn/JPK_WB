from validators.podmiot_validator import PodmiotValidator
from validators.rachunek_validator import RachunekValidator
from validators.operacje_validator import OperacjeValidator
from models.podmiot import Podmiot
from models.numer_rachunku import NumerRachunku
from models.wyciag_wiersz import WyciagWiersz
import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


def read_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        column_names = lines[0].strip().split("\t")
        for line in lines[1:]:
            fields = line.strip().split("\t")
            data.append(dict(zip(column_names, fields)))
    return data


def get_podmiot(file_path):
    podmiot_data = read_data(file_path)
    podmiot_validator = PodmiotValidator()
    valid, error = podmiot_validator.validate(
        nip=podmiot_data[0]["NIP"],
        pelna_nazwa=podmiot_data[0]["PelnaNazwa"],
        regon=podmiot_data[0]["REGON"],
        kod_kraju=podmiot_data[0]["KodKraju"],
        wojewodztwo=podmiot_data[0]["Wojewodztwo"],
        powiat=podmiot_data[0]["Powiat"],
        gmina=podmiot_data[0]["Gmina"],
        ulica=podmiot_data[0]["Ulica"],
        nr_domu=podmiot_data[0]["NrDomu"],
        nr_lokalu=podmiot_data[0]["NrLokalu"],
        miejscowosc=podmiot_data[0]["Miejscowosc"],
        kod_pocztowy=podmiot_data[0]["KodPocztowy"],
        poczta=podmiot_data[0]["Poczta"],
    )
    if not valid:
        logger.error(f"Błąd walidacji danych: {error}")
        sys.exit(1)
    else:
        logger.info("Dane podmiotu są poprawne")
        return Podmiot(
            nip=podmiot_data[0]["NIP"],
            pelna_nazwa=podmiot_data[0]["PelnaNazwa"],
            regon=podmiot_data[0]["REGON"],
            kod_kraju=podmiot_data[0]["KodKraju"],
            wojewodztwo=podmiot_data[0]["Wojewodztwo"],
            powiat=podmiot_data[0]["Powiat"],
            gmina=podmiot_data[0]["Gmina"],
            ulica=podmiot_data[0]["Ulica"],
            nr_domu=podmiot_data[0]["NrDomu"],
            nr_lokalu=podmiot_data[0]["NrLokalu"],
            miejscowosc=podmiot_data[0]["Miejscowosc"],
            kod_pocztowy=podmiot_data[0]["KodPocztowy"],
            poczta=podmiot_data[0]["Poczta"],
        )


def get_rachunek_data(file_path):
    rachunek_data = read_data(file_path)
    rachunek_validator = RachunekValidator()
    valid, error = rachunek_validator.validate(
        numer_rachunku=rachunek_data[0]["NumerRachunku"],
        kod_waluty=rachunek_data[0]["KodWaluty"],
    )
    if not valid:
        logger.error(f"Błąd walidacji danych: {error}")
        sys.exit(1)
    else:
        logger.info("Dane rachunku są poprawne")
        return (
            NumerRachunku(numer_rachunku=rachunek_data[0]["NumerRachunku"]),
            rachunek_data[0]["KodWaluty"],
        )


def get_wyciag_wiersz_list(file_path, since=None, to=None):
    operacje_data = read_data(file_path)
    operacje_validator = OperacjeValidator()
    wyciag_wiersze = []
    num_row = 0
    for data in operacje_data:
        data_operacji = datetime.strptime(data["DataOperacji"], "%d.%m.%Y")

        if since and data_operacji < since:
            continue
        if to and data_operacji > to:
            continue

        num_row += 1

        valid, error = operacje_validator.validate(
            data_operacji=data["DataOperacji"],
            nazwa_podmiotu=data["NazwaPodmiotu"],
            opis_operacji=data["OpisOperacji"],
            kwota_operacji=data["KwotaOperacji"],
            saldo_operacji=data["SaldoOperacji"],
        )
        if not valid:
            logger.error(f"Błąd walidacji danych operacji: {error}")
            sys.exit(1)
        else:
            wyciag_wiersz = WyciagWiersz(
                numer_wiersza=num_row,
                data_operacji=data_operacji.strftime("%Y-%m-%d"),
                nazwa_podmiotu=data["NazwaPodmiotu"],
                opis_operacji=data["OpisOperacji"],
                kwota_operacji=data["KwotaOperacji"],
                saldo_operacji=data["SaldoOperacji"],
            )
            wyciag_wiersze.append(wyciag_wiersz)

    valid, error = operacje_validator.validate_kwota_saldo(operacje_data)
    if not valid:
        logger.error(f"Błąd walidacji kwoty i salda: {error}")
        sys.exit(1)
    else:
        logger.info(f"Dane wszystkich operacji są poprawne")

    return wyciag_wiersze
