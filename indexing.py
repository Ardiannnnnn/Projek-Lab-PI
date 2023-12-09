import os
import re
from collections import Counter

# Fungsi untuk membersihkan dan tokenisasi teks
def clean_and_tokenize(text):
    text = re.sub(r'\n', ' ', text)  # Mengganti newline dengan spasi
    text = re.sub(r'\s+', ' ', text)  # Menghilangkan whitespace berlebihan
    tokens = text.split()
    return tokens

# Fungsi untuk membangun inverted index dari file
def build_inverted_index(file_path, doc_id):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Membersihkan dan tokenisasi teks
    tokens = clean_and_tokenize(text)
    
    # Menghitung frekuensi term dalam dokumen
    term_frequency = Counter(tokens)
    
    # Membuat inverted index
    index = {}
    for term, freq in term_frequency.items():
        if term not in index:
            index[term] = []
        index[term].append((doc_id, freq))
    return index

# Memproses setiap file dalam output_folder
output_folder = 'Clean_File'
output_files = os.listdir(output_folder)

# Membuat inverted index
inverted_index = {}

for doc_id, output_file in enumerate(output_files):
    if output_file.endswith('.txt'):
        file_path = os.path.join(output_folder, output_file)
        
        # Membuat inverted index untuk dokumen ini
        index = build_inverted_index(file_path, doc_id)
        
        # Memasukkan ke dalam inverted index global
        for term, positions in index.items():
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].extend(positions)
       
# Menyimpan inverted index ke dalam berkas
index_file_path = os.path.join('inverted_index.txt')
with open(index_file_path, 'w', encoding='utf-8') as index_file:
    for term, doc_freq_pairs in inverted_index.items():
        index_file.write(f"{term}: {', '.join([f'({doc_id},{freq})' for doc_id, freq in doc_freq_pairs])}\n")

print(f"Inverted index telah disimpan ke dalam '{index_file_path}'.")
