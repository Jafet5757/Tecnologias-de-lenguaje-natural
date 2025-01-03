import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 1. Datos de entrenamiento (secuencia sencilla de números)
# Secuencia de números: [1, 2, 3, 4, 5, 6, 7, 8, 9]
secuencia = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

# Crear entradas y salidas (contexto y próxima palabra)
# Entrada: un solo número, Salida: el siguiente número
entrada = []
salida = []

for i in range(len(secuencia)-1):
    entrada.append([secuencia[i]])  # Usamos un solo número como entrada
    salida.append(secuencia[i+1])   # El siguiente número en la secuencia

entrada = np.array(entrada)
salida = np.array(salida)

# 2. Construcción del modelo LSTM
model = Sequential()
model.add(LSTM(50, input_shape=(entrada.shape[1], 1)))  # LSTM con 50 unidades
model.add(Dense(1))  # Una salida: el siguiente número en la secuencia

model.compile(loss='mean_squared_error', optimizer='adam')

# 3. Ajuste de dimensiones para la entrada LSTM (LSTM requiere entrada con 3D)
entrada = entrada.reshape((entrada.shape[0], entrada.shape[1], 1))

# 4. Entrenamiento
model.fit(entrada, salida, epochs=200, verbose=0)

# 5. Generación de una secuencia con la red entrenada
def generar_siguiente_numero(model, semilla):
    semilla = semilla.reshape((1, len(semilla), 1))
    prediccion = model.predict(semilla, verbose=0)
    return prediccion[0][0]

# Semilla inicial
semilla = np.array([1])

# Generar el siguiente número
siguiente_numero = generar_siguiente_numero(model, semilla)
print(f"El siguiente número después de {semilla} es: {siguiente_numero}")
