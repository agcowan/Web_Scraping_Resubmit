# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():
    # Automatic browser
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
    url1 = "https://spaceimages-mars.com/"
    browser.visit(url1)

    # Parser
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Find the div with the Featured Mars Image
    header = soup.find('div',class_='header')

    # Extract the URL from the header used for the Featured Image
    image = header.find('img',class_ = 'headerimage fade-in')
    featured_image_url = url1 + image['src']

    # Visit Mars Facts site https://galaxyfacts-mars.com
    url2 = "https://galaxyfacts-mars.com/"
    browser.visit(url2)

    # Use Pandas to scrape the planet profile table
    table = pd.read_html(url2)

    # Convert the scraped table to a DataFrame
    df = table[1]

    # Convert DataFrame to table, replace values with blanks 
    html_table = df.to_html().replace('\n', '')

    # Save the file as .html
    df.to_html('table.html')

    # Visit astrogeology site
    url3 = "https://marshemispheres.com/"
    browser.visit(url3)

    # Empty list for the dictionaries
    hemisphere_image_urls = []
    titles = []

    # Parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Click on links to go to the hemisphere pages
    links = []
    area = soup.find_all('a', class_ = 'itemLink')

    for each in area:
        try:
            link = each.get('href')
            if link not in links:
                links.append(link)
            browser.visit(url3 + link)
            # Parser
            html2 = browser.html
            soup2 = BeautifulSoup(html2, 'html.parser')
            # Scrape links to images
            downloads = soup2.find('div', class_ = 'downloads')
            anchor = downloads.a
            href = anchor.get('href')
            # Scrape h2 tags to get titles
            title = soup2.find('div', class_ = 'cover')
            name = title.h2.text
            # If image link not in the list, append
            if url3 + href not in hemisphere_image_urls:
                hemisphere_image_urls.append(url3 + href)
            # If title not in the list, append
            if name not in titles:
                titles.append(name)
        except:
            pass

    browser.quit()

    mars_data = {
        "image":featured_image_url,
        "art_title":title,
        "paragraph":paragraph,
        "title":title[0],"image_url":hemisphere_image_urls[0],
        "title":title[1],"image_url":hemisphere_image_urls[1],
        "title":title[2],"image_url":hemisphere_image_urls[2],
        "title":title[3],"image_url":hemisphere_image_urls[3],
        "table":html_table
    }

    return mars_data