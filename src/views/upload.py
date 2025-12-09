import streamlit as st

from api import ApiClient


def render_upload(api: ApiClient):
  st.title("Загрузка данных")

  st.subheader("Загрузка одного файла")
  uploaded_file = st.file_uploader(
    "Выберите файл", type=["csv", "xlsx", "xls", "json", "parquet"], key="single_upload"
  )
  if uploaded_file is not None:
    if st.button("Загрузить файл"):
      with st.spinner("Загрузка..."):
        result = api.upload_file(uploaded_file)
        if result:
          st.success("Файл успешно загружен!")
          st.json(result)

  st.divider()

  st.subheader("Загрузка нескольких файлов")
  uploaded_files = st.file_uploader(
    "Выберите файлы",
    type=["csv", "xlsx", "xls", "json", "parquet"],
    accept_multiple_files=True,
    key="multi_upload",
  )
  if uploaded_files:
    if st.button("Загрузить файлы"):
      with st.spinner("Загрузка..."):
        result = api.upload_multiple_files(uploaded_files)
        if result:
          st.success("Файлы успешно загружены!")
          st.json(result)
