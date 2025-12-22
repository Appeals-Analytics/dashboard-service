import streamlit as st
import pandas as pd
from datetime import datetime

from api import ApiClient
from ui import plot_pie_chart, plot_emotion_dynamics_chart
from schemas import CATEGORY_LEVEL_1_TRANSLATIONS, CategoryLevel1Enum


def render_category_detail(api: ApiClient, start_dt: datetime, end_dt: datetime, granularity: str):
  category_l1 = st.session_state.get("selected_l1")
  if not category_l1:
    st.session_state["page"] = "overview"
    st.rerun()
    return

  try:
    label_ru = CATEGORY_LEVEL_1_TRANSLATIONS.get(CategoryLevel1Enum(category_l1), category_l1)
  except ValueError:
    label_ru = category_l1

  if st.button("⬅️ Назад"):
    st.session_state["page"] = "overview"
    del st.session_state["selected_l1"]
    st.rerun()

  st.title(f"Аналитика: {label_ru}")

  with st.spinner("Загрузка данных категории..."):
    sentiments = api.get_sentiments(start_dt, end_dt, level1=category_l1)
    emotions = api.get_emotions(start_dt, end_dt, level1=category_l1)
    subcategories = api.get_categories_l2(start_dt, end_dt, level1=category_l1)
    dynamics = api.get_emotion_dynamics(start_dt, end_dt, granularity=granularity, level1=category_l1)

  st.subheader("Динамика эмоционального фона")
  plot_emotion_dynamics_chart(dynamics.data)

  col1, col2 = st.columns(2)
  with col1:
    sentiments_data = [s.model_dump() for s in sentiments]
    plot_pie_chart(sentiments_data, "sentiment_label_ru", "count", "Сентименты")
  with col2:
    emotions_data = [e.model_dump() for e in emotions]
    plot_pie_chart(emotions_data, "emotion_label_ru", "count", "Эмоции")

  st.subheader("Подкатегории (Уровень 2)")
  if subcategories:
    subcategories_data = [s.model_dump() for s in subcategories]
    df_sub = pd.DataFrame(subcategories_data)

    def format_emotions(emotions_dict):
      if not emotions_dict:
        return ""
      sorted_emotions = sorted(emotions_dict.items(), key=lambda x: x[1], reverse=True)
      return ", ".join([f"{k}: {v}" for k, v in sorted_emotions])

    df_sub["top_emotions"] = df_sub["emotions_ru"].apply(format_emotions)
    display_df = df_sub[["label_ru", "count", "top_emotions"]].copy()
    display_df.columns = ["Подкатегория", "Количество", "Эмоции"]

    st.write("Выберите подкатегорию для просмотра сообщений:")
    event = st.dataframe(
      display_df,
      on_select="rerun",
      selection_mode="single-row",
      width="stretch",
      hide_index=True,
    )

    if event.selection.rows:
      selected_index = event.selection.rows[0]
      selected_l2 = subcategories[selected_index].label
      st.session_state["page"] = "messages"
      st.session_state["selected_l2"] = selected_l2
      st.rerun()
  else:
    st.info("Подкатегории не найдены.")
