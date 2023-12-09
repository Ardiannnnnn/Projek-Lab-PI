import math
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# Inisialisasi stemmer dari Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Fungsi untuk membaca inverted index dari file
def read_inverted_index(file_path):
    inverted_index = {}
    with open(file_path, 'r') as file:
        for line in file:
            term, postings = line.strip().split(': ')
            postings = eval(postings)
            inverted_index[term] = postings
    return inverted_index

# Fungsi untuk menghitung skor tf-idf
def calculate_tf_idf_score(query_terms, doc_id, inverted_index, doc_lengths):
    score = 0
    for term in query_terms:
        if term in inverted_index:
            for doc_freq, freq in inverted_index[term]:
                if doc_freq == doc_id:
                    idf = math.log(len(doc_lengths) / len(inverted_index[term]))
                    score += (freq * idf)      
    return score

# Modify the read_document_links function to read document links from a file
def read_document_links(file_path):
    document_links = {}
    document_name ={}
    with open(file_path, 'r') as file:
        for line in file:
            doc_id, link, name = line.strip().split(', ')
            document_links[int(doc_id)] = link
            document_name[int(doc_id)] = name
    return document_links, document_name

# Update the search function to include document links in the output
def search(query, inverted_index, doc_lengths, document_links):
    query_terms = [stemmer.stem(word) for word in query.split()]
    scores = {}
    
    for doc_id in range(4000):
        if doc_id in doc_lengths:
            score = calculate_tf_idf_score(query_terms, doc_id, inverted_index, doc_lengths)
            if score != 0:
                scores[doc_id] = score
    
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    if not ranked_docs:
        return ["Tidak ada dokumen yang cocok"]
    
    results = []
    for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
        if doc_id in document_links:  # Check if the document ID has a corresponding link
            link = document_links[doc_id]
            name = document_name[doc_id]
            # Bersihkan teks dari karakter khusus
            name = re.sub(r'\W+', ' ', name)
            name = name.capitalize()
            results.append(f"Ranking: {rank}\nScore: {score}\nJudul Artikel: {name}\nLink: {link}\n")
        else:
            results.append(f"Ranking: {rank}\nScore: {score}\nJudul Artikel: {name}\nLink: Not Found\n")
    
    return results

# Read the inverted index and document links from files
inverted_index = read_inverted_index('inverted_index.txt')
document_links, document_name = read_document_links('all_links.txt')

# Average document length assumed here
avg_doc_length = 500
doc_lengths = {i: avg_doc_length for i in range(4000)}

query = input("Masukkan query: ")
results = search(query, inverted_index, doc_lengths, document_links)

for result in results:
    print(result)
