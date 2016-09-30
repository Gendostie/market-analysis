#!/usr/bin/python
import ManagerCompany
import finsymbols


def insert_company_snp500():
    """
    Insert company s&p500 in table company
    :return: None
    """
    snp500 = finsymbols.get_sp500_symbols()

    for company in snp500:
        ManagerCompany.add_company_to_db(company.get('symbol'), company.get('company'))
