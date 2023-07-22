import requests
from html.parser import HTMLParser


''' 
    Yahoo Finance currencies scraper 
    It doesn't use external modules for web crawling/web scraping or data manipulation
'''


PATH = 'https://finance.yahoo.com/quote/{}%3DX/history?p={}%3DX'
PAIRS = ['BRLUSD', 'EURUSD', 'CHFUSD', 'EURCHF']
PARSE_DATA = ['Date', 'Open', 'High', 'Low', 'Close*']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'
}


class customHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {PARSE_DATA[0]: PARSE_DATA[1:]}
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
        if data in PARSE_DATA:
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


def main():
    currencies = {}
    parser = customHTMLParser()

    for pair in PAIRS:

        # Headers are necessary in order to not receive a 404 error
        response = requests.get(PATH.format(pair, pair), headers=headers)

        parser.feed(response.text)
        currencies[pair] = parser.data

    print(currencies.keys())


if __name__ == '__main__':
    main()
