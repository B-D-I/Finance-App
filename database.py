from utils import *


class Database:

    def __init__(self):
        self.conn = sqlite3.connect('finance_database')
        self.c = self.conn.cursor()

    @staticmethod
    def create_and_return_cache(ticker: str, start: dt, reference: str):
        """
        Provide an SQLite cache of query
        :param ticker: ticker name
        :param start: start date
        :param reference: further reference for naming
        :return: cached session
        """
        cache_expire_after = dt.timedelta(days=3)
        session = requests_cache.CachedSession(cache_name=f'{ticker}_{reference}_{str(start.date())}', backend='sqlite',
                                               expire_after=cache_expire_after)
        session.headers = DEFAULT_HEADERS
        return session

    def get_db_data(self, table_name: str, col_name: str,  value: Union[str, int]):
        try:
            self.c.execute(f"SELECT * FROM {table_name} WHERE {col_name} = '{value}'")
            rows = self.c.fetchone()
        except sqlError or ValueError as error:
            print(error)
        return rows

    def get_all_table_data(self, table_name: str):
        try:
            self.c.execute(f"SELECT * FROM {table_name}")
            rows = self.c.fetchall()
        except sqlError or ValueError as error:
            print(error)
        return rows

    def insert_db(self, table_name: str, col1_value: str, col2_value: Union[str, int]):
        if table_name == 'user':
            col1 = 'username'
            col2 = 'password'
        if table_name == 'portfolio':
            col1 = 'ticker_name'
            col2 = 'share_amount'
        try:
            self.c.execute(f"INSERT INTO {table_name} ({col1}, {col2}) VALUES ( '{col1_value}', '{col2_value}' )")
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        self.conn.close()

    def update_db(self, table_name: str, col_name: str, new_value: Union[int, str], reference_col: str, reference_value: Union[int, str]):
        try:
            self.c.execute(f"UPDATE {table_name} SET {col_name} = '{new_value}' WHERE {reference_col} = '{reference_value}'")
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        self.conn.close()

    def delete_from_db(self, table_name: str, col_name: str, col_value: Union[str, int]):
        try:
            self.c.execute(f"DELETE FROM {table_name} WHERE {col_name} = '{col_value}'")
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        self.conn.close()

    def create_db(self):
        try:
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS portfolio ([portfolio_id] INTEGER PRIMARY KEY,
            [ticker_name] TEXT, [share_amount] INTEGER)
            """)
            self.conn.commit()
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS user ([user_id] INTEGER PRIMARY KEY, [username] TEXT, [password] TEXT)
            """)
            self.conn.commit()
            self.c.execute(("""
            INSERT INTO user (username, password) VALUES ('admin', 'change-me')
            """))
            self.conn.commit()
        except sqlError as error:
            print(error)



