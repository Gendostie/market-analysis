# market-analysis

## Version language
- Python 3.4
- MySql server 5.7 (https://dev.mysql.com/downloads/installer/)
  To get same configuration MySql: 
    - user: root
    - password: root

## Package python to need
- To install, use `pip install -r requirements.txt` to install all package required
- To check package required in your system, use `pip freeze -r requirements.txt`
- To update, use `pip install -r requirements.txt -U`

## Interface QT
- We use PyQt4 to switch file ui in file py and use language Python
    - We use `QT/convert_ui_to_py.bat` to execute function pyuic4 of Pyt4, 
      most fast to update modification in file ui to file py
- To install PyQt4, go to https://www.riverbankcomputing.com/software/pyqt/download

## Export data base MySql
First time, must be create schema before export db. After, to update bd,
pass to step 2.
1. Create schema `market_analysis`
    - CREATE SCHEMA 'market_analysis';
2. Export table sql
    - Click `Data import/restore`
    - Choice `/market-analysis/DB` of your Git `market_analysis`
    - Start import

## DbConnexion.py
Create a connexion to db MySql.
Two functions can using:

    - select_in_db(self, query, params=None)
    - modified_db(self, query, params=None)

## Installation
1. `pip install -r requirements.txt`, for install package and add -U for 
   update package
2. Check `config.ini` if all value of `[installer]` is to True and :

        [daily]
        day_min = 01
        month_min = 00
        year_min = 2006
        
        [dividend]
        day_min = 01
        month_min = 00
        year_min = 2006
3. Execute script of `Install_DB/installer.py` for create Database
4. You are ready to begin.
