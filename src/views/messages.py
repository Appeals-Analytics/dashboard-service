import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

from api import ApiClient
from ui import plot_pie_chart, plot_emotion_dynamics_chart
from schemas import (
  CATEGORY_LEVEL_1_TRANSLATIONS,
  CATEGORY_LEVEL_2_TRANSLATIONS,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
  SENTIMENT_TRANSLATIONS,
  EMOTION_TRANSLATIONS
)

def render_messages(api: ApiClient, start_dt: datetime, end_dt: datetime, granularity: str):
  st.html(f"<script>window.scrollTo(0,0);</script><div style='display:none'>{uuid.uuid4()}</div>")

  category_l1 = st.session_state.get("selected_l1")
  category_l2 = st.session_state.get("selected_l2")

  if not category_l1 or not category_l2:
    st.session_state["page"] = "overview"
    st.rerun()
    return

  label_l1_ru = CATEGORY_LEVEL_1_TRANSLATIONS.get(CategoryLevel1Enum(category_l1), category_l1)
  label_l2_ru = CATEGORY_LEVEL_2_TRANSLATIONS.get(CategoryLevel2Enum(category_l2), category_l2)

  if st.button(f"⬅️ Назад к {label_l1_ru}"):
    st.session_state["page"] = "category_detail"
    del st.session_state["selected_l2"]
    st.rerun()

  st.title(f"Сообщения: {label_l1_ru} > {label_l2_ru}")

  with st.spinner("Загрузка данных..."):
    sentiments = api.get_sentiments(start_dt, end_dt, level1=category_l1, level2=category_l2)
    emotions = api.get_emotions(start_dt, end_dt, level1=category_l1, level2=category_l2)
    dynamics = api.get_emotion_dynamics(start_dt, end_dt, granularity=granularity, level1=category_l1, level2=category_l2)

  st.subheader("Динамика эмоционального фона")
  plot_emotion_dynamics_chart(dynamics.data)

  col1, col2 = st.columns(2)
  with col1:
    sentiments_data = [s.model_dump() for s in sentiments]
    plot_pie_chart(sentiments_data, "sentiment_label_ru", "count", "Сентименты")
  with col2:
    emotions_data = [e.model_dump() for e in emotions]
    plot_pie_chart(emotions_data, "emotion_label_ru", "count", "Эмоции")

  # Filters
  col1, col2, col3 = st.columns(3)
  with col1:
    search_query = st.text_input("Поиск")
  with col2:
    sentiment_map = {v: k.value for k, v in SENTIMENT_TRANSLATIONS.items()}
    selected_sentiments = st.multiselect("Сентимент", options=list(sentiment_map.keys()))
    sentiment_filter = [sentiment_map[s] for s in selected_sentiments] if selected_sentiments else None
  with col3:
    emotion_map = {v: k.value for k, v in EMOTION_TRANSLATIONS.items()}
    selected_emotions = st.multiselect("Эмоция", options=list(emotion_map.keys()))
    emotion_filter = [emotion_map[e] for e in selected_emotions] if selected_emotions else None

  with st.spinner("Загрузка сообщений..."):
    messages = api.get_messages(
      start_dt,
      end_dt,
      level1=category_l1,
      level2=category_l2,
      search=search_query if search_query else None,
      sentiment=sentiment_filter,
      emotion=emotion_filter,
    )

  if messages:
    messages_data = [m.model_dump() for m in messages]
    df_msgs = pd.DataFrame(messages_data)

    cols_to_show = [
      "event_date", "text", "sentiment_label_ru", "emotion_label_ru",
      "source", "user_id", "external_id", "lang_code", "lang_score", "emotion_score", "sentiment_score"
    ]
    cols_to_show = [c for c in cols_to_show if c in df_msgs.columns]

    with st.container():

      table_height = 21 * 35

      st.dataframe(
        df_msgs[cols_to_show],
        width="stretch",
        height=table_height,
        hide_index=True,
        column_config={
          "event_date": st.column_config.DatetimeColumn("Дата", format="D MMM YYYY, HH:mm"),
          "text": st.column_config.TextColumn("Текст", width="large"),
          "sentiment_label_ru": "Сентимент",
          "emotion_label_ru": "Эмоция",
          "source": "Источник",
          "user_id": "User ID",
          "external_id": "External ID",
          "lang_code": "Язык",
          "lang_score": st.column_config.NumberColumn("Lang Score", format="%.2f"),
          "emotion_score": st.column_config.NumberColumn("Emotion Score", format="%.2f"),
          "sentiment_score": st.column_config.NumberColumn("Sentiment Score", format="%.2f")
        },
      )
  else:
    st.info("Сообщения не найдены.")
