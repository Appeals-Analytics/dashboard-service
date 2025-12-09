import httpx
from typing import Dict, Any
import streamlit as st

from config import settings


class BaseApiClient:

  def __init__(self):
    self.base_url = settings.api_base_url
    self.client = httpx.Client(base_url=self.base_url, timeout=30.0)

  def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
    if st.session_state.get("debug_mode"):
      st.write(f"**Request:** `GET {self.base_url}{endpoint}`")
      st.json(params)

    try:
      response = self.client.get(endpoint, params=params)

      if st.session_state.get("debug_mode"):
        st.write(f"**Response Status:** `{response.status_code}`")
        try:
          st.json(response.json())
        except:
          st.text(response.text)

      response.raise_for_status()
      return response.json()
    except httpx.RequestError as e:
      st.error(f"API Connection Error: {e}")
      return []
    except httpx.HTTPStatusError as e:
      st.error(f"API Error {e.response.status_code}: {e.response.text}")
      return []

  def _post(self, endpoint: str, files: list = None) -> Dict:
    try:
      response = self.client.post(endpoint, files=files)
      response.raise_for_status()
      return response.json()
    except httpx.HTTPStatusError as e:
      st.error(f"Upload Error {e.response.status_code}: {e.response.text}")
      return {}
    except httpx.RequestError as e:
      st.error(f"Upload Connection Error: {e}")
      return {}
