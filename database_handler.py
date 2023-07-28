import sqlite3

''' 
    A database handler to storage scraped currencies into SQLite db
'''


class DatabaseHandler:
    def __init__(self, settings):
        self.db_name = settings['db-name']
        self.table_name = settings['table-name']
        self.table_headers = settings['table-headers']

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return self

        except sqlite3.Error as e:
            raise RuntimeError(f'Error creating the database! {e}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def _create_table(self, name, headers):
        try:
            # It needs to be a list in order to remove last ','
            query_list = list(f'CREATE TABLE IF NOT EXISTS {name} (')

            for header in headers:
                query_list += list(f' {header} {headers[header]},')

            # Add query closing
            query_list[-1] = ')'

            query = "".join(query_list)

            self.cursor.execute(query)
            print(f'Table \'{name}\' has been created successfully!')

        except sqlite3.Error as e:
            raise RuntimeError(f'Error creating \'{name}\' table! {e}')

    def insert_currency(self, data):
        try:
            # Create table only works if table still doesn't exist
            self._create_table(self.table_name, self.table_headers)

            for ticker in data:
                for date in data[ticker]:
                    # Reserve space for ticker and date
                    query = f'INSERT OR IGNORE INTO {self.table_name} VALUES (?, ?'
                    # Each date should have it's exclusive item_list
                    item_list = [ticker, date]

                    for item in data[ticker][date]:
                        # Reserve space for each consequent associated value
                        query += ', ?'
                        item_list.append(item)

                    # Close query
                    query += ')'
                    self.cursor.execute(query, tuple(item_list))
            print('Currency history saved successfully!')

        except sqlite3.Error as e:
            raise RuntimeError(f'Error inserting data into \'{self.table_name}\' table! {e}')

    def get_currencies(self):
        try:
            self.cursor.execute(f'SELECT * FROM {self.table_name}')
            return self.cursor.fetchall()

        except sqlite3.Error as e:
            raise RuntimeError(f'Error fetching data from table \'{self.table_name}\'! {e}')
