# tools.py
import random
from agents import function_tool
from typing import List
from menu import MENU, MenuItem
from models import RestaurantState, OrderItem

STATE: RestaurantState  # injected by sim

@function_tool
def seat_customer(party_size: int, cust_id: int) -> str:
    """Seat or queue the arriving customer."""
    free = STATE.open_tables(party_size)
    if free:
        tbl = min(free, key=lambda t: t.capacity)
        tbl.status, tbl.occupied_by = "occupied", cust_id
        msg = f"🪑 Seated {cust_id} at T{tbl.id}"
    else:
        STATE.queue.append(cust_id)
        msg = f"⏳ Queued {cust_id}"
    STATE.log.append(f"[{STATE.clock:05}s] {msg}")
    return msg

@function_tool
def wait_message(customer_id: int, wait_time: int) -> str:
    """Generate a friendly hold‑music message for waiting customers."""
    # (Here you could call openai.ChatCompletion internally if you wanted,
    # but Agents will invoke this tool for you.)
    return f"Hi #{customer_id}, thanks for your patience! Your table’s a few minutes away—feel free to mull over our specials while you wait."

@function_tool
def get_menu() -> List[MenuItem]:
    """Return the full menu."""
    return MENU

@function_tool
def recommend_menu(preferences: str) -> List[int]:
    """Ask the LLM which item IDs to suggest given some preferences."""
    # In reality you’d call openai.ChatCompletion here; for now stub:
    # return [item.id for item in MENU if preferences.lower() in item.description.lower()]
    # But Agents will call this tool itself, so leave it as an LLM call
    raise NotImplementedError("Let the Agent pick via LLM!")

@function_tool
def place_order(table_id: int, item_ids: List[int]) -> str:
    """Record one order per item, compute ready_at, and return a summary."""
    cust = next(t.occupied_by for t in STATE.tables if t.id == table_id)
    names = []
    for iid in item_ids:
        itm = next(m for m in MENU if m.id == iid)
        ready = STATE.clock + itm.prep_time
        oi = OrderItem(
            table_id=table_id,
            cust_id=cust,
            item_id=iid,
            category=itm.category,
            placed_at=STATE.clock,
            ready_at=ready
        )
        STATE.order_items.append(oi)
        names.append(itm.name)
    summary = ", ".join(names)
    msg = f"Table {table_id} (cust {cust}) ordered: {summary}"
    STATE.log.append(f"[{STATE.clock:05}s] 📝 {msg}")
    return msg
