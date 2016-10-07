#!/usr/bin/python
import unittest
from copy import deepcopy

from Manager_DB.DbConnection import DBConnection
from Manager_DB import ManagerCompany
from UnitTest import ManagerDbTest

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'market_analysis_test'


class ManagerCompanyTest(unittest.TestCase):
    __db = None

    @classmethod
    def setUpClass(cls):
        ManagerDbTest.init_db_mysql_test(HOST, USER, PASSWORD, DATABASE)
        cls.__db = DBConnection(HOST, USER, PASSWORD, DATABASE)

        cls.__company = [{'symbol': 'GOOGL', 'name': 'Alphabet Inc Class A', 'last_update_historic': None},
                         {'symbol': 'AMZN', 'name': 'Amazon.com Inc', 'last_update_historic': None},
                         {'symbol': 'AAPL', 'name': 'Apple Inc.', 'last_update_historic': None},
                         {'symbol': 'HRB', 'name': 'Block H&R', 'last_update_historic': None},
                         {'symbol': 'gps', 'name': 'Gap (The)', 'last_update_historic': None}]

    @classmethod
    def tearDownClass(cls):
        ManagerDbTest.drop_db_mysql_test(HOST, USER, PASSWORD, DATABASE, cls.__db)

    def test_1_add_company_to_db(self):
        row_added = 0
        for c in self.__company:
            row_added += ManagerCompany.add_company_to_db(c.get('symbol'), c.get('name'), self.__db)
            c['symbol'] = c.get('symbol').upper()  # uppercase symbol for compare result with expected result

        ManagerCompany.add_company_to_db(self.__company[0].get('symbol'), self.__company[0].get('name'), self.__db)
        self.assertEqual(row_added, len(self.__company), 'It\'s not the number of rows expected in the table Company.')

    def test__2_get_snp500(self):
        res = ManagerCompany.get_snp500(self.__db)
        self.assertEqual(len(res), len(self.__company), 'It\'s not the number of rows expected in the table Company.')
        for r in res:
            self.assertTrue(r in self.__company, 'Not the expected result for %s, res= %s' % (r, res))

    def test_3_get_company_by_symbol(self):
        expected_res = deepcopy(self.__company)
        for c in expected_res:
            res = ManagerCompany.get_company_by_symbol(c.get('symbol'), self.__db)
            c['is_in_snp500'] = b'\x01'
            self.assertTrue(res == [c], 'Not the expected result for %s' % res)
        # company no in table Company
        res = ManagerCompany.get_company_by_symbol('symbol_not_', self.__db)
        self.assertEqual(res, [], 'Not the expected result, we expected a list empty.')
        # with symbol in lowercase
        res = ManagerCompany.get_company_by_symbol(expected_res[0].get('symbol').lower(), self.__db)
        self.assertEqual(res, [expected_res[0]], '%s != %s' % (res, [expected_res[0]]))

    def test_4_get_company_by_name(self):
        expected_res = deepcopy(self.__company)
        for c in expected_res:
            res = ManagerCompany.get_company_by_name(c.get('name'), self.__db)
            c['is_in_snp500'] = b'\x01'
            self.assertTrue(res == [c], 'Not the expected result for %s' % res)
        # company no in table Company
        res = ManagerCompany.get_company_by_name('symbol_not_', self.__db)
        self.assertEqual(res, [], 'Not the expected result, we expected a list empty.')
        # with symbol in lowercase
        res = ManagerCompany.get_company_by_name(expected_res[0].get('name').lower(), self.__db)
        self.assertEqual(res, [expected_res[0]], '%s != %s' % (res, [expected_res[0]]))

if __name__ == '__main__':
    unittest.main()
