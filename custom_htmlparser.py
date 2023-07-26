from html.parser import HTMLParser

''' 
    A custom HTML parser for parsing currency pairs and it's data from a table 
'''


class customHTMLParser(HTMLParser):
    def __init__(self, desired_headers):
        super().__init__()
        self.desired_headers = desired_headers
        self.header_positions = []
        self.header_col_selected = 0
        self.data = {}
        self.curr_data = ''
        self.inside_table = False
        self.inside_theader = False
        self.inside_tbody = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for attr in attrs:
                # Find the correct table in website
                if len(attr) >= 2 and attr[0] == 'data-test' and attr[1] == 'historical-prices':
                    self.inside_table = True

        elif self.inside_table:
            if tag == 'thead':
                self.inside_theader = True
            elif tag == 'tbody':
                self.inside_tbody = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.inside_table = False
        elif self.inside_table:
            if tag == 'thead':
                self.inside_theader = False
            elif tag == 'tbody':
                self.inside_tbody = False

    def _parse_header(self, header_item):
        """ Stores the position of each of the requested columns in list """

        if header_item and type(header_item) == str:

            # To remove the * at the end of 'Close' header in website's table
            cleaned_header = header_item.replace('*', '')

            if cleaned_header in self.desired_headers:
                self.header_positions.append(cleaned_header)
                return

        # To ignore non-relevant columns and save it's position
        self.header_positions.append(None)

    def _data_parser(self, curr_data, first_item=True):
        """ Store data into data list """
        try:
            if curr_data:
                if first_item:
                    self.data[curr_data] = []
                    # Store the position of data to use bellow in next call, Ex. Date
                    self.curr_data = curr_data

                else:
                    self.data[self.curr_data].append(curr_data)
        except AttributeError:
            # Calls again but as a first element
            self._data_parser(curr_data)
        except Exception as e:
            print(f'Error parsing value {curr_data}! {e}')

    def _parse_checker(self):
        """ Check if current location in table is one to be parsed """

        if self.header_col_selected >= len(self.header_positions):
            self.header_col_selected = 0

        '''
            header_positions mimic original table but erase the header of not 
            required columns, so if a header is present, it should be parsed
        '''
        result = len(self.header_positions) > 0 and self.header_positions[self.header_col_selected]

        self.header_col_selected += 1
        return bool(result)

    def _parse_table(self, curr_data):
        """ Verify if selected data is one requested, if so, append it to data """
        if self._parse_checker():
            self._data_parser(curr_data, self.header_col_selected == 1)

    def handle_data(self, data):
        """ Calls the parse of the table with currency history """

        # Dynamically identifies the position of the columns to be parsed
        if self.inside_theader:
            self._parse_header(data)

        elif self.inside_tbody:
            self._parse_table(data)
