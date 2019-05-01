#!/usr/bin/env python
# coding: utf-8

#imports
from bs4 import BeautifulSoup as bs
from splinter import Browser
from urllib.parse import urlsplit
import os
import pandas as pd
import time
from selenium import webdriver

#chromedriver path
def init_browser():
    executable_path = {"executable_path":"C:\chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    return browser
    
#scrape function
def scrape():
    browser = init_browser()
    mars_storedata = {}

    #visiting the page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #using beautiful soup
    html = browser.html
    soup = bs(html,"html.parser")

    # collecting latest news
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_storedata['news_title'] = news_title
    mars_storedata['news_paragraph'] = news_paragraph

    # collecting featured image
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url_image)

    #Getting the base url
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))

    #Design an xpath selector to grab the image
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
    print(full_img_url)
    mars_storedata["featured_image"] = full_img_url

    #get mars weather's latest tweet
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    # beatifulsoup for weather
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_storedata["mars_weather"] = mars_weather
    
    # collecting mars facts
    url_facts = "https://space-facts.com/mars/"

    # convert the data to a HTML table string
    table = pd.read_html(url_facts)
    table[0]

    mars_facts_df = table[0]
    mars_facts_df.columns = ["Parameter", "Values"]
    facts_table = mars_facts_df.set_index(["Parameter"])

    # HTML table
    mars_html_table = facts_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_storedata["mars_facts_table"] = mars_html_table

    # Mars Hemispheres
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(mars_hemisphere_url))

    # Dictionary Images
    hemisphere_img_urls = []


    # Cerberus Image Collect and Append
    results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
    time.sleep(2)
    cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    cerberus_image = browser.html
    soup = bs(cerberus_image, "html.parser")
    cerberus_url = soup.find("img", class_="wide-image")["src"]
    cerberus_img_url = hemisphere_base_url + cerberus_url
    cerberus_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    cerberus = {"image title":cerberus_title, "image url": cerberus_img_url}
    hemisphere_img_urls.append(cerberus)

    # Schiaparelli Image Collect and Append
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
    time.sleep(2)
    schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    schiaparelli_image = browser.html
    soup = bs(schiaparelli_image, "html.parser")
    schiaparelli_url = soup.find("img", class_="wide-image")["src"]
    schiaparelli_img_url = hemisphere_base_url + schiaparelli_url
    schiaparelli_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_img_url}
    hemisphere_img_urls.append(schiaparelli)

    # Syrtis Image Collect and Append
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
    time.sleep(2)
    syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    syrtis_major_image = browser.html
    soup = bs(syrtis_major_image, "html.parser")
    syrtis_major_url = soup.find("img", class_="wide-image")["src"]
    syrtis_major_img_url = hemisphere_base_url + syrtis_major_url
    syrtis_major_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_img_url}
    hemisphere_img_urls.append(syrtis_major)

    # Valles_Marineris Image Collect and Append
    results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
    time.sleep(2)
    valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
    time.sleep(1)
    valles_marineris_image = browser.html
    soup = bs(valles_marineris_image, "html.parser")
    valles_marineris_url = soup.find("img", class_="wide-image")["src"]
    valles_marineris_img_url = hemisphere_base_url + syrtis_major_url
    valles_marineris_title = soup.find("h2",class_="title").text
    back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
    valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_img_url}
    hemisphere_img_urls.append(valles_marineris)

    # Check Dictionary
    mars_storedata["hemisphere_img_url"] = hemisphere_img_urls

  # Close the browser after scraping
    browser.quit()

    return mars_storedata


