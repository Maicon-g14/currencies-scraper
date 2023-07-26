import sqlite3

''' 
    A database handler to storage scraped currencies into SQLite db
'''


class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name

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

    def _create_table(self, name):
        try:
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
                                        ticker TEXT, 
                                        date TEXT, 
                                        open REAL, 
                                        high REAL, 
                                        low REAL, 
                                        close REAL
                                    )'''
                                )
            print(f'Table \'{name}\' has been created successfully!')

        except sqlite3.Error as e:
            raise RuntimeError(f'Error creating \'{name}\' table! {e}')

    def insert_data(self, data, table_name='currencies'):
        try:
            self._create_table(table_name)

            for item in data:
                for inner_item in data[item]:

                    self.cursor.execute(f'''INSERT INTO {table_name} VALUES (
                                                ?, ?, ?, ?, ?, ?
                                            )''', (
                                                item,
                                                inner_item,
                                                data[item][inner_item][0],
                                                data[item][inner_item][1],
                                                data[item][inner_item][2],
                                                data[item][inner_item][3]
                                            )
                                        )
            print('Data saved successfully!')

        except sqlite3.Error as e:
            raise RuntimeError(f'Error inserting data into \'{table_name}\'! {e}')

    def get_table(self, table_name='currencies'):
        try:
            self.cursor.execute(f'SELECT * FROM {table_name}')
            return self.cursor.fetchall()

        except sqlite3.Error as e:
            raise RuntimeError(f'Error fetching data from \'{table_name}\'! {e}')
