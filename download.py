import requests
import os
from bs4 import BeautifulSoup
import re

# Create the 'File_txt' directory if it doesn't exist
if not os.path.exists('File_txt'):
    os.makedirs('File_txt')

# Function to download HTML from a given URL and save it to a file
def download_html(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse konten dengan BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Temukan elemen dengan atribut itemprop="articleBody"
            article_body = soup.find(class_='read__content')
            
            # Dapatkan teks dari setiap elemen <p> dan simpan ke dalam list
            paragraphs = [p.get_text() for p in article_body.find_all('p')]
            
            # Gabungkan list menjadi satu string, dengan setiap paragraf dipisahkan oleh baris baru
            text = '\n'.join(paragraphs) 
            
            # Hapus tanda baca dan karakter non-alfabet
            text = re.sub(r'[^\w\s]', ' ', text)

            # Case folding
            text = text.lower()

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
                
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
            break  # Stop when 2000 txt files are downloaded
        # Get the content of the HTML page
        filename = f'File_txt/{current_id}_{link.split("/")[-1]}.txt'
        if download_html(link, filename):
            current_id += 1
            downloaded_count += 1

    return current_id, downloaded_count

# Process links for "edukasi" with ID range 110000 to 112000
current_id, downloaded_count = process_links('edukasi_link.txt', 110000, 2000)

# Process links for "lifestyle" with ID range 220000 to 222000
current_id, downloaded_count = process_links('lifestyle_link.txt', 220000, 2000)


print(f'Total txt files downloaded for edukasi: {downloaded_count}')
print(f'Total txt files downloaded for lifestyle: {downloaded_count}')
