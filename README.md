# Scraping Reuters Archive

### The algorithm scrapes the Thomson Reuters archive between custom dates at an average rate of 200,000 news stories per day. In addition I include Jupyter Notebook running statistical analysis of scraped news such as number of atricles published by Reuters per weekday/month, distribution of news categories and others.

## Requirements
- bs4 (BeautifulSoup)
- requests
- matplotlib
- numpy
 
## How to scrape
1. Clone the repository on your machine. You may wish to delete contents of 'data exploration results' directory and 'scraped news' directory, as these are for demo purposes only, although you should keep these folders themselves.
2. In "scraping_reuters.py" on lines 10 and 11 set the start and finish dates between which you want to scrape the Thomson Reuters archive. Start date inclusive, finish date exclusive.
3. Launch "scraping_reuters.py" and leave it running to scrape the archive at the average rate of 200,000 news articles per 24 hours. The algorithm will automatically increase waiting time if too many requests are sent per minute. This is to follow the web scraping etiquette.

## Scraped News Storage
Gathered articles will be saved in 'scraped news' directory as a list of JSON files. Each files' name contains all articles published by Reuters on a particular date. Each JSON file contains a list of dictionaries where each dictionary is a single news article. Dictionaries have four keys: 'news_category', 'time', 'title' and 'body' where time is the date and time of article publication in UTC timezone.

## News Exploration with Jupyter
The included Jupyter Notebook runs statistical analysis on the gathered news articles once scraping is finished. It helps answer the following questions: 
1. How many archive days are scraped in total? 
2. How many archive days are missing? (Page Not found) 
3. How many news articles are scraped in total? 
4. How many articles are published per month? (timeline distribution) 
5. On average how many articles published per weekday? (distribution)
6. How many news categories are there and what are the most popular ones?

## Sample Exploration Plots
<img src="data exploration results/Monthly Timeline.png" />

<img src="data exploration results/Weekday Distribution.png" />

<img src="data exploration results/Most Popular News Categories.png" />
