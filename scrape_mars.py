#Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
#from webdriver_manager.chrome import ChromeDriverManager
#from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import time
import datetime as dt

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
  browser = init_browser()
  mars_dict = {}

  ## NASA Mars News
  nasa_url = 'https://mars.nasa.gov/news/'
  browser.visit(nasa_url)
  time.sleep(1)
  browser.is_element_present_by_name("email", wait_time=1)
  html = browser.html
  soup = bs(html, "html.parser")
  # Find news title and paragraph text
  news = soup.select_one('div.list_text')
  title = news.find('div', class_='content_title').get_text()
  paragraph = news.find('div', class_= 'article_teaser_body').get_text()

  ## JPL Mars Space Images

  jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
  browser.visit(jpl_url)
  time.sleep(1)
  browser.click_link_by_partial_text('FULL IMAGE')
  browser.is_element_present_by_text('more info', wait_time=1)
  html = browser.html
  jpl_soup = bs(html, 'html.parser')
  # Find the image url for the current Featured Mars Image
  original_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
  image = jpl_soup.find('div', class_='floating_text_area')
  new_image = image.find('a', class_='showimg fancybox-thumbs')
  final_image = new_image['href']
  featured_image_url = original_url + final_image


  ## Mars Facts
  mars_url = 'https://space-facts.com/mars/'
  mars_table = pd.read_html(mars_url)
  mars_facts_df = mars_table[0]
  mars_facts_df.rename(columns = {0: 'Measurement', 1: 'Value'}, inplace = True) 
  mars_facts_html = mars_facts_df.to_html()
  final_facts = mars_facts_html.replace('\n', '')

  ## Mars Hemispheres
  hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
  browser.visit(hemispheres_url)
  browser.is_element_present_by_text("Contact", wait_time=1)
  hemi_html = browser.html
  soup = bs(hemi_html, "html.parser")
  # Obtain high resolution images for each of Mars' hemispheres
  first_pass = soup.find('div', class_='result-list')
  images = first_pass.find_all('div', class_='item')
  base_url = 'https://astrogeology.usgs.gov/'
  
  hemi_urls = []
  for image in images:
    title = image.find('h3').text
    link = image.find('a')['href']
    updated_link = base_url + link
    browser.visit(updated_link)
    html2 = browser.html
    soup = bs(html2, 'html.parser')
    first_div = soup.find('div', class_='downloads')
    enhanced_image_url = first_div.find('a')['href']
    hemi_urls.append({'title' : title, 'img_url' : enhanced_image_url})

  ## Dictionary 
  mars_data = {
      "title" : title,
      "paragraph" : paragraph,
      "featured_image_url" : featured_image_url,
      "final_facts" : final_facts,
      "hemi_urls" : hemi_urls
  }

  # Close browser
  browser.quit()

  # Results
  return mars_data

