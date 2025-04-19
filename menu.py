from pydantic import BaseModel
from typing import List

class MenuItem(BaseModel):
    id: int
    name: str
    descritption: str
    prep_time: int 
    price: float 

MENU: List[MenuItem] = []