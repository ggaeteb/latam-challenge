from typing import List, Tuple
import pandas as pd
import re
from collections import Counter

# Expresión regular para detectar menciones (@usuario)
MENTION_PATTERN = re.compile(r'@(\w+)')  # Compilar la expresión regular una vez

def extract_mentions(text: str) -> List[str]:
    """Extrae todas las menciones (@usuario) de un texto."""
    return MENTION_PATTERN.findall(text) if isinstance(text, str) else []  # Validación compacta

def q3_memory(file_path: str, chunk_size: int = 100000) -> List[Tuple[str, int]]:
    """Obtiene el top 10 de usuarios más mencionados procesando por chunks."""
    mention_counter = Counter()  # Contador global para las menciones

    # Lee el archivo JSON en bloques para procesar por partes
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size):
        # Extraer menciones directamente en el DataFrame
        mentions_series = chunk['content'].dropna().map(extract_mentions)  # Evitar procesar valores NaN

        # Contar menciones en el chunk sin crear nuevas estructuras innecesarias
        chunk_counter = Counter(mention for mentions in mentions_series for mention in mentions)
        mention_counter.update(chunk_counter)  # Actualizar el contador global con el del chunk

        # Liberar memoria usada por el chunk explícitamente
        del chunk, mentions_series, chunk_counter

    # Obtener los 10 usuarios más mencionados
    top_mentions = mention_counter.most_common(10)

    return top_mentions
