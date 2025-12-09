import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, time
from typing import Tuple


def render_sidebar() -> Tuple[datetime, datetime]:
  st.sidebar.header("Фильтры")

  default_start = datetime.now() - timedelta(days=7)
  default_end = datetime.now()

  start_date = st.sidebar.date_input("Дата начала", default_start, format="DD.MM.YYYY")
  end_date = st.sidebar.date_input("Дата окончания", default_end, format="DD.MM.YYYY")

  start_dt = datetime.combine(start_date, time.min)
  end_dt = datetime.combine(end_date, time.max)

  st.sidebar.divider()
  st.sidebar.checkbox("Режим отладки", key="debug_mode")

  return start_dt, end_dt


def plot_pie_chart(data: list, label_col: str, value_col: str, title: str):
  if not data:
    st.info(f"No data for {title}")
    return

  df = pd.DataFrame(data)
  fig = px.pie(df, names=label_col, values=value_col, title=title, hole=0.4)
  st.plotly_chart(fig, width='stretch')


def plot_bar_chart(data: list, x_col: str, y_col: str, title: str):
  if not data:
    st.info(f"No data for {title}")
    return

  df = pd.DataFrame(data)
  fig = px.bar(df, x=x_col, y=y_col, title=title)
  st.plotly_chart(fig, width='stretch')


def render_kpi(label: str, value: int):
  st.metric(label=label, value=f"{value:,}")
