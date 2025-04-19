# tools.py
import random
from models import *
from agents import function_tool
import os, json
# singleton state (will be set by sim.py)
STATE: RestaurantState

def _seat_customer_impl(party_size: int, cust_id: int) -> str:
    free = STATE.open_tables(party_size)
    if free:
        tbl = min(free, key=lambda t: t.capacity)
        tbl.status, tbl.occupied_by = "occupied", cust_id
        tbl.leave_at = STATE.clock + random.randint(600,1200)
        msg = f"🪑 Seated {cust_id} at T{tbl.id}"
    else:
        STATE.queue.append(cust_id)
        msg = f"⏳ Queued {cust_id}"
    STATE.log.append(f"[{STATE.clock:05}s] {msg}")
    return msg



def release_tables() -> None:
    # 1) Free any tables whose customers are done
    for t in STATE.tables:
        # if table is occupied AND the leave time has passed
        if t.status == "occupied" and t.leave_at is not None \
           and STATE.clock >= t.leave_at:
            STATE.log.append(f"[{STATE.clock:05}s] 💸 Customer {t.occupied_by} left T{t.id}")
            t.status, t.occupied_by, t.leave_at = "open", None, None
    for cust in STATE.queue[:]:
        _seat_customer_impl(1, cust)
    STATE.queue.clear()

@function_tool
def get_menu() -> list[MenuItem]:
    """Return the full list of MenuItem objects."""
    return MENU

@function_tool
def place_order(table_id: int, item_ids: list[int]) -> str:
    """
    Record an order for this table.
    Returns a summary string.
    """
    STATE.orders.setdefault(table_id, [])
    # look up item names
    names = []
    for iid in item_ids:
        item = next((m for m in MENU if m.id == iid), None)
        if item:
            STATE.orders[table_id].append(item)
            names.append(item.name)
    summary = ", ".join(names) or "nothing"
    msg = f"Table {table_id} ordered: {summary}"
    STATE.log.append(f"[{STATE.clock:05}s] 📝 {msg}")
    return msg


# This is the tool the Agent sees:
seat_customer = function_tool(_seat_customer_impl)