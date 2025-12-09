import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

from api import ApiClient
from ui import plot_pie_chart, plot_bar_chart, render_kpi


def render_overview(api: ApiClient, start_dt: datetime, end_dt: datetime):
  st.html(f"<script>window.scrollTo(0,0);</script><div style='display:none'>{uuid.uuid4()}</div>")
  st.title("Общая аналитика")

  with st.spinner("Загрузка данных..."):
    sentiments = api.get_sentiments(start_dt, end_dt)
    emotions = api.get_emotions(start_dt, end_dt)
    categories = api.get_categories_l1(start_dt, end_dt)

  total_requests = sum(c.count for c in categories)
  render_kpi("Всего запросов", total_requests)

  col1, col2 = st.columns(2)
  with col1:
    sentiments_data = [s.model_dump() for s in sentiments]
    plot_pie_chart(sentiments_data, "sentiment_label_ru", "count", "Распределение сентиментов")
  with col2:
    if emotions:
      emotions_data = [e.model_dump() for e in emotions]
      df_emotions = pd.DataFrame(emotions_data).sort_values("count", ascending=False)
      if len(df_emotions) > 10:
        top_10 = df_emotions.head(10)
        other_count = df_emotions.iloc[10:]["count"].sum()
        top_10 = pd.concat([
          top_10,
          pd.DataFrame([{"emotion_label": "Other", "emotion_label_ru": "Другое", "count": other_count}]),
        ])
        plot_pie_chart(top_10.to_dict("records"), "emotion_label_ru", "count", "Распределение эмоций (Топ 10)")
      else:
        plot_pie_chart(emotions_data, "emotion_label_ru", "count", "Распределение эмоций")
    else:
      st.info("No emotion data")

  st.subheader("Категории (Уровень 1)")
  categories_data = [c.model_dump() for c in categories]
  plot_bar_chart(categories_data, "label_ru", "count", "Запросы по категориям")

  if categories:
    df_cats = pd.DataFrame(categories_data)

    def format_emotions(emotions_dict):
      if not emotions_dict:
        return ""
      sorted_emotions = sorted(emotions_dict.items(), key=lambda x: x[1], reverse=True)
      return ", ".join([f"{k}: {v}" for k, v in sorted_emotions])

    df_cats["top_emotions"] = df_cats["emotions_ru"].apply(format_emotions)
    display_df = df_cats[["label_ru", "count", "top_emotions"]].copy()
    display_df.columns = ["Категория", "Количество", "Эмоции"]

    st.write("Выберите категорию для просмотра деталей:")
    event = st.dataframe(
      display_df,
      on_select="rerun",
      selection_mode="single-row",
      width="stretch",
      hide_index=True,
    )

    if event.selection.rows:
      selected_index = event.selection.rows[0]
      selected_category = categories[selected_index].label
      st.session_state["page"] = "category_detail"
      st.session_state["selected_l1"] = selected_category
      st.rerun()
