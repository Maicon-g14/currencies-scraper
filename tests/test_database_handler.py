import pytest
import sqlite3
from database_handler import DatabaseHandler
from main import load_settings


# Fixture to initialize settings
@pytest.fixture
def settings():
    settings = load_settings('../settings')['database']
    settings['db-path'] = ''
    settings['db-name'] = ':memory:'

    return settings


# Test creation of table
def test_db_create_table(settings):
    with DatabaseHandler(settings) as dbh:
        dbh.insert_currency({})

        try:
            dbh.cursor.execute(f'SELECT * FROM {settings["table-name"]}')
            assert True

        except sqlite3.OperationalError:
            assert False


# Test insertion of data into table
def test_db_insert_currency(settings):
    with DatabaseHandler(settings) as dbh:
        data = {
            'BRLUSD' : {
                'Sep 28, 2020': [0.1799, 0.1814, 0.1779, 0.1798],
                'Nov 28, 2022': [0.1850, 0.1864, 0.1844, 0.1849],
            }
        }

        dbh.insert_currency(data)

        try:
            dbh.cursor.execute(f'SELECT * FROM {settings["table-name"]}')
            result = dbh.cursor.fetchall()
            assert len(result) == 2
            assert result[0][1] == 'Sep 28, 2020'
            assert result[0][2] == 0.1799
            assert result[1][1] == 'Nov 28, 2022'
            assert result[1][5] == 0.1849
        except Exception:
            assert False


# Test data requisition from table
def test_db_get_currencies(settings):
    with DatabaseHandler(settings) as dbh:
        data = {
            'BRLUSD' : {
                'Sep 28, 2020': [0.1799, 0.1814, 0.1779, 0.1798],
                'Nov 28, 2022': [0.1850, 0.1864, 0.1844, 0.1849],
            }
        }

        dbh.insert_currency(data)

        result = dbh.get_currencies()

        assert len(result) == 2
        assert result[0][0] == 'BRLUSD'
        assert result[0][1] == 'Sep 28, 2020'
        assert result[0][2] == 0.1799
        assert result[1][0] == 'BRLUSD'
        assert result[1][1] == 'Nov 28, 2022'
        assert result[1][5] == 0.1849
