from pydantic import BaseModel
from typing import Dict, List


class OrdersList(BaseModel):
    total_items: int
    total_amount: int
    products: List[Dict]
