from typing import Dict, List

from pydantic import BaseModel


class OrdersList(BaseModel):
    total_items: int
    total_amount: int
    products: List[Dict]
