from typing import List, Tuple
from datetime import datetime
import pandas as pd

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    df = pd.read_json(file_path, lines=True)
    
    # Convertir la columna 'date' a formato datetime y extraer solo la fecha
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    # Obtener las 10 fechas con más tweets
    top_dates = df.groupby('date').size().nlargest(10).reset_index(name='tweet_count')
    
    # Obtener el usuario más activo por cada fecha
    result = []
    for date in top_dates['date']:
        filtered_data = df[df['date'] == date]
        top_user = (
            filtered_data['user']
            .apply(lambda user: user['username'])  # Acceder al campo 'username' del diccionario 'user'
            .value_counts()
            .idxmax()  # Usuario con más publicaciones
        )
        result.append((date, top_user))
   
    return result