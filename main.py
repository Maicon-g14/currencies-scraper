import json
import requests
from custom_htmlparser import customHTMLParser
from database_handler import DatabaseHandler

''' 
    Yahoo Finance currencies scraper 
    It doesn't use external modules for web crawling/web scraping or data manipulation
'''


def load_scraper_config(name='config'):
    try:
        with open(f'{name}.json') as f:
            config = json.load(f)
            return config['scraper']

    except FileNotFoundError:
        print(f'File with scraper settings not found! {name}.json must be present in current folder.')

    except Exception as e:
        raise RuntimeError(f'Error loading scraper settings! {e}')


def parse_currencies(settings):
    """ Parses yfinance webpage for each currency pair and store requested data """
    try:
        if not settings:
            raise RuntimeError(f'Required settings not found!')

        currencies = {}

        for pair in settings['currency-pairs']:
            source = settings['website'].format(pair, pair)
            parser = customHTMLParser(settings['pair-data'])

            print(f'Parsing data from: {source}')

            # Headers are necessary in order to not receive a 404 error
            response = requests.get(source, headers=settings['header'])

            # Feed and process acquired data
            parser.feed(response.text)
            currencies[pair] = parser.data

            print("Data parsed successfully!")
            parser.reset_parsing()

        return currencies
    except Exception as e:
        raise RuntimeError(f'Error while scraping currencies! {e}')


def save_currencies(currencies, filename='currencies_db.db'):
    """ Save scraped currencies into database """

    with DatabaseHandler(filename) as dbh:
        dbh.insert_data(currencies)
        # print(dbh.get_table())


def main():
    settings = load_scraper_config()
    currencies = parse_currencies(settings)
    save_currencies(currencies)


if __name__ == '__main__':
    main()
