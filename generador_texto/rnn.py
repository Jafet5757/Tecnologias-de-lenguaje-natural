from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.utils import to_categorical
import numpy as np
import re

# Ejemplo de limpieza
def limpiar_texto(texto):
    texto = re.sub(r"[^a-zA-Z\s]", "", texto)  # Solo letras y espacios
    texto = texto.lower()  # Minúsculas
    texto = texto.strip()  # Elimina espacios extra
    return texto

def tokenizar_texto(texto):
  # Tokenización
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts([texto])
  secuencias = tokenizer.texts_to_sequences([texto])[0]

  # Creación de secuencias de entrada y salida
  secuencias_entrada = []
  secuencias_salida = []

  secuencia_longitud = 5  # Tamaño del contexto
  for i in range(secuencia_longitud, len(secuencias)):
      entrada = secuencias[i - secuencia_longitud:i]
      salida = secuencias[i]  
      secuencias_entrada.append(entrada)
      secuencias_salida.append(salida)
  return secuencias_entrada, secuencias_salida, tokenizer, secuencia_longitud


def crear_modelo(tokenizer, secuencias_entrada, secuencias_salida, secuencia_longitud=5):
  # Parámetros
  vocab_size = len(tokenizer.word_index) + 1

  # Modelo LSTM
  model = Sequential()
  model.add(Embedding(vocab_size, 50, input_length=secuencia_longitud))
  model.add(LSTM(100, return_sequences=False))
  model.add(Dense(vocab_size, activation='softmax'))

  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

  secuencias_salida = to_categorical(secuencias_salida, num_classes=vocab_size)

  # Entrenamiento
  model.fit(np.array(secuencias_entrada), secuencias_salida, epochs=50, batch_size=32)

  return model


def generar_texto(model, tokenizer, semilla, longitud_texto=50, secuencia_longitud=5):
    for _ in range(longitud_texto):
        secuencia = tokenizer.texts_to_sequences([semilla])[0]
        secuencia = pad_sequences([secuencia], maxlen=secuencia_longitud, padding='pre')
        prediccion = model.predict(secuencia, verbose=0)
        palabra_predicha = tokenizer.index_word[np.argmax(prediccion)]
        semilla += " " + palabra_predicha
    return semilla



if __name__ == "__main__":
    semilla = "era una noche"

    texto = "Era una noche oscura y tormentosa en la que el viento soplaba con fuerza. De repente, un rayo iluminó el cielo y un trueno retumbó en la distancia. En ese momento, una figura misteriosa apareció en el horizonte y se acercó lentamente. Era un hombre alto y delgado con ojos fríos y penetrantes que parecían ver a través de ti. Se detuvo frente a ti y te miró fijamente, como si estuviera leyendo tus pensamientos. Entonces, con una voz suave y siniestra, te dijo: 'Bienvenido al mundo de las sombras, donde nada es lo que parece y todo es posible'."

    texto = limpiar_texto(texto)
    secuencias_entrada, secuencias_salida, tokenizer, secuencia_longitud = tokenizar_texto(texto)

    model = crear_modelo(tokenizer, secuencias_entrada, secuencias_salida, secuencia_longitud)

    texto_generado = generar_texto(model, tokenizer, semilla)
    print(texto_generado)
