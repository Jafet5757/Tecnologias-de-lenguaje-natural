const textContainer = document.getElementById('text');
const orderSwitch = document.getElementById('order-switch');
const switchLenguageButton = document.getElementById('switch-lenguage');
const saveNewTranslationButton = document.getElementById('saveNewTranslation-button');
let traductionDirection = 'en-es';

const suggestionsCard = (suggestions) => {
  const keys = Object.keys(suggestions);
  const suggestions_text = [];
  
  for (const word of keys) {
    for (const suggestion of suggestions[word].suggestions) {
      suggestions_text.push(`<li><a href="#" onclick="replaceAllWords('${word}', '${suggestion}')">${suggestion}</a></li>`);
    }
  }

  const card = `
    <div class="card">
      <div class="card-body">
        <p class="fs-5">Sugerencias</p>
        <ul>
          ${suggestions_text.join('')}
        </ul>
      </div>
    </div>
  `;
  
  return card; // Devuelve el HTML para usarlo en el DOM
};

// when pressing a key, translate the text
textContainer.addEventListener("input", async () => {
  await translateText();
});
// when changing the order option, translate the text
orderSwitch.addEventListener("change", async () => {
  await translateText();
});

// when pressing the switch button, change the translation direction
switchLenguageButton.addEventListener("click", async () => {
  if (traductionDirection === 'en-es') {
    traductionDirection = 'es-en';
    document.getElementById('l1-label').innerText = 'Español';
    document.getElementById('l2-label').innerText = 'Inglés';
  } else {
    traductionDirection = 'en-es';
    document.getElementById('l1-label').innerText = 'Inglés';
    document.getElementById('l2-label').innerText = 'Español';
  }
});

saveNewTranslationButton.addEventListener("click", async () => {
  const newText = document.getElementById('newText').value;
  const newTranslation = document.getElementById('newTranslation').value;
  try {
    const response = await fetch('/save-translation', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ newText, newTranslation, direction: traductionDirection }),
    });
    const data = await response.json();
  } catch (error) {
    console.error('Error:', error);
    Swal.fire({
      title: 'Error',
      text: 'Ha ocurrido un error al intentar guardar la traducción',
      icon: 'error'
    });
  }
  // show swal alert
  Swal.fire({
    title: 'Guardado',
    text: 'La traducción ha sido guardada correctamente',
    icon: 'success',
    timer: 2000,
    timerProgressBar: true
  });
});

async function translateText() {
  const language = document.getElementById('language').value;
  const output = document.getElementById('translation');
  const response = await fetch('/translate', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phrase:textContainer.value, language, order: orderSwitch.checked, direction: traductionDirection }),
  });
  const data = await response.json();
  console.log(data);
  // Put the translation in the output div
  output.value = data.translation;
  // if there are suggestions, show them
  const suggestions = document.getElementById('suggestions-col');
  suggestions.innerHTML = suggestionsCard(data.suggestions);
}

async function replaceAllWords(word, newWord) {
  const text = textContainer.value;
  // replace capital and lower case
  const re = new RegExp(word, 'gi');
  const newText = text.replace(re, newWord);
  textContainer.value = newText;
  await translateText();
}