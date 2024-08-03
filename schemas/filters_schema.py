from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class FilterDates(BaseModel):
    """FilterDates Model"""
    init_date: Optional[datetime] = Query(None)
    end_date: Optional[datetime] = Query(None)
