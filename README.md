# Currencies Scraper App

A Python application that scrapes the last 30 daily currency prices from Yahoo Finance, filter it and stores into a database.

It **doesn't** use external specific libraries, like the ones focused on web scraping (BeautifulSoup, Selenium, etc). Instead, it relies more in strongly programming logic, but also in these not so high level libraries:
- Python requests
- HTMLParser
- SQLite 3
- Pytest
- JSON

The application were developed with a focus in maintainability and testability, doing so, it has many tests coverage, use of good practices and some considerable level of abstraction and customization.

This app is fully capable of scraping any available pair and it's parameters in any website, needing only a table specified by a certain key-value that is user defined. All customizable actions can be set in `settings.json`. Being those:

- Change of URL to parse
- Selection of table to parse (useful in websites with multiple tables)
- Addition/Removal of pairs to parse
- Specific selection of whose pairs from table should be parsed
- Path to store database
- Database's name
- Database's table's name
- And type of the data that will be stored in database

The program also features a method to exhibit the data parsed loading it from the saved database.

## How to run

To run the app, besides having Python 3, you will also need Python Requests and Pytest installed. Once so, simply run in your console:

On Linux: `python3 main.py`

On Windows: `python main.py`

## Some Examples

Here are some examples of the collected/processed data:

<details>
    <summary>Show some examples</summary>

    Some Timeseries:

    

    A correlation Heatmap:


    
</details>

### Links: 

[Jupyter Notebook](data/data_ploting.ipynb)

[SQL Database](data/currencies_db.db)
