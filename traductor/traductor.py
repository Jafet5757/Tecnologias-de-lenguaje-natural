import re
import nltk
from nltk.translate.bleu_score import corpus_bleu
from datasets import load_dataset
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords

# Descargar stopwords de nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Función de limpieza
def clean_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Eliminar stopwords
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

# Cargar el corpus paralelo de OPUS para inglés-español
dataset = load_dataset("Helsinki-NLP/opus_books", "en-es")

# Tamaño del conjunto de datos
print(f"Tamaño del conjunto de datos: {dataset['train'].num_rows}")

# Mostrar las primeras frases
for i in range(3):
    print(f"Inglés: {dataset['train'][i]['translation']['en']}")
    print(f"Español: {dataset['train'][i]['translation']['es']}\n")

print("Getting data...")
X = [clean_text(item['translation']['en']) for item in dataset['train']]
y = [item['translation']['es'] for item in dataset['train']]

# Dividimos el dataset a la mitad para que sea más rápido
X = X[:len(X)//2+len(X)//4]
y = y[:len(y)//2+len(y)//4]

print("Splitting data...")
# Dividimos los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=32)

print("Tokenizing model...")
# Crear un modelo de clasificación de texto
model = make_pipeline(CountVectorizer(), MultinomialNB())

print("Training model...")
# Entrenar el modelo
model.fit(X_train, y_train)

# Predecir el conjunto de prueba
y_pred = model.predict(X_test)

# Mostramos algunas predicciones
for i in range(5):
    print(f"Texto: {X_test[i]}")
    print(f"Predicción: {y_pred[i]}\n")
    print(f"Real: {y_test[i]}\n")

# Calcular la precisión
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión: {accuracy:.2f}")

# Calcular el puntaje BLEU
references = [[text.split()] for text in y_test]
candidates = [text.split() for text in y_pred]
bleu_score = corpus_bleu(references, candidates)
print(f"Puntaje BLEU: {bleu_score:.2f}")