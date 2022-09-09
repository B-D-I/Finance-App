import requests


class IEXStocks:

    def __init__(self, token):
        self.BASE_URL = "https://sandbox.iexapis.com/stable"
        self.token = token

    def get_company_data(self, ticker):
        api = f"{self.BASE_URL}/stock/{ticker}/company?token={self.token}"
        data = requests.get(api).json()
        return data

    def get_stats(self, ticker):
        api = f"{self.BASE_URL}/stock/{ticker}/advanced-stats?token={self.token}"
        data = requests.get(api).json()
        return data

    def get_balance_sheet(self, ticker):
        api = f'{self.BASE_URL}/stock/{ticker}/balance-sheet/?token={self.token}'
        data = requests.get(api).json()
        return data

    def get_quote(self, ticker):
        api = f'{self.BASE_URL}/stock/{ticker}/quote/?token={self.token}'
        data = requests.get(api).json()
        return data

