CREATE TABLE Podmiot (
    IdPodmiotu INT PRIMARY KEY IDENTITY(1, 1),
    NIP NVARCHAR(10) UNIQUE NOT NULL,
    PelnaNazwa NVARCHAR(50) UNIQUE NOT NULL,
    REGON NVARCHAR(14) UNIQUE NOT NULL,
    KodKraju NVARCHAR(2) NOT NULL,
    Wojewodztwo NVARCHAR(50) NOT NULL,
    Powiat NVARCHAR(50) NOT NULL,
    Gmina NVARCHAR(50) NOT NULL,
    Ulica NVARCHAR(50) NOT NULL,
    NrDomu NVARCHAR(10) NOT NULL,
    NrLokalu NVARCHAR(10) NOT NULL,
    Miejscowosc NVARCHAR(50) NOT NULL,
    KodPocztowy NVARCHAR(10) NOT NULL,
    Poczta NVARCHAR(50) NOT NULL
);

CREATE TABLE NumerRachunku (
    NumerRachunku NVARCHAR(50) PRIMARY KEY,
    IdPodmiotu INT NOT NULL,
    FOREIGN KEY (IdPodmiotu) REFERENCES Podmiot(IdPodmiotu)
);

CREATE TABLE Naglowek (
    IdNaglowka INT PRIMARY KEY IDENTITY(1, 1),
    KodFormularza NVARCHAR(10) NOT NULL,
    WariantFormularza INT NOT NULL,
    CelZlozenia INT NOT NULL,
    DataWytworzeniaJPK DATETIME NOT NULL,
    DataOd DATETIME NOT NULL,
    DataDo DATETIME NOT NULL,
    DomyslnyKodWaluty NVARCHAR(10) NOT NULL,
    KodUrz � du INT NOT NULL,
    NumerRachunku NVARCHAR(50) NOT NULL,
    FOREIGN KEY (NumerRachunku) REFERENCES NumerRachunku(NumerRachunku)
);

CREATE TABLE Salda (
    IdNaglowka INT NOT NULL,
    SaldoPoczatkowe DECIMAL(18, 2) NOT NULL,
    SaldoKoncowe DECIMAL(18, 2) NOT NULL,
    FOREIGN KEY (IdNaglowka) REFERENCES Naglowek(IdNaglowka)
);

CREATE TABLE WyciagWiersz (
    NumerWiersza INT NOT NULL,
    DataOperacji DATETIME NOT NULL,
    NazwaPodmiotu NVARCHAR(50) NOT NULL,
    OpisOperacji NVARCHAR(50) NOT NULL,
    KwotaOperacji DECIMAL(18, 2) NOT NULL,
    SaldoOperacji DECIMAL(18, 2) NOT NULL,
    IdNaglowka INT NOT NULL,
    PRIMARY KEY (NumerWiersza, IdNaglowka),
    FOREIGN KEY (IdNaglowka) REFERENCES Naglowek(IdNaglowka)
);

CREATE TABLE WyciagCtrl (
    LiczbaWierszy INT NOT NULL,
    SumaObciazen DECIMAL(18, 2) NOT NULL,
    SumaUznan DECIMAL(18, 2) NOT NULL,
    IdNaglowka INT NOT NULL,
    FOREIGN KEY (IdNaglowka) REFERENCES Naglowek(IdNaglowka)
);