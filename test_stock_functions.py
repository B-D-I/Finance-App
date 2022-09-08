import unittest
import datetime as dt
import stock_analysis

start_date = dt.datetime(2021, 1, 20)
end_date = dt.datetime(2022, 1, 20)


class TestStockFunctions(unittest.TestCase):

    def test_return_date_difference(self):
        result = stock_analysis.return_date_difference(start_date, end_date)
        self.assertEqual(result, 12)
        self.assertNotEqual(result, 1)

