from typing import List, Tuple
import pandas as pd
import re
from collections import Counter

# Expresión regular para identificar emojis
EMOJI_PATTERN = re.compile(
    r'[\U0001F600-\U0001F64F'  # Emoticons
    r'\U0001F300-\U0001F5FF'  # Símbolos y pictogramas
    r'\U0001F680-\U0001F6FF'  # Transporte y mapas
    r'\U0001F1E0-\U0001F1FF'  # Banderas
    r'\U00002700-\U000027BF'  # Símbolos diversos
    r'\U00002600-\U000026FF'  # Otras pictografías
    r'\U0001F900-\U0001F9FF'  # Suplementos de pictogramas
    r'\U0001FA70-\U0001FAFF'  # Suplementos adicionales
    r'\U000025A0-\U000025FF'  # Formas geométricas
    r']+'
)

def extract_emojis(text: str) -> List[str]:
    """Extrae todos los emojis."""
    return EMOJI_PATTERN.findall(text) if isinstance(text, str) else []

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """Obtiene los 10 emojis más usados y su cantidad."""
    chunk_size = 100_000  # Procesa en bloques
    emoji_counter = Counter()  # Contador de emojis

    # Lee el archivo JSON por partes
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size):
        # Extrae emojis de los textos en la columna 'content' y contarlos de manera más eficiente
        chunk_emojis = chunk['content'].map(lambda x: extract_emojis(x))  # Usamos map en lugar de apply
        emojis_flattened = [emoji for emojis in chunk_emojis for emoji in emojis] 
        emoji_counter.update(emojis_flattened)  # Actualiza el contador con todos los emojis encontrados en el chunk

    # Obtener los 10 emojis más usados
    top_emojis = emoji_counter.most_common(10)
    return top_emojis
