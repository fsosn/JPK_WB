# JPK_WB

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

## About The Project

A tool for processing bank statements, generating XML reports compliant with JPK_WB format and storing processed data in database.

### Built With
* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)

## Getting Started

This section provides step-by-step instructions on how to set up the project locally.

### Prerequisites

Ensure you have the following installed on your local machine:
* Python
* Microsoft SQL Server

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/fsosn/JPK_WB.git
   ```
2. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up database tables with db/create_tables_wb.sql script on your MSSQL server
4. Configure environment variables
   ```sh
   DB_SERVER = 
   DB_NAME = 
   DB_USERNAME = 
   DB_PASSWORD = 
   ```

## Usage

The JPK_WB XML Report Generator can be used to:

* Load files with data about subject, account and financial operations
* Validate input data
* Convert data to the appropriate format
* Generate XML reports compliant with JPK_WB


How to use the app:
1. Run the main script:
   ```sh
   python src/main.py
   ```
2. Follow the prompts to provide the paths to the input files containing data about the entity, account, and operations.
3. Select the purpose of submission by entering the corresponding number:
1: Submission of information at the request of the tax authority
2: Submission of information at the taxpayer's request
3: Submission of correction
4: Submission of information for other reasons
4. Enter the start date.
5. Enter the end date.
6. Once the data is processed, the generator will provide feedback regarding the validity of the entity, account and operations data.
7. Upon successful processing, the generator will create an XML file containing the JPK_WB report. The path to the generated file will be displayed in the terminal.

Example:
   ```sh
PS C:\JPK_WB> python .\src\main.py
Podaj ścieżkę do pliku z danymi podmiotu: data/input/podmiot.txt
Podaj ścieżkę do pliku z danymi rachunku: data/input/rachunek.txt
Podaj ścieżkę do pliku z danymi operacji: data/input/operacje.txt
Cel złożenia:
1 - Złożenie informacji na żądanie organu podatkowego
2 - Złożenie informacji na wniosek podatnika
3 - Złożenie korekty
4 - Złożenie informacji z innych przyczyn
Wybierz cel złożenia (1-4): 2
Podaj datę początkową (DD.MM.RRRR): 01.03.2024
Podaj datę końcową (DD.MM.RRRR): 31.03.2024
Wygenerowano plik XML: C:\JPK_WB\data\output\JPK_WB_1234567890_202404191412.xml
   ```
