import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta, time
from typing import Tuple, List, Any
from schemas import GranularityEnum


def render_sidebar() -> Tuple[datetime, datetime, str]:
  st.sidebar.header("Фильтры")

  default_start = datetime.now() - timedelta(days=7)
  default_end = datetime.now()

  start_date = st.sidebar.date_input("Дата начала", default_start, format="DD.MM.YYYY")
  end_date = st.sidebar.date_input("Дата окончания", default_end, format="DD.MM.YYYY")

  start_dt = datetime.combine(start_date, time.min)
  end_dt = datetime.combine(end_date, time.max)

  duration_days = (end_date - start_date).days
  
  default_index = 0
  if duration_days > 30:
      default_index = 2
  elif duration_days > 7:
      default_index = 1

  granularity = st.sidebar.selectbox(
      "Детализация",
      options=["day", "week", "month", "hour"],
      index=default_index,
      format_func=lambda x: {
          "day": "По дням",
          "week": "По неделям",
          "month": "По месяцам",
          "hour": "По часам"
      }.get(x, x)
  )

  st.sidebar.divider()
  st.sidebar.checkbox("Режим отладки", key="debug_mode")

  return start_dt, end_dt, granularity


def plot_pie_chart(data: list, label_col: str, value_col: str, title: str):
  if not data:
    st.info(f"No data for {title}")
    return

  df = pd.DataFrame(data)
  fig = px.pie(df, names=label_col, values=value_col, title=title, hole=0.4)
  st.plotly_chart(fig, use_container_width=True)


def plot_bar_chart(data: list, x_col: str, y_col: str, title: str):
  if not data:
    st.info(f"No data for {title}")
    return

  df = pd.DataFrame(data)
  fig = px.bar(df, x=x_col, y=y_col, title=title)
  st.plotly_chart(fig, use_container_width=True)


def plot_emotion_dynamics_chart(data: List[Any], title: str = "Динамика эмоционального фона"):
  if not data:
    st.info(f"No data for {title}")
    return

  periods = [item.period_start for item in data]
  avg_sentiments = [item.average_sentiment_score for item in data]

  emotion_keys = set()
  key_to_label = {}
  
  for item in data:
    if item.breakdown:
      for k, v in item.breakdown.items():
        emotion_keys.add(k)
        if k not in key_to_label:
          key_to_label[k] = v.label_ru

  fig = make_subplots(specs=[[{"secondary_y": True}]])

  for emotion_key in sorted(emotion_keys):
    counts = []
    for item in data:
      if item.breakdown and emotion_key in item.breakdown:
        counts.append(item.breakdown[emotion_key].count)
      else:
        counts.append(0)
    
    fig.add_trace(
      go.Bar(
        x=periods,
        y=counts,
        name=key_to_label.get(emotion_key, emotion_key),
      ),
      secondary_y=False,
    )

  fig.add_trace(
    go.Scatter(
      x=periods,
      y=avg_sentiments,
      name="Среднее настроение",
      mode="lines+markers",
      line=dict(color="purple", width=3),
    ),
    secondary_y=True,
  )

  fig.update_layout(
    title_text=title,
    barmode="stack",
    xaxis_title="Период",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified"
  )

  fig.update_yaxes(title_text="Количество сообщений", secondary_y=False)
  fig.update_yaxes(title_text="Среднее настроение", secondary_y=True, range=[-1, 1])

  st.plotly_chart(fig, use_container_width=True)


def render_kpi(label: str, value: int):
  st.metric(label=label, value=f"{value:,}")
