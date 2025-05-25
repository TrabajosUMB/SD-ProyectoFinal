from wordcloud import WordCloud
import matplotlib.pyplot as plt
from .models import JobOffer
import nltk
from nltk.corpus import stopwords
import os

nltk.download('stopwords')

def generar_nube_palabras():
    titles = JobOffer.objects.values_list('title', flat=True)
    text = ' '.join(titles)

    # Limpieza básica
    stop_words = set(stopwords.words('spanish'))
    palabras = [word.lower() for word in text.split() if word.lower() not in stop_words and len(word) > 3]
    texto_filtrado = ' '.join(palabras)

    # Crear y mostrar nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_filtrado)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()

    # Guardar imagen
    path = os.path.join("api", "wordcloud.png")
    wordcloud.to_file(path)
    print(f"Nube de palabras guardada en: {path}")

