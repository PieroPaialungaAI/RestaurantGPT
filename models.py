from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Literal, List

class MenuItem(BaseModel):
    id: int
    category: str
    name: str
    description: str    # ← corrected spelling
    prep_time: int 
    price: float 

MENU: List[MenuItem] = []


class OrderItem(BaseModel):
    table_id: int
    cust_id:   int             # ← new field
    item_id:   int
    category:  str
    placed_at: int
    ready_at:  int
    served_at: Optional[int] = None


class Table(BaseModel):
    id: int
    capacity: int
    status: Literal["open", "occupied"] = "open"
    occupied_by: Optional[int] = None
    leave_at: Optional[int] = None


class RestaurantState(BaseModel):
    clock:      int = 0
    tables:     List[Table]
    queue:      List[int]          = []
    log:        List[str]          = []
    menu:       List[MenuItem]     = MENU   # loaded at startup
    order_items:List[OrderItem]    = []     # all items ordered
    revenue:    float              = 0.0


    def open_tables(self, party: int) -> List[Table]:
        return [t for t in self.tables if t.status=="open" and t.capacity>=party]

    @property
    def pending_orders(self) -> List[OrderItem]:
        return [o for o in self.orders if o.ready_at is None]

    @property
    def served_orders(self) -> List[OrderItem]:
        return [o for o in self.orders if o.served_at is not None]

    def record_revenue(self, order: OrderItem) -> None:
        # look up price per item in menu
        prices = {item.id: item.price for item in self.menu}
        self.revenue += sum(prices[i] for i in order.item_ids)
        self.log.append(f"[{self.clock:05}s] 💲 Recorded sale ${sum(prices[i] for i in order.item_ids):.2f}")
    


