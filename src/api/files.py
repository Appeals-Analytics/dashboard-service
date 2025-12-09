from typing import Dict
import streamlit as st

from api.base import BaseApiClient


class FilesApi(BaseApiClient):

  def upload_file(self, file) -> Dict:
    if file.size > 100 * 1024 * 1024:  # 100MB
      st.error("File size exceeds 100MB limit.")
      return {}

    files = {"file": (file.name, file, file.type)}
    return self._post("/files/upload", files=files)

  def upload_multiple_files(self, file_list) -> Dict:
    valid_files = []
    for f in file_list:
      if f.size > 100 * 1024 * 1024:
        st.warning(f"Skipping {f.name}: File size exceeds 100MB limit.")
        continue
      valid_files.append(f)

    if not valid_files:
      st.error("No valid files to upload.")
      return {}

    files = [("files", (f.name, f, f.type)) for f in valid_files]
    return self._post("/files/multiple-upload", files=files)
