from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Kalimat contoh
kalimat = "dan "

# Membuat objek stopword remover
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

# Menghapus stopwords dari kalimat
kalimat_tanpa_stopword = stopword_remover.remove(kalimat)

print("Kalimat asli:", kalimat)
print("Kalimat tanpa stopwords:", kalimat_tanpa_stopword)
