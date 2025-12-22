from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from schemas.emotion_enum import EmotionEnum
from schemas.sentiment_enum import SentimentEnum
from schemas.category_level_1_enum import CategoryLevel1Enum
from schemas.category_level_2_enum import CategoryLevel2Enum
from schemas.order_enum import OrderEnum
from schemas.granularity_enum import GranularityEnum


class BaseFilterParams(BaseModel):
  start_time: datetime
  end_time: datetime


class DashboardFilterParams(BaseFilterParams):
  level1_category: Optional[CategoryLevel1Enum] = None
  level2_category: Optional[CategoryLevel2Enum] = None


class EmotionDynamicsFilterParams(DashboardFilterParams):
  granularity: GranularityEnum = GranularityEnum.DAY



class CategoryFilterParams(BaseFilterParams):
  order_by: OrderEnum = OrderEnum.DESC
  level1_category: Optional[CategoryLevel1Enum] = None


class MessagesFilterParams(BaseModel):
  start_date: datetime
  end_date: datetime
  limit: int = 1000
  category_level_1: Optional[CategoryLevel1Enum] = None
  category_level_2: Optional[List[CategoryLevel2Enum]] = None
  search: Optional[str] = None
  sentiment_label: Optional[List[SentimentEnum]] = None
  emotion_label: Optional[List[EmotionEnum]] = None
  user_id: Optional[str] = None
