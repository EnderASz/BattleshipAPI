# BattleshipAPI
__[For english version of 'README.md' click here](./README-eng.md)__

Projekt ten jest efektem wykonania zadania, otrzymanego w procesie rekrutacji na stanowisko Backend Developera do toruńskiego Software House'u [SPTech](https://sptech.pl/).

W dużym skrócie, zadanie polegało na stworzeniu HTTP API pozwalającego na przeprowadzenie rozgrywki w "statki", w języku Python, przy użyciu technologii Flask lub FastAPI oraz z zastosowaniem zasad i reguł REST.
Dodatkowym atutem miało być użycie systemu relacyjnych baz danych SQL oraz biblioteki SQLAlchemy, do czego się zastosowałem.

## Użyte technologie
- Python
- FastAPI
- SQLAlchemy
- Inne biblioteki języka Python wymienione w pliku `requirements.txt`
- PostgreSQL

Do uruchamiania aplikacji w procesie tworzenia aplikacji, wykorzystano `Uvicorn`.

## Podstawowa instalacja
1. Sklonuj to repozytorium: `git clone https://github.com/EnderASz/BattleshipAPI.git`

2. Przejdź do ścieżki sklonowanego repozytorium (najczęściej poprzez polecenie `cd battleship_api`)

- Jeżeli chcesz użyć wirtualnego środowiska stwórz je oraz aktywuj przed następnymi czynnościami

3. Użyj polecenia `pip3 install -r requirements.txt` w celu pobrania i zainstalowania wymaganych paczek języka Python

4. Przejdź do [Konfiguracji](#Konfiguracja) i przygotuj ustawienia aplikacji poprzez zmienne środowiskowe (można również wykorzystać plik `.env`) lub plik konfiguracyjny znajdujący się pod ścieżką wskazaną przez zmienną środowiskową `battleship_api_config_path`.

## Konfiguracja
Cała poniższa konfiguracja, jest możliwa zarówno poprzez umieszczenie odpowiednich zmiennych w pliku konfiguracyjnym lub poprzez stworzenie odpowiadających im zmiennych środowiskowych (również poprzez plik `.env`).

W przypadku użycia zmiennych środowiskowych, nazwa zmiennej powinna być poprzedzona przedrostkiem `battleship_api_`. Naprzykład `battleship_api_port`.
|Nazwa zmiennej|Wartość domyślna|Opcjonalna|Opis|
|-------------|-------------|--------|-----------|
|port|`80`|:white_check_mark:|Port z którego chcesz udostępnić dostęp do aplikacji|
|host|`127.0.0.1`|:white_check_mark:|Adres hosta z którego aplikacja ma być uruchomiona|
|debug|`True`|:white_check_mark:|Przełącznik decydujący czy aplikacja ma być uruchomiona w trybie debugowania
|db_url|`sqlite:///./db.sqlite3`|:x:|URL połączenia z bazą danych (SQLite lub PostgreSQL)
|db_check_same_thread|:heavy_minus_sign:|Wymagany przy użyciu bazy danych SQLite.|W przypadku użycia bazy danych SQLite zalecane jest, aby wartość ta była ustawiona na `False`. Po więcej informacji przejdź [tutaj](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/?h=check_same_thread#note).
|secret_key|Domyślnie używany jest predefiniowany klucz|:white_check_mark:|Sekretny klucz dla instancji aplikacji.<br>**Rekomendowane jest, aby wprowadzić własny oraz przechowywać go w sekrecie.**

## Podstawowe uruchomienie aplikacji
W celu uruchomienia aplikacji wystarczy uruchomić plik `runserver.py` za pomocą zainstalowanego środowiska Python.
```cmd
python3 runserver.py
```
