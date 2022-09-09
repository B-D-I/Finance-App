import unittest
import datetime as dt
import analysis
import database
import utils

db = database.Database()
start_date = dt.datetime(2021, 1, 20)
end_date = dt.datetime(2022, 1, 20)


class TestStockFunctions(unittest.TestCase):

    def test_return_date_difference(self):
        result = analysis.return_date_difference(start_date, end_date)
        self.assertEqual(result, 12)
        self.assertNotEqual(result, 1)

    def test_format_number(self):
        result = utils.format_number(123456789)
        correct = '123,456,789'
        incorrect = 123456789
        self.assertEqual(result, correct)
        self.assertNotEqual(result, incorrect)

    def test_return_datetime(self):
        result = utils.return_datetime('01-01-20')
        correct = dt.datetime(2020, 1, 1, 0, 0)
        incorrect = '01-01-20'
        self.assertEqual(result, correct)
        self.assertNotEqual(result, incorrect)

    def test_db_select(self):
        table = 'user'
        col = 'username'
        username = 'admin'
        correct = (1, 'admin', 'change-this')
        result = db.get_db_data(table, col, username)
        self.assertEqual(result, correct)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
