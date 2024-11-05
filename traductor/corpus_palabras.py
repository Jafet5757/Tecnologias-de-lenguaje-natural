import random
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import words
import json

# Descargar el paquete wordnet y las traducciones
nltk.download('wordnet')
nltk.download('omw-1.4')
# Descargar el corpus de palabras en inglés
nltk.download('words')

def download_english_spanish_dic():
  # Crear diccionario inglés-español
  words_to_translate = ['hello', 'world', 'computer', 'science']
  english_spanish_dict = {}

  for word in words_to_translate:
      synsets = wn.synsets(word, lang='eng')
      if synsets:
          translations = synsets[0].lemma_names('spa')  # Obtener traducción en español
          if translations:
              english_spanish_dict[word] = translations[0]  # Obtener la primera traducción

  # Obtener la lista de palabras en inglés
  word_list = words.words()
  # Mostramos el tamaño de la lista
  print(f"Tamaño de la lista de palabras: {len(word_list)}") # Tamaño de la lista de palabras: 236736

  print("Palabras de muestra (aleatorias): ", random.sample(word_list, 5))

  # Obtenemos una muestra de 1000 palabras
  word_list = random.sample(word_list, 236736)
  # Obtenemos su traducción al español
  english_spanish_dict = {}
  for word in word_list:
      synsets = wn.synsets(word, lang='eng')
      if synsets:
          translations = synsets[0].lemma_names('spa')  # Obtener traducción en español
          if translations:
              english_spanish_dict[word] = translations[0]  # Obtener la primera traducción

  # Guardamos el diccionario en un archivo JSON, usamos utf-8 para caracteres especiales
  with open('english_spanish_dict.json', 'w', encoding='utf-8') as f:
      json.dump(english_spanish_dict, f, ensure_ascii=False, indent=4)

def download_spanish_english_dic():
  # Obtenemos el total de palabras en español
  spanish_words = wn.words(lang='spa')
  # Iteramos sobre las palabras y obtenemos su traducción al inglés
  spanish_english_dict = {}
  for word in spanish_words:
      synsets = wn.synsets(word, lang='spa')
      if synsets:
          translations = synsets[0].lemma_names('eng')  # Obtener traducción en inglés
          if translations:
              spanish_english_dict[word] = translations[0]  # Obtener la primera traducción

  # Guardamos el diccionario en un archivo JSON, usamos utf-8 para caracteres especiales
  with open('spanish_english_dict.json', 'w', encoding='utf-8') as f:
      json.dump(spanish_english_dict, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
  download_spanish_english_dic()
  print("Descarga de diccionarios completada")