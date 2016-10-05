#!/usr/bin/python
import finsymbols

from Manager_DB import ManagerCompany
from Manager_DB.DbConnection import DBConnection

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'


def insert_company_snp500():
    """
    Insert company s&p500 in table company
    :return: None
    """
    snp500 = finsymbols.get_sp500_symbols()

    for company in snp500:
        ManagerCompany.add_company_to_db(company.get('symbol'), company.get('company'))


def init_db_mysql():
    """
    Create schema and table for use the program
    :return: None
    """
    # No Database name, because if not exists, we have an error
    db = DBConnection(HOST, USER, PASSWORD, '')
    query = """Create schema IF NOT EXISTS `market_analysis`"""
    db.modified_db(query)
