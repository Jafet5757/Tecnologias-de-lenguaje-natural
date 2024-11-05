import json
import re
import ordenador_palabras_bayesiano as ordenador

# Cargar el diccionario inglés-español
with open('english_spanish_dict.json', 'r', encoding='utf-8') as f:
    english_spanish_dict = json.load(f)

# Cargar el diccionario español-inglés
with open('spanish_english_dict.json', 'r', encoding='utf-8') as f:
    spanish_english_dict = json.load(f)

# Función de limpieza
def clean_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def console_main():
  while True:
    # Menu de opciones
    print("\n"*4)
    print("Traductor inglés-español")
    print("1. Traducir palabra o frase")
    print("2. Ordenar traducciones")
    print("3. Salir")
    opc = input("Seleccione una opción: ")

    if opc == "1":
        text = input("\nIngrese la palabra o frase a traducir: ")
        text = clean_text(text)
        # Dividir el texto en palabras
        words = text.split()
        # Traducir cada palabra
        translation = ""
        for word in words:
            if word in english_spanish_dict:
                translation += english_spanish_dict[word] + " "
            else:
                word_unknown = input(f"La palabra '{word}' no está en el diccionario. Ingrese su traducción: ")
                translation += word_unknown + " "
                # Agregamos la palabra al diccionario
                english_spanish_dict[word] = word_unknown
        print(f"Traducción textual: {translation}")
        # ordenamos las palabras
        print("Frase ordenada: ", ordenador.order_words(translation))

        # Guardar el diccionario actualizado
        with open('english_spanish_dict.json', 'w', encoding='utf-8') as f:
            json.dump(english_spanish_dict, f, ensure_ascii=False, indent=4)

    elif opc == "2":
        order_translations()
        print("Traducciones ordenadas alfabéticamente")
    else:
        print("Saliendo...")
        break
    
def translate(phrase, order, direction):
    """ 
    Traduce una frase de inglés a español
    ----
    Parámetros:
      phrase (str): Frase en inglés
      order (bool): Ordenar las palabras de la traducción
    ----
    Returns:
      translation str: Frase traducida a español 
    """
    phrase = clean_text(phrase)
    words = phrase.split()
    suggests = {} # Diccionario de sugerencias: {index_word: Number, suggestions: [word1, word2, ...]}
    translation = ""
    dic = english_spanish_dict if direction == "en-es" else spanish_english_dict # Seleccionar el diccionario
    for word in words:
        if word in dic:
            translation += dic[word] + " "
        else:
            translation += word + " "
            # Buscar palabras sugeridas
            suggestions_list = suggestions(word, direction)
            suggests[word] = {"suggestions":suggestions_list}
    # Ordenar las palabras
    translation = ordenador.order_words(translation) if (order and direction=="en-es") else translation
    return translation, suggests

def suggestions(word1, direction, tolerance=2, search_zone=8, rounds = 12):
    """
    Encuentra las palabras más cercanas a la dada usando búsqueda binaria y cálculo de la distancia de Levenshtein.
    ----
    Parámetros:
      word1 (str): Palabra en inglés
      tolerance (int): Tolerancia para la distancia de Levenshtein
      search_zone (int): Zona de búsqueda alrededor del índice encontrado
    ----
    Returns:
      closest_words (list): Lista de palabras más cercanas
    """
    closest_words = []
    dic = english_spanish_dict if direction == "en-es" else spanish_english_dict
    keys = list(dic.keys())
    left, right = 0, len(keys) - 1
    pointer = 0
    counter = 0
    
    # Búsqueda binaria para encontrar el índice inicial cercano a la palabra
    while left <= right and counter < rounds:
        mid = (left + right) // 2
        if keys[mid] < word1:
            left = mid + 1
        elif keys[mid] > word1:
            right = mid - 1
        else:
            pointer = mid
            break
        counter += 1
    else:
        pointer = left  # Asigna el punto más cercano si no se encuentra exactamente

    # Búsqueda de palabras alrededor del puntero dentro de la zona de búsqueda especificada
    start = max(0, pointer - search_zone)
    end = min(len(keys), pointer + search_zone)

    for i in range(start, end):
        # Calcular la distancia de Levenshtein y verificamos si es tolerable
        if levenstein_distance(word1, keys[i]) <= tolerance:
            closest_words.append(keys[i])

    return closest_words
    
def levenstein_distance(word1, word2):
    """ 
    Calcula la distancia de Levenshtein entre dos palabras
    ----
    Parámetros:
      word1 (str): Primera palabra
      word2 (str): Segunda palabra
    ----
    Returns:
      distance (int): Distancia de Levenshtein
    """
    # Inicializar la matriz
    matrix = [[0 for _ in range(len(word2) + 1)] for _ in range(len(word1) + 1)]
    # Inicializar la primera fila y la primera columna
    for i in range(len(word1) + 1):
        matrix[i][0] = i
    for j in range(len(word2) + 1):
        matrix[0][j] = j
    # Calcular la distancia de Levenshtein
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + substitution_cost
            )
    return matrix[-1][-1]

def save_translation(word1, word2, direction):
    dic = english_spanish_dict if direction == "en-es" else spanish_english_dict
    dic[word1] = word2
    # Ordenamos el diccionario
    ordered_dict = dict(sorted(dic.items()))
    # Guardamos el diccionario actualizado
    if direction == "en-es":
        english_spanish_dict[word1] = word2
        with open('english_spanish_dict.json', 'w', encoding='utf-8') as f:
            json.dump(ordered_dict, f, ensure_ascii=False, indent=4)
    else:
        spanish_english_dict[word1] = word2
        with open('spanish_english_dict.json', 'w', encoding='utf-8') as f:
            json.dump(ordered_dict, f, ensure_ascii=False, indent=4)

def order_translations():
  # Cargar el diccionario inglés-español
  with open('english_spanish_dict.json', 'r', encoding='utf-8') as f:
      english_spanish_dict = json.load(f)
  # Cargar diccionario español-inglés
  with open('spanish_english_dict.json', 'r', encoding='utf-8') as f:
      spanish_english_dict = json.load(f)
  # Ordenar las traducciones por orden alfabético
  ordered_dict = dict(sorted(english_spanish_dict.items()))
  ordered_dict_spanish = dict(sorted(spanish_english_dict.items()))
  # Guardar el diccionario ordenado
  with open('english_spanish_dict.json', 'w', encoding='utf-8') as f:
      json.dump(ordered_dict, f, ensure_ascii=False, indent=4)
  with open('spanish_english_dict.json', 'w', encoding='utf-8') as f:
      json.dump(ordered_dict_spanish, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    console_main()
    print(suggestions("hello"))