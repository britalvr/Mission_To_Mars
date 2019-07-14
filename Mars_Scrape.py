from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars = {}

    ## NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    latest_title = soup.find("div", class_="content_title").find("a").text
    latest_text = soup.find ("div", class_="article_teaser_body").text

    mars["latest_title"] = latest_title
    mars["latest_text"] = latest_text

    ## JPL Mars Space Images - Featured Image
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)
    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")
    partial_img = soup.find("img", class_ = "fancybox-image")["src"]
    featured_image_url = img_url[:24] + partial_img

    mars["featured_image_url"] = featured_image_url

    ## Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("div", class_="js-tweet-text-container")
    mars_weather = result.p.text

    mars["mars_weather"] = mars_weather

    ## Mars Facts
    facts_url = "http://space-facts.com/mars/"
    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]
    mars_df.columns = ["description", "value"]
    mars_df = mars_df.set_index("description")
    
    facts_html = mars_df.to_html()
    mars["facts_html"] = facts_html

    ## Mars Hemispheres
    mars_hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hem_url)
    mars_hem_html = browser.html

    soup = BeautifulSoup(mars_hem_html, "html.parser")

    hem_image_urls = []
    h3_soup = soup.find_all("h3")

    for h3 in h3_soup:
        click_link = h3.text
        title = click_link[:-9]
        browser.click_link_by_partial_text(click_link)
    
        mars_hem_html = browser.html
    
        hem_soup = BeautifulSoup(mars_hem_html, "html.parser")
        img_url = browser.url[:29] + hem_soup.find("img", class_ = "wide-image")["src"]
    
        dictionary = {"title" : title, "img_url" : img_url}
        hem_image_urls.append(dictionary)
        browser.back()

        for i in range(4):
            print(hem_image_urls[i]["title"])
            print(hem_image_urls[i]["img_url"])

        browser.quit()

        mars["hem_image_urls"] = hem_image_urls
        return mars
