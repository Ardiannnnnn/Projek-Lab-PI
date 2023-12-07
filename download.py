import requests
import os
from bs4 import BeautifulSoup

# Create the 'File_HTML' directory if it doesn't exist
if not os.path.exists('File_HTML'):
    os.makedirs('File_HTML')

# Function to download HTML from a given URL and save it to a file
def download_html(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f'Berhasil didownload: {filename}')
            return True
        else:
            print(f'Failed to download: {filename}')
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')
    return False

# Function to process links from a file
def process_links(file_name, start_id, max_count):
    current_id = start_id
    downloaded_count = 0

    with open(file_name, 'r') as file:
        links = file.read().splitlines()

    for link in links:
        if downloaded_count >= max_count:
            break  # Stop when 1000 HTML files are downloaded
        # Get the content of the HTML page
        filename = f'File_HTML/{current_id}_{link.split("/")[-1]}.html'
        if download_html(link, filename):
            current_id += 1
            downloaded_count += 1

    return current_id, downloaded_count

# Process links for "otomotif" with ID range 110000 to 111000
current_id, downloaded_count = process_links('otomotif_link.txt', 110000, 1000)

# Process links for "health" with ID range 220000 to 221000
current_id, downloaded_count = process_links('health_link.txt', 220000, 1000)

print(f'Total HTML files downloaded for otomotif: {downloaded_count}')
print(f'Total HTML files downloaded for health: {downloaded_count}')
