import xml.etree.ElementTree as ET
import xml.dom.minidom


def generate_xml(
    file_path, podmiot, numer_rachunku, naglowek, salda, wyciag_wiersze, wyciag_ctrl
):
    ET.register_namespace("tns", "http://crd.gov.pl/wzor/2020/05/08/9393/")

    root = ET.Element(
        "{http://crd.gov.pl/wzor/2020/05/08/9393/}JPK",
        {
            "xmlns:etd": "http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2020/03/11/eD/DefinicjeTypy/",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        },
    )

    naglowek_element = ET.SubElement(
        root, "{http://crd.gov.pl/wzor/2020/05/08/9393/}Naglowek"
    )
    ET.SubElement(
        naglowek_element,
        "{http://crd.gov.pl/wzor/2020/05/08/9393/}KodFormularza",
        kodSystemowy="JPK_WB",
        wersjaSchemy="1-0",
    ).text = naglowek.kod_formularza
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}WariantFormularza"
    ).text = str(naglowek.wariant_formularza)
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}CelZlozenia"
    ).text = naglowek.cel_zlozenia
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}DataWytworzeniaJPK"
    ).text = naglowek.data_wytworzenia_jpk.strftime("%Y-%m-%dT%H:%M:%S")
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}DataOd"
    ).text = naglowek.data_od.strftime("%Y-%m-%d")
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}DataDo"
    ).text = naglowek.data_do.strftime("%Y-%m-%d")
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}DomyslnyKodWaluty"
    ).text = naglowek.domyslny_kod_waluty
    ET.SubElement(
        naglowek_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}KodUrzedu"
    ).text = naglowek.kod_urzedu

    podmiot_element = ET.SubElement(
        root, "{http://crd.gov.pl/wzor/2020/05/08/9393/}Podmiot1"
    )
    identyfikator_podmiotu_element = ET.SubElement(
        podmiot_element,
        "{http://crd.gov.pl/wzor/2020/05/08/9393/}IdentyfikatorPodmiotu",
    )
    ET.SubElement(
        identyfikator_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}NIP"
    ).text = podmiot.nip
    ET.SubElement(
        identyfikator_podmiotu_element,
        "{http://crd.gov.pl/wzor/2020/05/08/9393/}PelnaNazwa",
    ).text = podmiot.pelna_nazwa
    ET.SubElement(
        identyfikator_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}REGON"
    ).text = podmiot.regon
    adres_podmiotu_element = ET.SubElement(
        podmiot_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}AdresPodmiotu"
    )
    ET.SubElement(
        adres_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}Ulica"
    ).text = podmiot.ulica
    ET.SubElement(
        adres_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}NrDomu"
    ).text = podmiot.nr_domu
    ET.SubElement(
        adres_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}NrLokalu"
    ).text = podmiot.nr_lokalu
    ET.SubElement(
        adres_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}Miejscowosc"
    ).text = podmiot.miejscowosc
    ET.SubElement(
        adres_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}KodPocztowy"
    ).text = podmiot.kod_pocztowy
    ET.SubElement(
        adres_podmiotu_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}Poczta"
    ).text = podmiot.poczta

    numer_rachunku_element = ET.SubElement(
        root, "{http://crd.gov.pl/wzor/2020/05/08/9393/}NumerRachunku"
    )
    numer_rachunku_element.text = numer_rachunku.numer_rachunku

    salda_element = ET.SubElement(
        root, "{http://crd.gov.pl/wzor/2020/05/08/9393/}Salda"
    )
    saldo_poczatkowe_element = ET.SubElement(
        salda_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}SaldoPoczatkowe"
    )
    saldo_poczatkowe_element.text = str(salda.saldo_poczatkowe)
    saldo_koncowe_element = ET.SubElement(
        salda_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}SaldoKoncowe"
    )
    saldo_koncowe_element.text = str(salda.saldo_koncowe)

    for wiersz in wyciag_wiersze:
        wyciag_wiersz_element = ET.SubElement(
            root, "{http://crd.gov.pl/wzor/2020/05/08/9393/}WyciagWiersz"
        )
        ET.SubElement(
            wyciag_wiersz_element,
            "{http://crd.gov.pl/wzor/2020/05/08/9393/}NumerWiersza",
        ).text = str(wiersz.numer_wiersza)
        ET.SubElement(
            wyciag_wiersz_element,
            "{http://crd.gov.pl/wzor/2020/05/08/9393/}DataOperacji",
        ).text = wiersz.data_operacji
        ET.SubElement(
            wyciag_wiersz_element,
            "{http://crd.gov.pl/wzor/2020/05/08/9393/}NazwaPodmiotu",
        ).text = wiersz.nazwa_podmiotu
        ET.SubElement(
            wyciag_wiersz_element,
            "{http://crd.gov.pl/wzor/2020/05/08/9393/}OpisOperacji",
        ).text = wiersz.opis_operacji
        ET.SubElement(
            wyciag_wiersz_element,
            "{http://crd.gov.pl/wzor/2020/05/08/9393/}KwotaOperacji",
        ).text = str(wiersz.kwota_operacji)
        ET.SubElement(
            wyciag_wiersz_element,
            "{http://crd.gov.pl/wzor/2020/05/08/9393/}SaldoOperacji",
        ).text = str(wiersz.saldo_operacji)

    wyciag_ctrl_element = ET.SubElement(
        root, "{http://crd.gov.pl/wzor/2020/05/08/9393/}WyciagCtrl"
    )
    ET.SubElement(
        wyciag_ctrl_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}LiczbaWierszy"
    ).text = str(wyciag_ctrl.liczba_wierszy)
    ET.SubElement(
        wyciag_ctrl_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}SumaObciazen"
    ).text = str(wyciag_ctrl.suma_obciazen)
    ET.SubElement(
        wyciag_ctrl_element, "{http://crd.gov.pl/wzor/2020/05/08/9393/}SumaUznan"
    ).text = str(wyciag_ctrl.suma_uznan)

    save_xml_to_file(root, file_path)


def save_xml_to_file(xml_element, file_path):
    xml_string = ET.tostring(xml_element, encoding="utf-8", xml_declaration=False)
    xml_string_pretty = xml.dom.minidom.parseString(xml_string).toprettyxml()

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xml_string_pretty)
