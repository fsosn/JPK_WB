import re
from datetime import datetime


class OperacjeValidator:

    def validate(
        self,
        data_operacji,
        nazwa_podmiotu,
        opis_operacji,
        kwota_operacji,
        saldo_operacji,
    ):
        errors = []

        if not data_operacji:
            errors.append("Data operacji jest wymagana")
        else:
            try:
                datetime.strptime(data_operacji, "%d.%m.%Y")
            except ValueError:
                errors.append(
                    "Nieprawidłowy format daty operacji. Wymagany: DD.MM.YYYY"
                )

        if not nazwa_podmiotu:
            errors.append("Nazwa podmiotu jest wymagana")
        elif len(nazwa_podmiotu) > 50:
            errors.append("Nazwa podmiotu może mieć maksymalnie 50 znaków")

        if not opis_operacji:
            errors.append("Opis operacji jest wymagany")
        elif len(opis_operacji) > 50:
            errors.append("Opis operacji może mieć maksymalnie 50 znaków")

        if not kwota_operacji:
            errors.append("Kwota operacji jest wymagana")
        elif not re.match(r"^-?\d+(\.\d{1,2})?$", kwota_operacji):
            errors.append("Nieprawidłowy format kwoty operacji.")

        if not saldo_operacji:
            errors.append("Saldo operacji jest wymagane")
        elif not re.match(r"^-?\d+(\.\d{1,2})?$", saldo_operacji):
            errors.append("Nieprawidłowy format salda operacji.")

        if errors:
            return False, errors
        else:
            return True, ""

    def validate_kwota_saldo(self, operacje_data):
        errors = []
        saldo_poprzedni = None
        for i, data in enumerate(operacje_data, start=1):
            kwota_operacji = data["KwotaOperacji"]
            saldo_operacji = data["SaldoOperacji"]

            if saldo_poprzedni is not None:
                saldo_po_operacji = saldo_poprzedni + float(kwota_operacji)
                if round(saldo_po_operacji, 2) != round(float(saldo_operacji), 2):
                    errors.append(f"Błąd w wierszu {i}: Niezgodność salda po operacji")

            saldo_poprzedni = float(saldo_operacji)

        if errors:
            return False, errors
        else:
            return True, "Wszystkie operacje są poprawne"
