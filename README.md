# market-analysis

## Version language
- Python 2.7
- MySql server 5.7 (https://dev.mysql.com/downloads/installer/)
  To get same configuration MySql: 
    - user: root
    - password: root

## Package python to need
- mysqldb (https://sourceforge.net/projects/mysql-python/)
- findsymbols
- pandas
    - Numpy must be installed already
    - Cython and pytz must be possible installed too
- requests

## Export data base MySql
First time, must be create schema before export db. After, to update bd,
pass to step 2.
1. Create schema `market_analysis`
    - CREATE SCHEMA 'market_analysis';
2. Export table sql
    - Click ``Data import/restore``
    - Choice `\market-analysis\DB` of your Git `market_analysis`
    - Start import

## DbConnexion.py
Create a connexion to db MySql.
Two functions can using:

    - select_in_db(self, query, params=None)
    - modified_db(self, query, params=None)
