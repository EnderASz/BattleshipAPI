# BattleshipAPI
__[Aby przejść do polskiej wersji 'README.md' naciśnij tutaj](./README.md)__

<!-- TODO -  Project description -->

## Technology Stack
- Python
- FastAPI
- SQLAlchemy
- Other Python libraries mentioned in `requirements.txt`
- PostgreSQL

For running application in development process used `Uvicorn`.

## Basic instalation
1. Clone this repository: `git clone https://github.com/EnderASz/BattleshipAPI.git`

2. Enter into cloned repository directory (usually by `cd battleship_api`)

- If you want to use virtual environment activate it before steps below

3. Run `pip3 install -r requirements.txt` to install required python packages

4. Go to [Configuration](#Configuration) and configure application via environment variables (and/or by creating `.env` file) or in config file setted by `battleship_api_config_path` enviroment variable.

## Configuration
Entire configuration below can be done by creating a configuration file with below variables or by creating environment variables (or putting them into `.env` file).

In case of creating environment variables, name of each variable should starts with `battleship_api_` prefix. For example: `battleship_api_port`.
|Variable name|Default value|Optional|Description|
|-------------|-------------|--------|-----------|
|port|`80`|:white_check_mark:|Port from which you want to publish app|
|host|`127.0.0.1`|:white_check_mark:|Host address from which you want to starts app|
|debug|`True`|:white_check_mark:|Switch deciding whether an application is running in debug mode or not.
|db_url|`sqlite:///./db.sqlite3`|:x:|Database connection string or url
|db_check_same_thread|:heavy_minus_sign:|Required with SQLite database.|In case of use SQLite database it's recommend to set this value to `False`. For more informations look [here](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/?h=check_same_thread#note).
|secret_key|By default application use constant predefined key|:white_check_mark:|Secret Key for application instance.<br>**It's recommended to provide it and keep it in secret.**

## Basic app run
To run application, just run `runserver.py` via installed Python environment.
```cmd
python3 runserver.py
```
