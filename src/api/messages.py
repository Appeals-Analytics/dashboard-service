from typing import Optional, List
from datetime import datetime

from api.base import BaseApiClient
from schemas import (
  MessagesFilterParams,
  MessageResponse,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
  SentimentEnum,
  EmotionEnum,
)


class MessagesApi(BaseApiClient):

  def get_messages(
    self,
    start_time: datetime,
    end_time: datetime,
    level1: Optional[str] = None,
    level2: Optional[str] = None,
    search: Optional[str] = None,
    sentiment: Optional[List[str]] = None,
    emotion: Optional[List[str]] = None,
    limit: int = 1000,
  ) -> List[MessageResponse]:
    query = MessagesFilterParams(
      start_date=start_time,
      end_date=end_time,
      limit=limit,
      category_level_1=CategoryLevel1Enum(level1) if level1 else None,
      search=search,
      sentiment_label=[SentimentEnum(s) for s in sentiment] if sentiment else None,
      emotion_label=[EmotionEnum(e) for e in emotion] if emotion else None,
    )

    if level2 and isinstance(level2, str):
      query.category_level_2 = CategoryLevel2Enum(level2)

    params = query.model_dump(mode="json", exclude_none=True)
    data = self._get("/messages/", params)
    return [MessageResponse(**item) for item in data]
