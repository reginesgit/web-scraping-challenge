from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import urllib.parse


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    ### NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Variable for returned first paragraph text, cleaned up
    text = soup.find('div', class_='rollover_description_inner').text
    text_stripped = text.strip('\n')

    # Variable for returned first article title, cleaned up
    title = soup.find('div', class_='content_title').a.text
    title_stripped = title.strip('\n')


    ### JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve image path and append it to the site path for complete link to image
    featuredimagepath = soup.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featuredimagepath

    browser.quit()


    ### Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[0]
    cleaned_facts_df = facts_df.rename(columns={0:" ", 1:"Mars"})
    cleaned_facts_df.set_index(" ")
    cleaned_facts_df.to_html('html_facts_table.html')
    facts_html = cleaned_facts_df.to_html()
    facts_html.replace('\n', '')



    ### Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    titles = []

    for item in items:
        title = item.find('h3').text
        titles.append(title)

    original_img_url_list =[]

    for title in titles:
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        link = soup.find('div', class_= 'downloads')('li')[0]
        orig_img = link.find('a')['href']
        original_img_url_list.append(orig_img)
        browser.back()

    title1 = titles[0]
    title2 = titles[1]
    title3 = titles[2]
    title4 = titles[3]

    hem1 = original_img_url_list[0]
    hem2 = original_img_url_list[1]
    hem3 = original_img_url_list[2]
    hem4 = original_img_url_list[3]



    # # Store data in a dictionary to be returned
    mars_data = {
        "title_stripped": title_stripped,
        "text_stripped": text_stripped,
        "featured_image_url": featured_image_url,
        "facts_html": facts_html,
        "title1": title1,
        "hem1": hem1,
        "title2": title2,
        "hem2": hem2,
        "title3": title3,
        "hem3": hem3,
        "title4": title4,
        "hem4": hem4
    }

    browser.quit()

    return mars_data