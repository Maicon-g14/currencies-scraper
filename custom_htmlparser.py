from html.parser import HTMLParser

''' 
    A custom HTML parser for parsing currency pairs and it's data from a table 
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
                # Find the correct table in website
                if len(attr) >= 2 and attr[0] == 'data-test' and attr[1] == 'historical-prices':
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
        """ Stores the position of each of the requested columns in table_header """

        # Disregard the * at the end of 'Close' header in website's table
        if data and type(data) == str and data.replace('*', '') in self.pair_data:
            self.table_header.append(data)
        else:
            # To ignore non-relevant columns and save it's position
            self.table_header.append(None)

    def parse_table(self, data_key):
        """ Verify if current column of the table is one of the requested, if so, append it to data """

        if self.col_selected >= len(self.table_header):
            self.col_selected = 0

        if self.table_header[self.col_selected]:
            if self.col_selected == 0:
                self.key = data_key     # Store the position of data to use bellow in next call
                self.data[data_key] = []
            else:
                self.data[self.key].append(data_key)

        self.col_selected += 1

    def handle_data(self, data):
        """ Calls the parse of the table with currency history """

        # Dynamically identifies the position of the columns to be parsed
        if self.header:
            self.parse_header(data)

        elif self.table:
            self.parse_table(data)
