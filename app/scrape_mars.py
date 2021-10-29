from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
  
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

   
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }


    browser.quit()
    return data


def mars_news(browser):

  
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    browser.is_element_present_by_css('div.list_text', wait_time=1)

    
    html = browser.html
    news_soup = soup(html, 'html.parser')


    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        news_title = slide_elem.find("div", class_="content_title").get_text()
        
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

  
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

   
    html = browser.html
    img_soup = soup(html, 'html.parser')

   
    try:
   
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

   
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():

    try:
        
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

   
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

   
    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')

 
    hemisphere_image_urls = []
    for i in range(4):
       
        browser.find_by_css("a.product-item img")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data['img_url'] = url + hemi_data['img_url']

        hemisphere_image_urls.append(hemi_data)
       
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
   
    hemi_soup = soup(html_text, "html.parser")


    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres


if __name__ == "__main__":

   
    print(scrape_all())