from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def scrape():

    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path)

    #NASA MARS NEWS

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_body = soup.find('div', class_='article_teaser_body').text

    #JPL MARS SPACE FEATURED IMAGE

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url_find = soup.find('article', class_='carousel_item')["style"]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url_find.split("'",2)[1]

    # MARS WEATHER

    url = 'https://twitter.com/MarsWxReport?lang=en'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    # MARS FACTS

    url = 'https://space-facts.com/mars/'

    fact_table = pd.read_html(url)[1]
    fact_table = fact_table.set_index(0)
    fact_table = fact_table.rename(columns={1: ""})
    fact_table.index = fact_table.index.rename("")

    table_html = fact_table.to_html()

    # MARS HEMISPHERS

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)

    hemisphere_image_urls = []

    html = browser.html
    soup = bs(html, 'html.parser')

    title_list = []
    titles = soup.find_all('div', class_='description')
    for x in titles:
        title_list.append(x.a.h3.text)

    for x in title_list:

        html = browser.html
        soup = bs(html, 'html.parser')

        browser.click_link_by_partial_text(x)

        html = browser.html
        soup = bs(html, 'html.parser')

        img = soup.find('img', class_='wide-image')["src"]
        img_link = "https://astrogeology.usgs.gov" + img

        dict = {'title': x[:-9],
               'img_url': img_link}

        hemisphere_image_urls.append(dict)
        browser.visit(url)

    hemisphere_image_urls.append(dict)

    # DICTIONARY WITH ALL SCRAPED DATA

    scraped_dict = {
        'news_title':news_title,
        'news_body': news_body,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'table_html': table_html,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return scraped_dict