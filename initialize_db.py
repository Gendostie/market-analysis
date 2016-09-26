#!/usr/bin/python
from DbConnection import DBConnection
import ManagerCompany
import finsymbols


def insert_company_snp500():
    snp500 = finsymbols.get_sp500_symbols()
