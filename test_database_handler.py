import sqlite3
from database_handler import DatabaseHandler


# Test creation of table
def test_db_create_table():
    with DatabaseHandler(':memory:') as dbh:
        dbh.insert_data({})

        try:
            dbh.cursor.execute('SELECT * FROM currencies')
            assert True

        except sqlite3.OperationalError:
            assert False


# Test insertion of data into table
def test_db_insert_data():
    with DatabaseHandler(':memory:') as dbh:
        data = {
            'BRLUSD' : {
                'Sep 28, 2020': [0.1799, 0.1814, 0.1779, 0.1798],
                'Nov 28, 2022': [0.1850, 0.1864, 0.1844, 0.1849],
            }
        }

        dbh.insert_data(data)

        try:
            dbh.cursor.execute('SELECT * FROM currencies WHERE ticker=\'BRLUSD\'')
            result = dbh.cursor.fetchall()
            assert len(result) == 2
            assert result[0][1] == 'Sep 28, 2020'
            assert result[0][2] == 0.1799
            assert result[1][1] == 'Nov 28, 2022'
            assert result[1][5] == 0.1849
        except Exception:
            assert False


# Test data requisition from table
def test_db_get_table():
    with DatabaseHandler(':memory:') as dbh:
        data = {
            'BRLUSD' : {
                'Sep 28, 2020': [0.1799, 0.1814, 0.1779, 0.1798],
                'Nov 28, 2022': [0.1850, 0.1864, 0.1844, 0.1849],
            }
        }

        dbh.insert_data(data)

        result = dbh.get_table()

        assert len(result) == 2
        assert result[0][0] == 'BRLUSD'
        assert result[0][1] == 'Sep 28, 2020'
        assert result[0][2] == 0.1799
        assert result[1][0] == 'BRLUSD'
        assert result[1][1] == 'Nov 28, 2022'
        assert result[1][5] == 0.1849
