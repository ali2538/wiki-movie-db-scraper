# wiki-movie-db-scraper
# A Scraper that uses the list created from the script that can be found in my [other github repo](https://github.com/ali2538/wiki-movie-list) to fetch the details from each of their Wikipedia pages

This scraper uses scrapy framework to go through the list of movies

The result is saved in a csv file by running the command ``scrapy crawl wiki_movie_db -O wiki_movie_db_details.csv``.

There are intentional pauses in the script to avoid over loading any server.