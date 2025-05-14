from typing import Iterable

import plotly.express as px
import os
import uuid

def generate_graphic_html(x: Iterable, y: Iterable) -> str:
    os.makedirs("tmp", exist_ok=True)

    fig = px.scatter(x=x, y=y, labels={'x': 'Дата', 'y': 'Количество сообщений'}, title='График обращений')

    file_name = uuid.uuid4()
    file_path = f"tmp/{file_name}.html"
    fig.write_html(file_path)

    return file_path
