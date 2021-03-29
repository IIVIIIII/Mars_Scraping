import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    
    # Try to scrape the site using the URL
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html.text, 'html.parser')

    # Get article title and summary paragraph
    news_H = soup.find_all('div', class_='content_title')[0].a.text.replace("\n", "")
    news_P = soup.find_all('div', class_='rollover_description_inner')[0].text.replace("\n", "")



    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Jump to image link and setup soup
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = bs(html, 'html.parser')

    # Get featured image url
    featured_image_url = url.replace('index.html', soup.find_all('img')[1]['src'])

    # quit the browser
    browser.quit()



    # Try to scrape the site using the URL
    url = 'https://space-facts.com/mars/'

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html.text, 'html.parser')

    # Get Mars descriptions
    col1 = soup.find_all('td', class_='column-1')
    col2 = soup.find_all('td', class_='column-2')
    props = []
    stats = []

    # Put descriptions in a dataframe
    for x in range(0, len(col1)):
        props.append(col1[x].text)
        stats.append(col2[x].text)
        
    fax_table = pd.DataFrame({"Description": props, "Mars": stats}).set_index('Description').to_html()



    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Get pages to jump to and set arrays to fill
    jumps = []
    titles = []
    img_urls = []
    hemisphere_urls = []

    that = soup.find_all('h3')

    for this in that:
        jumps.append(this.text)
        
    # Jump through pages and get image titles and urls
    for jump in jumps:
        try:
            browser.links.find_by_partial_text(jump).click()
            html = browser.html
            soup = bs(html, 'html.parser')
            titles.append(soup.find_all('h2')[0].text.replace(" Enhanced", ""))
            img_urls.append(soup.find_all('a')[4]['href'])
            print("1 " + jump)
        except:
            try:
                browser.links.find_by_partial_text('2').click()
                browser.links.find_by_partial_text(jump).click()
                html = browser.html
                soup = bs(html, 'html.parser')
                titles.append(soup.find_all('h2')[0].text.replace(" Enhanced", ""))
                img_urls.append(soup.find_all('a')[4]['href'])
                print("2 " + jump)
            except:
                browser.links.find_by_partial_text('1').click()
                browser.links.find_by_partial_text(jump).click()
                html = browser.html
                soup = bs(html, 'html.parser')
                titles.append(soup.find_all('h2')[0].text.replace(" Enhanced", ""))
                img_urls.append(soup.find_all('a')[4]['href'])
                print("1 " + jump)

    # Quit the browser
    browser.quit()

    # Set results to list of dictionaries
    for x in range(0, len(img_urls)):
        hemisphere_urls.append({"title": titles[x], "img_url": img_urls[x]})



    mars = {"news_H": news_H,
            "news_P": news_P,
            "featured_image_url": featured_image_url,
            "fax_table": fax_table,
            "hemisphere_urls": hemisphere_urls}



    return mars

