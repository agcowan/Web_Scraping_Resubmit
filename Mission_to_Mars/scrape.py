# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_info():
    # Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome',**executable_path, headless=False)

    # Visit news site https://redplanetscience.com
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    
    # Parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Find the first article div, class list_text
    article = soup.find('div', class_='list_text')

    # Scrape the title and save in a variable
    title = article.find('div', class_='content_title').text

    # Scrape the paragraph text and save in a variable
    paragraph = article.find('div', class_='article_teaser_body').text

    # Visit Featured Space Image site https://spaceimages-mars.com
    img_url = "https://spaceimages-mars.com/"
    browser.visit(img_url)
    time.sleep(2)
    # Parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Find the div with the Featured Mars Image
    header = soup.find('div',class_='header')

    # Extract the URL from the header used for the Featured Image
    image = header.find('img',class_ = 'headerimage fade-in')
    featured_image_url = img_url + image['src']

    # Visit Mars Facts site https://galaxyfacts-mars.com
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)

    # Use Pandas to scrape the planet profile table
    table = pd.read_html(facts_url)

    # Convert the scraped table to a DataFrame
    df = table[1]

    # Convert DataFrame to table, replace values with blanks 
    html_table = df.to_html().replace('\n', '')

    # Save the file as .html
    df.to_html('table.html')

    # Visit astrogeology site
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)

    # Empty list for the dictionaries
    hemisphere_image_urls = []
    titles = []
    image_url = []
    links = []

    # Parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Click on links to go to the hemisphere pages
    area = soup.find_all('a', class_ = 'itemLink')

    for each in area:
        # print("Running for each")
        try:
            link = each.get('href')

            if link not in links:
                links.append(link)
            browser.visit(hemi_url + link)
            time.sleep(2)

            # Parser
            html2 = browser.html
            soup2 = BeautifulSoup(html2, 'html.parser')
            # Scrape links to images
            downloads = soup2.find('div', class_ = 'downloads')
            anchor = downloads.a
            href = anchor.get('href')

            # Scrape h2 tags to get titles
            title2 = soup2.find('h2')
            name = title2.text
            img_url = hemi_url + href


            # If image link not in list, append
            if img_url not in image_url:
                image_url.append(img_url)
            
            # If image title not in list, append
            if name not in titles:
                titles.append(name)            
            
        except Exception as e:
            print(e)

    hemisphere_image_urls = [{"title":titles[0], "img_url":image_url[0]},
                            {"title":titles[1], "img_url":image_url[1]},
                            {"title":titles[2], "img_url":image_url[2]},
                            {"title":titles[3], "img_url":image_url[3]}]
    browser.quit()

    mars_data = {
        "image":featured_image_url,
        "art_title":title,
        "paragraph":paragraph,
        "hemispheres":hemisphere_image_urls,
        "table":html_table
    }

    return mars_data




if __name__ == "__main__":
    print(scrape_info())