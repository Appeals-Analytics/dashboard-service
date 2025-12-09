from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class EmotionCountedItem(BaseModel):
  emotion_label: str
  count: int
  total_count: int
  emotion_label_ru: str


class SentimentCountedItem(BaseModel):
  sentiment_label: str
  count: int
  total_count: int
  sentiment_label_ru: str


class CategoryCountedItem(BaseModel):
  label: str
  count: int
  total_count: int
  emotions: Dict[str, int]
  label_ru: str
  emotions_ru: Dict[str, int]


class MessageResponse(BaseModel):
  id: str
  external_id: Optional[str] = None
  created_at: datetime
  event_date: datetime
  source: str
  user_id: Optional[str] = None
  text: str
  cleaned_text: Optional[str] = None
  lang_code: Optional[str] = None
  lang_score: Optional[float] = None
  sentiment_label: Optional[str] = None
  sentiment_score: Optional[float] = None
  emotion_label: Optional[str] = None
  emotion_score: Optional[float] = None
  category_level_1: Optional[str] = None
  category_level_2: Optional[List[str]] = None
  sentiment_label_ru: Optional[str] = None
  emotion_label_ru: Optional[str] = None
  category_level_1_ru: Optional[str] = None
  category_level_2_ru: Optional[List[str]] = None
