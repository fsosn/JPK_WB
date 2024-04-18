import pyodbc
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )
        except Exception as e:
            logger.error("Błąd podczas łączenia z bazą danych:", e)
            sys.exit(1)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        if not self.connection:
            logger.error("Brak połączenia z bazą danych.")
            sys.exit(1)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            logger.error("Błąd podczas wykonywania zapytania:", e)
            sys.exit(1)

    def insert_podmiot(self, podmiot):
        query_check = "SELECT IdPodmiotu FROM Podmiot WHERE NIP = ? AND PelnaNazwa = ? AND REGON = ?"
        cursor_check = self.connection.cursor()
        cursor_check.execute(
            query_check, (podmiot.nip, podmiot.pelna_nazwa, podmiot.regon)
        )
        existing_podmiot_id = cursor_check.fetchone()

        if existing_podmiot_id:
            logger.info("Podmiot znajduje się już w bazie danych. Aktualizuję dane.")
            query_update = """
                UPDATE Podmiot 
                SET PelnaNazwa = ?, REGON = ?, Ulica = ?, NrDomu = ?, NrLokalu = ?, Miejscowosc = ?, KodPocztowy = ?, Poczta = ? 
                WHERE IdPodmiotu = ?
            """
            cursor_update = self.connection.cursor()
            cursor_update.execute(
                query_update,
                (
                    podmiot.pelna_nazwa,
                    podmiot.regon,
                    podmiot.ulica,
                    podmiot.nr_domu,
                    podmiot.nr_lokalu,
                    podmiot.miejscowosc,
                    podmiot.kod_pocztowy,
                    podmiot.poczta,
                    existing_podmiot_id[0],
                ),
            )
            cursor_update.close()
            self.connection.commit()

            return existing_podmiot_id[0]

        else:
            query = """
                INSERT INTO Podmiot (NIP, PelnaNazwa, REGON, KodKraju, Wojewodztwo, Powiat, Gmina, Ulica, NrDomu, NrLokalu, Miejscowosc, KodPocztowy, Poczta)
                OUTPUT INSERTED.IdPodmiotu
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                podmiot.nip,
                podmiot.pelna_nazwa,
                podmiot.regon,
                podmiot.kod_kraju,
                podmiot.wojewodztwo,
                podmiot.powiat,
                podmiot.gmina,
                podmiot.ulica,
                podmiot.nr_domu,
                podmiot.nr_lokalu,
                podmiot.miejscowosc,
                podmiot.kod_pocztowy,
                podmiot.poczta,
            )
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row:
                last_inserted_id = row[0]
            else:
                last_inserted_id = None
            cursor.close()
            self.connection.commit()

            return last_inserted_id

    def insert_numer_rachunku(self, numer_rachunku, podmiot_id):
        query_check = "SELECT IdPodmiotu FROM NumerRachunku WHERE NumerRachunku = ?"
        cursor_check = self.connection.cursor()
        cursor_check.execute(query_check, (numer_rachunku,))
        existing_podmiot_id = cursor_check.fetchone()

        if existing_podmiot_id:
            existing_podmiot_id = existing_podmiot_id[0]
            if existing_podmiot_id != podmiot_id:
                logger.error(
                    "Podmiot przekazany do metody nie jest zgodny z tym przypisanym do numeru rachunku w bazie danych."
                )
                sys.exit(1)

        try:
            query = """
                INSERT INTO NumerRachunku (NumerRachunku, IdPodmiotu)
                VALUES (?, ?)
            """
            values = (numer_rachunku, podmiot_id)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            cursor.close()
            self.connection.commit()
        except pyodbc.IntegrityError:
            logger.info("Rachunek znajduje się już w bazie danych.")

    def insert_naglowek(self, naglowek, numer_rachunku):
        query = """
            INSERT INTO Naglowek (KodFormularza, WariantFormularza, CelZlozenia, DataWytworzeniaJPK, DataOd, DataDo, DomyslnyKodWaluty, KodUrzędu, NumerRachunku)
            OUTPUT INSERTED.IdNaglowka
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = (
            naglowek.kod_formularza,
            naglowek.wariant_formularza,
            naglowek.cel_zlozenia,
            naglowek.data_wytworzenia_jpk,
            naglowek.data_od,
            naglowek.data_do,
            naglowek.domyslny_kod_waluty,
            naglowek.kod_urzedu,
            numer_rachunku,
        )
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        row = cursor.fetchone()
        if row:
            last_inserted_id = row[0]
        else:
            last_inserted_id = None
        cursor.close()
        self.connection.commit()

        return last_inserted_id

    def insert_salda(self, salda, naglowek_id):
        query = """
            INSERT INTO Salda (IdNaglowka, SaldoPoczatkowe, SaldoKoncowe)
            VALUES (?, ?, ?)
        """
        values = (naglowek_id, salda.saldo_poczatkowe, salda.saldo_koncowe)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        cursor.close()
        self.connection.commit()

    def insert_wyciag_wiersze(self, wyciag_wiersze, naglowek_id):
        for wiersz in wyciag_wiersze:
            query = """
                INSERT INTO WyciagWiersz (NumerWiersza, DataOperacji, NazwaPodmiotu, OpisOperacji, KwotaOperacji, SaldoOperacji, IdNaglowka)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                wiersz.numer_wiersza,
                wiersz.data_operacji,
                wiersz.nazwa_podmiotu,
                wiersz.opis_operacji,
                wiersz.kwota_operacji,
                wiersz.saldo_operacji,
                naglowek_id,
            )
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            cursor.close()
        self.connection.commit()

    def insert_wyciag_ctrl(self, wyciag_ctrl, naglowek_id):
        query = """
            INSERT INTO WyciagCtrl (LiczbaWierszy, SumaObciazen, SumaUznan, IdNaglowka)
            VALUES (?, ?, ?, ?)
        """
        values = (
            wyciag_ctrl.liczba_wierszy,
            wyciag_ctrl.suma_obciazen,
            wyciag_ctrl.suma_uznan,
            naglowek_id,
        )
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        cursor.close()
        self.connection.commit()

    def commit(self):
        self.connection.commit()
