# market-analysis

## Version language
- Python 3.4
- MySql server 5.7 (https://dev.mysql.com/downloads/installer/)
  To get same configuration MySql: 
    - user: root
    - password: root
- Qt 4.8, you can have the most recent version

## Python packages
- Use `pip install -r requirements.txt` to install all required packages.
- To check which packages to install on your system, use `pip freeze -r requirements.txt`
- To update, use `pip install -r requirements.txt -U`

## Interface QT
- To be able to use Qt in Python, we are using PyQt4. It converts a ui file into a python file.
    - We use the function `QT/convert_ui_to_py.bat` to make this conversion more easily.
- To install PyQt4, go to https://www.riverbankcomputing.com/software/pyqt/download

## DbConnexion.py
Create a connexion to a MySql database.
Two functions can be used:

    - select_in_db(self, query, params=None)
    - modified_db(self, query, params=None)

## Installation
1. `pip install -r requirements.txt` to install packages and add -U to 
   update package.
2. Verify that only `install_db` is True in `config.ini`.
3. Execute the script `Install_DB/installer.py` to create the database
4. You are ready to begin.
