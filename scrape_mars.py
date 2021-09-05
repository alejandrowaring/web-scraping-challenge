#Imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #Mars News
    news_url= 'https://redplanetscience.com/'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    latest_news = {}
    latest_news['headline'] = soup.find("div", class_="content_title").get_text()
    latest_news['body'] = soup.find('div',class_="article_teaser_body").get_text()
    #JPL Mars Space Images
    jpl_mars_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_mars_url)
    html = browser.html
    soup = bs(html,'html.parser')
    featured_image = f"{jpl_mars_url}{soup.find('img',class_='headerimage')['src']}"
    #Mars Facts
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_facts_url)
    html = browser.html
    soup = bs(html,'html.parser')
    df = pd.read_html(mars_facts_url)[1].transpose()
    df.columns = df.iloc[0]
    df.drop(0,inplace=True)
    df.reset_index(drop=True, inplace=True)
    tableresult = df.to_html(index=False)
    #Mars Hemispheres
    astrogeology_url = 'https://marshemispheres.com/'
    browser.visit(astrogeology_url)
    html = browser.html
    soup = bs(html,'html.parser')
    hemisphere_image_urls = []
    results = soup.find_all('div',class_="item")
    for i in results:
        url = f"{astrogeology_url}{i.find('a',class_='itemLink')['href']}"
        browser.visit(url)
        image_html = browser.html
        csoup = bs(image_html,'html.parser')
        image_link = f"{astrogeology_url}{csoup.find('img', class_='wide-image')['src']}"
        title = csoup.find('h2',class_="title").get_text().rsplit(" ",1)[0]
        result_dict = {"title":title,"img_url":image_link}
        hemisphere_image_urls.append(result_dict)
    #dictionary for export
    mars_data = {
        "mars_news": latest_news['headline'],
         "mars_p":latest_news['body'],
         "mars_img": featured_image,
         "mars_facts":tableresult,
         "mars_hemispheres":hemisphere_image_urls
        }
    print(mars_data)
    return mars_data
