import json
import re
import ordenador_palabras_bayesiano as ordenador

# Cargar el diccionario inglés-español
with open('english_spanish_dict.json', 'r', encoding='utf-8') as f:
    english_spanish_dict = json.load(f)

# Función de limpieza
def clean_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

while True:
  # Menu de opciones
  print("\n"*4)
  print("Traductor inglés-español")
  print("1. Traducir palabra o frase")
  print("2. Salir")
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

  else:
      print("Saliendo...")
      break

