class Naglowek:
    def __init__(
        self,
        kod_formularza,
        wariant_formularza,
        cel_zlozenia,
        data_wytworzenia_jpk,
        data_od,
        data_do,
        domyslny_kod_waluty,
        kod_urzedu,
    ):
        self.kod_formularza = kod_formularza
        self.wariant_formularza = wariant_formularza
        self.cel_zlozenia = cel_zlozenia
        self.data_wytworzenia_jpk = data_wytworzenia_jpk
        self.data_od = data_od
        self.data_do = data_do
        self.domyslny_kod_waluty = domyslny_kod_waluty
        self.kod_urzedu = kod_urzedu
