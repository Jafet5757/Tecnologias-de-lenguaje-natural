from flask import Flask, request, render_template
import traductor_bayesiano as traductor

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
  """ 
  Traduce una frase de inglés a español
  ----
  Parámetros:
    phrase (str): Frase en inglés
  ----
  Returns:
    translation str: Frase traducida a español
    suggestions list: Lista de sugerencias para palabras no encontradas 
  """
  data = request.get_json()

  phrase = data["phrase"]
  order = data["order"]
  direction = data["direction"]

  translation, suggestions_list = traductor.translate(phrase, order, direction)

  return {"translation": translation, "suggestions": suggestions_list}

@app.route("/save-translation", methods=["POST"])
def save_translation():
  """ 
  Guarda una traducción en el diccionario
  ----
  Parámetros:
    word1 (str): Palabra en inglés
    word2 (str): Traducción en español
    direction (str): Dirección de la traducción
  ----
  Returns:
    message str: Mensaje de confirmación
  """
  data = request.get_json()

  word1 = data["newText"]
  word2 = data["newTranslation"]
  direction = data["direction"]

  traductor.save_translation(word1, word2, direction)

  return {"message": "Translation saved successfully"}


if __name__ == "__main__":
  app.run(debug=True)