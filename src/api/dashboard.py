from typing import Optional, List
from datetime import datetime

from api.base import BaseApiClient
from schemas import (
  DashboardFilterParams,
  CategoryFilterParams,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
  EmotionCountedItem,
  SentimentCountedItem,
  CategoryCountedItem,
  OrderEnum,
)


class DashboardApi(BaseApiClient):

  def get_emotions(
    self,
    start_time: datetime,
    end_time: datetime,
    level1: Optional[str] = None,
    level2: Optional[str] = None,
  ) -> List[EmotionCountedItem]:
    query = DashboardFilterParams(
      start_time=start_time,
      end_time=end_time,
      level1_category=CategoryLevel1Enum(level1) if level1 else None,
      level2_category=CategoryLevel2Enum(level2) if level2 else None,
    )
    params = query.model_dump(mode="json", exclude_none=True)
    data = self._get("/dashboard/emotions", params)
    return [EmotionCountedItem(**item) for item in data]

  def get_sentiments(
    self,
    start_time: datetime,
    end_time: datetime,
    level1: Optional[str] = None,
    level2: Optional[str] = None,
  ) -> List[SentimentCountedItem]:
    query = DashboardFilterParams(
      start_time=start_time,
      end_time=end_time,
      level1_category=CategoryLevel1Enum(level1) if level1 else None,
      level2_category=CategoryLevel2Enum(level2) if level2 else None,
    )
    params = query.model_dump(mode="json", exclude_none=True)
    data = self._get("/dashboard/sentiments", params)
    return [SentimentCountedItem(**item) for item in data]

  def get_categories_l1(self, start_time: datetime, end_time: datetime) -> List[CategoryCountedItem]:
    query = CategoryFilterParams(start_time=start_time, end_time=end_time, order_by=OrderEnum.DESC)
    params = query.model_dump(mode="json", exclude_none=True)
    data = self._get("/dashboard/categories/level-1", params)
    return [CategoryCountedItem(**item) for item in data]

  def get_categories_l2(
    self, start_time: datetime, end_time: datetime, level1: str
  ) -> List[CategoryCountedItem]:
    query = CategoryFilterParams(
      start_time=start_time,
      end_time=end_time,
      level1_category=CategoryLevel1Enum(level1),
      order_by=OrderEnum.DESC,
    )
    params = query.model_dump(mode="json", exclude_none=True)
    data = self._get("/dashboard/categories/level-2", params)
    return [CategoryCountedItem(**item) for item in data]
