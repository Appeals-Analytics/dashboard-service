import streamlit as st
from config import settings
from api import ApiClient
from ui import render_sidebar
from views import render_overview, render_category_detail, render_messages, render_upload

st.set_page_config(page_title=settings.app_title, layout="wide", initial_sidebar_state="expanded")


def main():
  if "page" not in st.session_state:
    st.session_state["page"] = "overview"

  if "nav_section" not in st.session_state:
    st.session_state["nav_section"] = "Аналитика"

  api = ApiClient()

  st.sidebar.title("Навигация")

  col1, col2 = st.sidebar.columns(2)

  with col1:
    if st.sidebar.button(
      "📊 Аналитика" if st.session_state["nav_section"] == "Аналитика" else "Аналитика",
      width='stretch'
      ):
      st.session_state["nav_section"] = "Аналитика"
      st.rerun()

  with col2:
    if st.sidebar.button(
      "📁 Загрузка" if st.session_state["nav_section"] == "Загрузка данных" else "Загрузка данных",
      width='stretch'
      ):
      st.session_state["nav_section"] = "Загрузка данных"
      st.rerun()

  nav_selection = st.session_state["nav_section"]

  if nav_selection == "Аналитика":
    start_dt, end_dt = render_sidebar()

    page = st.session_state["page"]

    if page == "overview":
      render_overview(api, start_dt, end_dt)
    elif page == "category_detail":
      render_category_detail(api, start_dt, end_dt)
    elif page == "messages":
      render_messages(api, start_dt, end_dt)
    else:
      render_overview(api, start_dt, end_dt)

  elif nav_selection == "Загрузка данных":
    render_upload(api)


if __name__ == "__main__":
  main()
