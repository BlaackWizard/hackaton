from typing import Iterable

import plotly.express as px
import os
import uuid

import plotly.graph_objs as go
from io import BytesIO

def generate_graphic_html(x: list[str], y: list[int]) -> bytes:
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines+markers'))
    fig.update_layout(title='Сообщения за последние 30 дней', xaxis_title='Дата', yaxis_title='Количество')

    html_bytes = fig.to_html(full_html=True, include_plotlyjs='cdn').encode('utf-8')
    return html_bytes
