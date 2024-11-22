from typing import List, Tuple
import pandas as pd
import re
from collections import Counter

# Expresión regular para detectar menciones (@usuario)
MENTION_PATTERN = r'@(\w+)'

def extract_mentions(text: str) -> List[str]:
    """Extrae todas las menciones (@usuario) de un texto."""
    if isinstance(text, str):  # Verifica que el valor es una cadena de texto
        return re.findall(MENTION_PATTERN, text)  # Busca menciones con la expresión regular
    return []  # Si no es un texto válido, devuelve una lista vacía

def q3_time(file_path: str, chunk_size: int = 100000) -> List[Tuple[str, int]]:
    """Obtiene el top 10 de usuarios más mencionados en función de las menciones (@) con procesamiento por chunks."""
    mention_counter = Counter()  # Contador global para las menciones

    # Lee el archivo en bloques (chunks)
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size):
        # Asegurarse de que la columna 'content' sea de tipo string
        chunk['mentions'] = chunk['content'].apply(lambda x: extract_mentions(str(x)))   # Valida si el contenido es una cadena

        # Contar menciones en el chunk
        for mentions in chunk['mentions']:
            mention_counter.update(mentions)  # Contar las menciones

    # Obtener los 10 usuarios más mencionados
    top_mentions = mention_counter.most_common(10)

    # Devolver el Top 10 de usuarios más mencionados y su frecuencia
    return top_mentions
