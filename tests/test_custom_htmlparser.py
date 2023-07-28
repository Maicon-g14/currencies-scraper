import pytest
from custom_htmlparser import customHTMLParser
from main import load_settings


# Fixture to initialize the parser
@pytest.fixture
def settings():
    settings = load_settings('../settings')['scraper']
    settings["currency-pairs"] = ["BRLUSD", "EURUSD"]

    return settings


@pytest.fixture
def parser(settings):
    return customHTMLParser(settings)


# Tests recognition of desired html start tags
def test_handle_starttag_true(parser):
    # Should start parsing the table
    parser.handle_starttag('table', [('data-test', 'historical-prices')])
    assert parser.inside_table is True

    # Should start parsing the table's header
    parser.handle_starttag('thead', [])
    assert parser.inside_theader is True

    # Should start parsing the table's body
    parser.handle_starttag('tbody', [])
    assert parser.inside_tbody is True


def test_handle_starttag_false(parser):
    # Case where nothing should happen
    parser.handle_starttag('div', [('class', 'currency')])
    assert parser.inside_table is False
    assert parser.inside_theader is False
    assert parser.inside_tbody is False


# Tests recognition of desired html end tags
def test_handle_endtag_true(parser):
    parser.inside_table = True
    parser.inside_theader = True
    parser.inside_tbody = True

    # Inverse order to short the code

    # Should finish the parsing of table's body
    parser.handle_endtag('tbody')
    assert parser.inside_tbody is False

    # Should finish the parsing of table's header
    parser.handle_endtag('thead')
    assert parser.inside_theader is False

    # Should finish the parsing of the table
    parser.handle_endtag('table')
    assert parser.inside_table is False


def test_handle_endtag_false(parser):
    # Case where nothing should happen
    parser.inside_table = True
    parser.inside_theader = True
    parser.inside_tbody = True

    parser.handle_endtag('div')
    assert parser.inside_table is True
    assert parser.inside_theader is True
    assert parser.inside_tbody is True


# Tests the parsing of table's header
def test_parse_header(parser):
    parser.inside_theader = True
    parser.handle_data('High')
    parser.handle_data('Volume')
    parser.handle_data('')
    # Should remove all the '*'
    parser.handle_data('Low**')

    assert parser.header_positions == ['High', None, None, 'Low']


# Tests the parsing of data on the table
def test_data_parser(parser):
    parser.inside_tbody = True
    parser.header_positions = ['Ticker', 'Date', None, 'High']

    parser.handle_data('January 1, 2023')
    parser.handle_data('0.2345')

    parser.header_col_selected = 0

    parser.handle_data('January 3, 2023')

    assert len(parser.data) == 2
    assert parser.data['January 1, 2023'] == ['0.2345']


# Tests the iteration across the table being parsed
def test_parse_checker_true(parser):
    parser.inside_tbody = True
    parser.header_positions = ['Ticker', 'Date', None, 'High']

    parser.header_col_selected = 0
    parser.handle_data('January 3, 2023')
    assert parser.header_col_selected == 1


def test_parse_checker_false(parser):
    # Cases where nothing should happen
    parser.inside_tbody = True

    # Test out of range index
    parser.header_col_selected = 3
    parser.handle_data('January 3, 2023')
    # It is expected to be 1 because it should iterate by the end of execution
    assert parser.header_col_selected == 1
    assert parser.curr_data == ''
