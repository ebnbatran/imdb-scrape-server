# IMDB Scraping Server
> My server that scrapes IMDB.com and produce movies information written purely in Python

## "Server" Django App
Has a `models.py` which instructs Django to create the tables for movies information and scraping dates

## Views (Server's URL end points)
Three important views: 
1. home 
2. scrape 
3. search

* **Home** view shows all the scraped data
* **Scrape** view creates a subprocess on the server to launch Scrapy's crawling spider
* **Search** view gets movies by title parameter in the URL query string

## Scrapy's Spider
The crawling spider which starts at **imdb.com**'s search page of the letter 'a' which has around **200K movie** search results
This spider crawles from page to page on the results and delivers all input to the **Pipeline**

## Pipeline
This is the code that recieves the input from the spider and processes it removing any unwanted symbols
Then it inserts the info into the **PostgreSQL** database

## PostgreSQL Database
It is hosted on **Heroku**'s server. The app recieves its URL from the `os.environ` dictionary located on the server itself

> Choosing **PostgreSQL** over other relational DBMSs was purely because **Heroku** prefers to communicate with this specific type, it is also easy to manipulate and very convenient.
