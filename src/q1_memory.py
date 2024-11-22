from typing import List, Tuple
from datetime import datetime
import pandas as pd

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    chunk_size = 100_000  # Tamaño del chunk para leer datos por partes
    user_date_counts = []

    # Leer el archivo JSON por partes
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size):
        # convierte 'date' a fecha y extrae el 'username' en el chunk
        chunk['date'] = pd.to_datetime(chunk['date']).dt.date
        chunk['username'] = chunk['user'].apply(lambda user: user['username'])
        
        # Contar tweets por usuario y fecha en el chunk
        counts = chunk.groupby(['date', 'username']).size().reset_index(name='tweet_count')
        user_date_counts.append(counts)

    # Combinar resultados de todos los chunks
    combined_counts = pd.concat(user_date_counts, ignore_index=True)

    # Obtiene las 10 fechas con más tweets
    top_dates = (
        combined_counts.groupby('date')['tweet_count']
        .sum()
        .nlargest(10)
        .index
    )

    # Filtrar por las principales fechas
    filtered_counts = combined_counts[combined_counts['date'].isin(top_dates)]

    # Agrupar por fecha y encontrar el usuario más activo por fecha
    result = (
        filtered_counts.groupby('date')
        .apply(lambda group: group.loc[group['tweet_count'].idxmax(), 'username'])
        .reset_index(name='top_user')
    )

    # Convertir resultado a lista de tuplas
    return list(result.itertuples(index=False, name=None))
