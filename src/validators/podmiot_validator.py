import re


class PodmiotValidator:

    def validate(
        self,
        nip,
        pelna_nazwa,
        regon,
        kod_kraju,
        wojewodztwo,
        powiat,
        gmina,
        ulica,
        nr_domu,
        nr_lokalu,
        miejscowosc,
        kod_pocztowy,
        poczta,
    ):
        errors = []

        if not nip:
            errors.append("NIP jest wymagany")
        elif not nip.isdigit() or len(nip) != 10:
            errors.append("NIP powinien składać się z 10 cyfr")

        if not pelna_nazwa:
            errors.append("Pełna nazwa jest wymagana")
        elif len(pelna_nazwa) > 50:
            errors.append("Pełna nazwa powinna mieć maksymalnie 50 znaków")

        if not regon:
            errors.append("REGON jest wymagany")
        if len(regon) != 9 and len(regon) != 14:
            errors.append("REGON powinien mieć 9 lub 14 znaków")

        if not kod_kraju:
            errors.append("Kod kraju jest wymagany")
        elif not kod_kraju.isalpha() or len(kod_kraju) != 2:
            errors.append("Kod kraju powinien składać się z dwóch liter")
        elif not kod_kraju.isupper():
            errors.append("Kod kraju powinien składać się z dużych liter")

        if not wojewodztwo:
            errors.append("Województwo jest wymagane")
        elif len(wojewodztwo) > 50:
            errors.append("Województwo powinno mieć maksymalnie 50 znaków")

        if not powiat:
            errors.append("Powiat jest wymagany")
        elif len(powiat) > 50:
            errors.append("Powiat powinien mieć maksymalnie 50 znaków")

        if not gmina:
            errors.append("Gmina jest wymagana")
        elif len(gmina) > 50:
            errors.append("Gmina powinna mieć maksymalnie 50 znaków")

        if not ulica:
            errors.append("Ulica jest wymagana")
        elif len(ulica) > 50:
            errors.append("Ulica powinna mieć maksymalnie 50 znaków")

        if not nr_domu:
            errors.append("Numer domu jest wymagany")
        elif not str(nr_domu).isdigit() or len(str(nr_domu)) > 10:
            errors.append(
                "Numer domu musi być liczbą całkowitą o długości do 10 znaków"
            )

        if nr_lokalu and (not str(nr_lokalu).isdigit() or len(str(nr_lokalu)) > 10):
            errors.append(
                "Numer lokalu musi być liczbą całkowitą o długości do 10 znaków"
            )

        if not miejscowosc:
            errors.append("Miejscowość jest wymagana")
        elif len(miejscowosc) > 50:
            errors.append("Miejscowość powinna mieć maksymalnie 50 znaków")

        if not kod_pocztowy:
            errors.append("Kod pocztowy jest wymagany")
        elif not re.match(r"^\d{2}-\d{3}$", kod_pocztowy):
            errors.append("Nieprawidłowy format kodu pocztowego.")
        elif len(kod_pocztowy) > 6:
            errors.append("Kod pocztowy powinien mieć maksymalnie 6 znaków")

        if not poczta:
            errors.append("Poczta jest wymagana")
        elif len(poczta) > 50:
            errors.append("Poczta powinna mieć maksymalnie 50 znaków")

        if errors:
            return False, errors
        else:
            return True, ""
