from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Literal

class Table(BaseModel):
    id: int
    capacity: int
    status: Literal["open", "occupied"] = "open"
    occupied_by: Optional[int] = None
    leave_at: Optional[int] = None


class RestaurantState(BaseModel):
    clock: int = 0
    tables: list[Table]
    queue: list[int] = []
    log: list[str] = []

    def open_tables(self, party: int) -> list[Table]:
        return [t for t in self.tables
                if t.status == "open" and t.capacity >= party]
