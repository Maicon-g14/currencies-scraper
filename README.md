# Currencies Scraper App

A Python application that scrapes daily currency prices from Yahoo Finance and stores it into a database.

It **doesn't** use external specific libraries, like the ones focused on web scraping/web crawling. Instead, it was more of a challenge relying only on:
- Python requests
- HTMLParser
- SQLite 3
- Pytest
- JSON

The application have coverage in unitary tests, and I tried to always maintain the use of good practices, focusing more in maintainability and testability.

This app is capable of scraping any available pair in yfinance by specifying it in `config.json`. There you will also find an option to customize the desired fields that should be parsed from the website's pair table.

## How to run

To run the app, besides having Python 3, you will also need Requests and Pytest installed. Once so, simply run in your console:

On Linux: `python3 main.py`

On Windows: `python main.py`

## Some Samples

And here are some examples of the collected data:

<details>
  <summary>Show</summary>
    ![Soon]()
</details>

And a link to the Jupyter Notebook:

[Link]()