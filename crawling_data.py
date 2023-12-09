import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

def get_urls(url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for article in soup.find_all('h3', class_='article__title'):
            link = article.find('a')['href']
            links.append(link)
            
        return links
   
def save_urls(links, category, count_link):
    # Create a filename based on the category
    filename_category = f'{category}_link.txt'
    filename_all = f'all_links.txt'

    with open(filename_category, 'a') as f:
        for link in links:
            f.write(link + '\n')
    
    with open(filename_all, 'a') as f:
        for idx, link in enumerate(links, start=count_link):
            f.write(f'{idx}, {link}, {link.split("/")[-1]}\n')

if __name__ == '__main__':
    # Define the date ranges
    end_date = '2023-12-05'
    start_date = '2022-12-06'    
    current_date = end_date  # Start crawling from the most recent date
    links_lifestyle = 0  # Counter for links crawled from 'lifestyle' category
    links_edukasi = 0  # Counter for links crawled from 'edukasi' category
    count_links = 0 # Counter for links crawled from 'lifestyle' and 'edukasi' category
    switch_category_limit = 2000  # The limit to switch to the category

    while current_date >= start_date and links_lifestyle <= 2000:
        if links_edukasi <= switch_category_limit:
            url = 'https://indeks.kompas.com/?site=edukasi&date={}'.format(current_date)
            category = 'edukasi'
        elif links_lifestyle <= switch_category_limit:
                url = 'https://indeks.kompas.com/?site=lifestyle&date={}'.format(current_date)
                category = 'lifestyle'
        
        # Get URLs for the current category
        links = get_urls(url)

        # Save URLs to the appropriate file
        save_urls(links, category, count_links)

        print(f'{category.capitalize()} links berhasil diambil untuk tanggal {current_date}')

        if category == 'edukasi':
            links_edukasi += len(links)
            count_links += len(links)
        elif category == 'lifestyle':
            links_lifestyle += len(links)
            count_links += len(links)
            

        current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Add a delay of a few seconds between requests to avoid overloading the server
        time.sleep(2)  # Adjust the delay as needed
