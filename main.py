import json
import requests
from html.parser import HTMLParser
from database_handler import DatabaseHandler

''' 
    Yahoo Finance currencies scraper 
    It doesn't use external modules for web crawling/web scraping or data manipulation
'''


class customHTMLParser(HTMLParser):
    def __init__(self, pair_data):
        super().__init__()
        self.pair_data = pair_data
        self.data = {}
        self.key = []
        self.table_header = []
        self.col_selected = 0
        self.inside = False
        self.header = False
        self.table = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for attr in attrs:
                if attr[0] == 'data-test' and attr[1] == 'historical-prices':
                    self.inside = True

        elif self.inside:
            if tag == 'thead':
                self.header = True
            elif tag == 'tbody':
                self.table = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.inside = False
        elif self.inside:
            if tag == 'thead':
                self.header = False
            if tag == 'tbody':
                self.table = False
                
    def parse_header(self, data):
        # To disregard the * at the end of 'Close' header
        if data.replace('*', '') in self.pair_data:
            self.table_header.append(data)
        else:
            # To ignore non-relevant columns in any order
            self.table_header.append(None)

    def parse_table(self, data):
        if self.col_selected == len(self.table_header):
            self.col_selected = 0

        if self.table_header[self.col_selected]:
            if self.col_selected == 0:
                self.key = data
                self.data[data] = []
            else:
                self.data[self.key].append(data)

        self.col_selected += 1
        
    def handle_data(self, data):
        
        # To dynamically identify the columns to be parsed
        if self.header:
            self.parse_header(data)

        elif self.table:
            self.parse_table(data)


def load_scraper_config(name='config'):
    try:
        with open(f'{name}.json') as f:
            config = json.load(f)
            return config['scraper']

    except FileNotFoundError:
        print(f"File with scraper configuration not found! {name}.json must be present in current folder.")

    except Exception as e:
        print(f"Error loading scraper configs! {e.__str__()}")


def main():
    settings = load_scraper_config()

    currencies = {}
    parser = customHTMLParser(settings['pair-data'])

    for pair in settings['currency-pairs']:

        # Headers are necessary in order to not receive a 404 error
        response = requests.get(settings['website'].format(pair, pair), headers=settings['header'])

        parser.feed(response.text)
        currencies[pair] = parser.data

    with DatabaseHandler('currencies_db.db') as dbh:
        dbh.insert_data(currencies)
        print(dbh.get_table())


if __name__ == '__main__':
    main()
