from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


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
    featured_image_url = ['https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featuredimagepath]

    browser.quit()

    ### Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[0]
    cleaned_facts_df = facts_df.rename(columns={0:" ", 1:"Mars"})
    cleaned_facts_df.set_index(" ")
    facts_html = cleaned_facts_df.to_html()
    facts_html.replace('\n', '')

    # cleaned_facts_df.to_html('html_facts_table.html')

    ### Mars Hemispheres
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    titles = []
    url_list = []
    img_url_list = []

    for item in items:
        title = item.find('h3').text
        titles.append(title)
        img_url = item.find('a')['href']
        url_list.append(img_url)

    img_url_list = ['https://astrogeology.usgs.gov/' + url for url in url_list]

    original_img_url_list =[]

    for title in titles:
        # browser.click_link_by_partial_text(title)
        browser.links.find_by_partial_text(title)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        link = soup.find('div', class_= 'downloads')('li')[1]
        orig_img = link.find('a')['href']
        original_img_url_list.append(orig_img)
        browser.back()
    
    # hemisphere_img_list = [
    #     {"title": titles[0], "img_url": original_img_url_list[0]},
    #     {"title": titles[1], "img_url": original_img_url_list[1]},
    #     {"title": titles[2], "img_url": original_img_url_list[2]},
    #     {"title": titles[3], "img_url": original_img_url_list[3]}
    # ]

    # # Store data in a dictionary
    mars_data = {
        "title_stripped": title_stripped,
        "text_stripped": text_stripped,
        "featured_image_url": featured_image_url,
        "facts_html": facts_html,
        "titles[0]": titles[0],
        "original_img_url_list[0]": original_img_url_list[0],
        "titles[1]": titles[1],
        "original_img_url_list[1]": original_img_url_list[1],
        "titles[2]": titles[2],
        "original_img_url_list[2]": original_img_url_list[2],
        "titles[3]": titles[3],
        "original_img_url_list[3]": original_img_url_list[3]
    }

    browser.quit()

    return mars_data

    # # Visit visitcostarica.herokuapp.com
    # url = "https://visitcostarica.herokuapp.com/"
    # browser.visit(url)

    # time.sleep(1)

    # # Scrape page into Soup
    # html = browser.html
    # soup = bs(html, "html.parser")

    # # Get the average temps
    # avg_temps = soup.find('div', id='weather')

    # # Get the min avg temp
    # min_temp = avg_temps.find_all('strong')[0].text

    # # Get the max avg temp
    # max_temp = avg_temps.find_all('strong')[1].text

    # # BONUS: Find the src for the sloth image
    # relative_image_path = soup.find_all('img')[2]["src"]
    # sloth_img = url + relative_image_path

    # # Store data in a dictionary
    # costa_data = {
    #     "sloth_img": sloth_img,
    #     "min_temp": min_temp,
    #     "max_temp": max_temp
    # }

    # # Close the browser after scraping
    # browser.quit()

    # # Return results
    # return costa_data
