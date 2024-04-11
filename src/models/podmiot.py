class Podmiot:
    def __init__(
        self,
        id_podmiotu,
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
        self.id_podmiotu = id_podmiotu
        self.nip = nip
        self.pelna_nazwa = pelna_nazwa
        self.regon = regon
        self.kod_kraju = kod_kraju
        self.wojewodztwo = wojewodztwo
        self.powiat = powiat
        self.gmina = gmina
        self.ulica = ulica
        self.nr_domu = nr_domu
        self.nr_lokalu = nr_lokalu
        self.miejscowosc = miejscowosc
        self.kod_pocztowy = kod_pocztowy
        self.poczta = poczta
