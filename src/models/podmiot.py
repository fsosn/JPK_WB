import xml.etree.ElementTree as ET


class Podmiot:
    def __init__(
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

    def to_xml(self):
        podmiot_element = ET.Element("Podmiot1")

        identyfikator_podmiotu_element = ET.SubElement(
            podmiot_element, "IdentyfikatorPodmiotu"
        )

        nip_element = ET.SubElement(identyfikator_podmiotu_element, "NIP")
        nip_element.text = self.nip

        pelna_nazwa_element = ET.SubElement(
            identyfikator_podmiotu_element, "PelnaNazwa"
        )
        pelna_nazwa_element.text = self.pelna_nazwa

        regon_element = ET.SubElement(identyfikator_podmiotu_element, "REGON")
        regon_element.text = self.regon

        adres_podmiotu_element = ET.SubElement(podmiot_element, "AdresPodmiotu")

        ulica_element = ET.SubElement(adres_podmiotu_element, "Ulica")
        ulica_element.text = self.ulica

        nr_domu_element = ET.SubElement(adres_podmiotu_element, "NrDomu")
        nr_domu_element.text = self.nr_domu

        nr_lokalu_element = ET.SubElement(adres_podmiotu_element, "NrLokalu")
        nr_lokalu_element.text = self.nr_lokalu

        miejscowosc_element = ET.SubElement(adres_podmiotu_element, "Miejscowosc")
        miejscowosc_element.text = self.miejscowosc

        kod_pocztowy_element = ET.SubElement(adres_podmiotu_element, "KodPocztowy")
        kod_pocztowy_element.text = self.kod_pocztowy

        poczta_element = ET.SubElement(adres_podmiotu_element, "Poczta")
        poczta_element.text = self.poczta

        return podmiot_element
