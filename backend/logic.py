from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    id: int
    name: str
    qty: int
    unit: str
    category: str
