from bs4 import BeautifulSoup
import requests
import random
import time
import datetime
import json
import os


date = datetime.date(2018,1,1)  		# START DATE (year,month,day)
finish_date = datetime.date(2018,1,10)  # STOP DATE (year,month,day)
t_delta = datetime.timedelta(days=1)
waiting = 0.01
while date != finish_date:
    date_for_link = date.strftime('%Y%m%d')
    date_for_us = date.strftime('%Y-%m-%d')
    source = requests.get(f'https://www.reuters.com/resources/archive/us/{date_for_link}.html').text
    soup = BeautifulSoup(source, 'lxml')
    try:
        # Make a soup from one archive page. Gather links of article links, and publication times.
        articles = soup.find('div', class_='module')
        articles = articles.find_all('div', class_='headlineMed')
        articles_links = [article.a['href'] for article in articles]
        articles_UTC_times = [article.text[-11:].split('\xa0')[-1] for article in articles]
        articles_UTC_times = [datetime.datetime.strptime(t, '%I:%M%p UTC').time().strftime('%H:%M') for t in
                              articles_UTC_times]
        articles_UTC_times = [date_for_us + '  ' + t for t in articles_UTC_times]
        articles_in_given_day = []
        num_links = len(articles_links)
        for num, link in enumerate(articles_links):
            try:
                # Make a soup from single article in list of links. Gather body, news category, time, title.
                done = False
                attempt = 1
                while not done:
                    try:
                        time.sleep(waiting)
                        source_link = requests.get(link, timeout=(0.4 + attempt - 1)).text
                        if attempt > 1: print(f', attempt {attempt}, ', end='')
                    except requests.exceptions.ReadTimeout:
                        if attempt == 1: print('Timed out', end='')
                        attempt += 1
                    except requests.exceptions.ConnectTimeout:
                        time.sleep(15)
                    except requests.exceptions.ConnectionError:
                        print('WARNING WE WERE BLOCKED: UPPING WAITING TIME...')
                        time.sleep(30)
                        waiting += 0.1
                    else:
                        if attempt > 1: print('success!')
                        done = True
                soup_link = BeautifulSoup(source_link, 'lxml')
                foreground = soup_link.find('div', class_='foreground')
                news_category = foreground.find('div', class_='channel_4KD-f').a.text
                time_ = articles_UTC_times[num]
                title = foreground.find('h1', class_='headline_2zdFM').text
                body = soup_link.find('div', class_='body_1gnLA').find_all('p')
                body = ' '.join([paragr.text for paragr in body])
            except AttributeError:
                print(f"Article number {num+1} was skipped - Page Not Found")
                news_category = None
                time_ = None
                title = None
                body = None
            articles_in_given_day.append(
                {'news_category': news_category,
                 'time': time_,
                 'title': title,
                 'body': body})
            print(f'({num+1}/{num_links}) day progress -- ({date_for_us}) year progress')
        with open('scraped news/' + date_for_us + '.json', 'w') as f:
            json.dump(articles_in_given_day, f, indent=5)
        date += t_delta
    except AttributeError:
        print(f"Day {date_for_us} was skipped - Archive Page Not Found")
        date += t_delta
