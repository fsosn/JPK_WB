import re


class RachunekValidator:

    def validate(
        self,
        numer_rachunku,
        kod_waluty,
    ):
        errors = []

        if not numer_rachunku:
            errors.append("Numer rachunku jest wymagany")
        elif not re.match(r"^[A-Z]{2}\d{26}$", numer_rachunku):
            errors.append("Nieprawidłowy format numeru rachunku.")

        if not kod_waluty:
            errors.append("Kod waluty jest wymagany")
        elif len(kod_waluty) != 3 and not kod_waluty.isupper():
            errors.append("Nieprawidłowy format kodu waluty.")

        if errors:
            return False, errors
        else:
            return True, ""
