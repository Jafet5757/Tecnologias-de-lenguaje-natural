import nltk
import re
from datasets import load_dataset
from nltk.corpus import stopwords
import pandas as pd

# Descargar stopwords de nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

TRAINING_PRHASES = 1000

# Cargar el corpus paralelo de OPUS para inglés-español
dataset = load_dataset("Helsinki-NLP/opus_books", "en-es")

# Función de limpieza
def clean_text(text):
    """ 
      Limpia el texto eliminando caracteres especiales, signos de puntuación y números
      
      -- Parámetros:
      text: texto a limpiar 
    """
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales, signos de puntuación (puntos, comas, etc) y números
    text = re.sub(r'[^a-zA-Zñ\s]', '', text)
    return text

def read_document(file_name):
    with open(file_name, 'r') as file:
        return file.read().splitlines()

# Entrenar el modelo bayesiano
def train(data_from_file=False, phrases_file_name='phrases.txt'):
    """ 
      Entrena el modelo bayesiano con las frases del dataset
      
      -- Parámetros:
      data_from_file: si se obtiene la data de un archivo
      phrases_file_name: nombre del archivo con las frases 
    """
    # creamos un diccionario de palabras que almacena su frecuencia
    words_frequency = {}
    # creamos un data frame para probabilidad conjunta, dónde cada fila y columna es una palabra y la diagonal es la probabilidad conjunta
    joint_probability = pd.DataFrame()
    phrases = [clean_text(item['translation']['es']) for item in dataset['train']] if not data_from_file else read_document(phrases_file_name)# Obtenemos frases en español
    phrases = phrases[:TRAINING_PRHASES]
    # Iteramos las frases
    for phrase in phrases:
        # Dividir el texto en palabras
        words = phrase.split()
        # Iteramos las palabras
        for i, word in enumerate(words):
            # Limpiamos la palabra
            word = clean_text(word.strip())
            # Incrementamos la frecuencia de la palabra
            if word in words_frequency:
                words_frequency[word] += 1
            else:
                words_frequency[word] = 1
            # Obtenemos su palabra anterior
            if i > 0:
                previous_word = clean_text(words[i-1].strip())
                # Creamos una columna con la probabilidad de la palabra anterior si no existe
                if previous_word not in joint_probability.columns:
                    joint_probability[previous_word] = 0
                # Obtenemos la probabilidad conjunta de la palabra anterior y la palabra actual
                joint_probability.loc[word, previous_word] = joint_probability.loc[word, previous_word] + 1 if word in joint_probability.index else 1
    # Guardamos la probabilidad conjunta en un archivo CSV
    joint_probability.to_csv('joint_probability.csv')
    # Convertimos el diccionario a un DataFrame
    df = pd.DataFrame(words_frequency.items(), columns=['word', 'frequency'])
    # Agregamos una columna con la probabilidad de la palabra
    df['probability'] = df['frequency'] / df['frequency'].sum()
    # Guardamos el DataFrame en un archivo CSV
    df.to_csv('words_frequency.csv', index=False)

def predict(word_a, word_b, print_probabilities=False):
    """ 
      Predice la probabilidad de p(a|b) y p(b|a) y retorna el orden de las palabras
      
      -- Parámetros:
      word_a: palabra a
      word_b: palabra b

      -- Retorna:
      word_a, word_b si p(a|b) > p(b|a) o p(a|b) = p(b|a)
      word_b, word_a si p(b|a) > p(a|b)
    """

    # Cargar el DataFrame con las frecuencias
    df = pd.read_csv('words_frequency.csv')
    # Cargamos el DataFrame con las probabilidades conjuntas
    joint_probability = pd.read_csv('joint_probability.csv', index_col=0)
    try:
      # Obtenemos la probabilidad de la palabra a
      p_a = df[df['word'] == word_a]['probability'].values[0]
      # Obtenemos la probabilidad de la palabra b
      p_b = df[df['word'] == word_b]['probability'].values[0]
    except IndexError:
      print("Error: palabra no encontrada")
      # Si alguna de las palabras no está en el diccionario, retornamos el mismo orden
      return word_a, word_b
    # Si alguna de las palabras no está en el diccionario, retornamos el mismo orden
    if p_a == 0 or p_b == 0:
        return word_a, word_b
    try:
      # Obtenemos la probabilidad conjunta de las palabras
      p_ab = (joint_probability.loc[word_a, word_b] if word_a in joint_probability.index and word_b in joint_probability.columns else 0) + (joint_probability.loc[word_b, word_a] if word_a in joint_probability.index and word_b in joint_probability.columns else 0)
      # calculamos la probabilidad de p(a|b)
      p_a_b = p_ab / p_b
      # calculamos la probabilidad de p(b|a)
      p_b_a = p_ab / p_a
    except KeyError:
      print("Error: palabra no encontrada")
      # Si alguna de las palabras no está en el diccionario, retornamos el mismo orden
      return word_a, word_b

    # Si p(a|b) > p(b|a) o p(a|b) = p(b|a) retornamos el orden de las palabras
    if p_a_b > p_b_a or p_a_b == p_b_a:
        if print_probabilities:
            print(f"p({word_a}|{word_b}): {p_a_b}")
            print(f"p({word_b}|{word_a}): {p_b_a}")
        return word_a, word_b
    # Si p(b|a) > p(a|b) retornamos el orden de las palabras
    else:
        if print_probabilities:
            print(f"p({word_a}|{word_b}): {p_a_b}")
            print(f"p({word_b}|{word_a}): {p_b_a}")
        return word_b, word_a
    
def order_words(phrase):
    """ 
      Ordena las palabras de una frase en base a la probabilidad conjunta de las palabras
      
      -- Parámetros:
      phrase: frase a ordenar
    """
    # Dividir el texto en palabras
    words = phrase.split()
    # Iteramos las palabras
    for i, word in enumerate(words):
        # Limpiamos la palabra
        words[i] = clean_text(word.strip())
    # Ordenamos las palabras
    for i in range(len(words)-1):
        words[i], words[i+1] = predict(words[i], words[i+1])
    # Retornamos la frase ordenada
    return ' '.join(words)

if __name__ == '__main__':
    #train(data_from_file=True)
    print("Frase ordenada: ", predict('rojo', 'carro', print_probabilities=True))
        