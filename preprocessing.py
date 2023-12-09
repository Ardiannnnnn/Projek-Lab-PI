import os
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Tentukan direktori tempat file-file berada
input_directory = "D:/Skill/Projek-Lab-PI/File_txt"

# Buat direktori baru untuk menyimpan file hasil di folder "Clean_File"
output_directory = "D:/Skill/Projek-Lab-PI/Clean_File"

# Buat daftar file-file di direktori input
file_list = os.listdir(input_directory)

# Membuat direktori output jika belum ada
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Inisialisasi Stemmer Sastrawi sekali di luar loop untuk meningkatkan kinerja
stemmer = StemmerFactory().create_stemmer()

# Inisialisasi Stopword Remover Sastrawi
stopword_factory = StopWordRemoverFactory()

# Hapus stopwords sekali lagi, jika ada yang tersisa
stopword = stopword_factory.create_stop_word_remover()

# Looping semua file di direktori input
for file_name in file_list:
    # Jika file adalah file teks, lanjutkan
    if file_name.endswith('.txt'):
        # Baca teks dari file
        with open(os.path.join(input_directory, file_name), 'r', encoding='utf-8') as f:
            text = f.read()

        # Bersihkan teks dari angka dan nomor-nomor
        text = re.sub(r'\d+', '', text)

         # Hapus stopword dari teks
        text = stopword.remove(text)

        # Bersihkan teks dari karakter khusus
        text = re.sub(r'[!()-[]{};:"\, <>./?@#$%^&*_~]', '', text)

        # Ubah teks menjadi huruf kecil
        text = text.lower()

        # Tokenisasi teks yang sudah dibersihkan
        tokens = text.split()

        # Stemming teks tanpa menghapus duplikat token
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        
        # Menyimpan hasil teks yang sudah dibersihkan, di-tokenisasi, 
        # di-stem, dan dihilangkan stopwords ke dalam berkas
        output_file_name = file_name
        output_file_path = os.path.join(output_directory, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(stemmed_tokens))
        print(f'Berhasil dipreprocessing : File {file_name} ')