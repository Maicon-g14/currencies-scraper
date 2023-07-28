import json
import requests
from custom_htmlparser import customHTMLParser
from database_handler import DatabaseHandler

''' 
    YF Currencies Scraper
    
    A web scraping tool that fetches and clean last 30 days of specified 
    pairs data from Yahoo Finance and save it's result into a database 
    for further analysis.
    
    It doesn't use external modules for web scraping or data manipulation, 
    instead it relies strongly in programming logic and focus in 
    maintainability and testability.
    
    Ps. A number of customizations can be made in 'settings.json'.
'''


def load_settings(name='settings'):
    try:
        with open(f'{name}.json') as f:
            return json.load(f)

    except FileNotFoundError:
        print(f'File with program settings not found! {name}.json must be present in current folder.')

    except Exception as e:
        raise RuntimeError(f'Error loading program settings! {e}')


def settings_check(settings):
    if not (settings or settings['scraper'] or settings['database']):
        raise RuntimeError(f'Required settings/settings field(s) not found!')
    return True


def parse_currencies(settings):
    """ Parses yfinance webpage for each currency pair and store requested data """
    try:
        currencies = {}

        for pair in settings['currency-pairs']:
            # Mounts the url of each currency pair
            source = settings['website'].format(pair, pair)

            parser = customHTMLParser(settings)

            print(f'Parsing data from: {source}')

            # Headers are necessary in order to not receive a 404 error
            response = requests.get(source, headers=settings['header'])

            # Feed and process acquired data
            parser.feed(response.text)
            currencies[pair] = parser.data

            print("Data parsed successfully!")

        return currencies
    except Exception as e:
        raise RuntimeError(f'Error while scraping currencies! {e}')


def save_currencies(currencies, settings):
    """ Save scraped currencies into database """
    try:
        with DatabaseHandler(settings) as dbh:
            dbh.insert_currency(currencies)
            # Show data saved on table
            # print(dbh.get_currencies())
    except Exception as e:
        raise RuntimeError(f'Error saving currencies! {e}')


def main():
    settings = load_settings()

    if settings_check(settings):
        currencies = parse_currencies(settings['scraper'])
        save_currencies(currencies, settings['database'])


if __name__ == '__main__':
    main()
