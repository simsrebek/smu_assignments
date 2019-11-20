# coding: utf-8

# # Misson to Mars

# # Step 1 - Scraping
# -------
# ## NASA Mars News
# -------
# - Get the latest  [NASA Mars News](https://mars.nasa.gov/news/) by scraping the website and collect the latest news title and paragragh text.


# Dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from selenium import webdriver
import requests as req
import re






def init_browser():
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url)
 

    # Search for news
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the latest Mars news.
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    
  
    # Add the title and summary to the dictionary
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p


    # ## JPL Mars Space Images - Featured Image
    # ------
    # - Visit the url for JPL's Featured Space [Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    # - Use splinter to navigate the site and find the full size jpg image url for the current Featured Mars Image.
    # - Save a complete url string for this image


    # While chromedriver is open go to JPL's Featured Space Image page. 
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `featured_image_url`
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    
    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url


    # ## Mars Weather 
    # ------
    # - From the [Mars Weather twitter](https://twitter.com/marswxreport?lang=en) account scrape the latest Mars weather tweet from the page.
    # - Save the tweet text for the weather report.
    #
    twitter_response = req.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = bs(twitter_response.text, 'html.parser')
    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")
    for i in range(10):
        tweets = tweet_containers[i].text
        if "Sol " in tweets:
            mars_weather = tweets
            break
    
    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather

    # ## Mars Facts
    request_mars_space_facts = req.get("https://space-facts.com/mars/")
    mars_space_table_read = pd.read_html(request_mars_space_facts.text)
    df = mars_space_table_read[0]
    df.set_index(0, inplace=True)
    mars_data_df = df
    mars_data_html = mars_information_df.to_html()
    mars_data_html.replace('\n', '')
    mars_data_df.to_html('mars_table.html')

    mars_data["mars_table"] = marsinformation
  
    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()

    mars_data['hemisphere_image_urls'] = hemispheres_image_urls
    # Return the dictionary
    return mars_data