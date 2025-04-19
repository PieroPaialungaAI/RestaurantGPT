# tools.py
import random
from models import *
from agents import function_tool
import os, json
from constants import * 
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
        if (
            t.status == "occupied"
            and t.leave_at is not None
            and STATE.clock >= t.leave_at
        ):
            STATE.log.append(f"[{STATE.clock:05}s] 💸 Customer {t.occupied_by} left T{t.id}")
            # clear old orders for this table
            STATE.order_items = [
                oi for oi in STATE.order_items
                if oi.table_id != t.id
            ]
            # reset the table
            t.status, t.occupied_by, t.leave_at = "open", None, None

    # 2) Seat anyone in the queue
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
    Record each requested item as an OrderItem, compute its ready_at,
    and return a summary.
    """
    msgs = []
    for iid in item_ids:
        item = next(m for m in MENU if m.id == iid)
        # immediate for wine, else prep_time from menu
        ready = STATE.clock if item.category == "Wine" else STATE.clock + item.prep_time
        oi = OrderItem(
            table_id=table_id,
            item_id=iid,
            category=item.category,
            placed_at=STATE.clock,
            ready_at=ready
        )
        STATE.order_items.append(oi)
        msgs.append(item.name)
    summary = ", ".join(msgs)
    STATE.log.append(f"[{STATE.clock:05}s] 📝 Table {table_id} ordered: {summary}")
    return f"Ordered {summary} for table {table_id}"


def cook_and_serve() -> None:
    ready = [oi for oi in STATE.order_items
             if oi.served_at is None and STATE.clock >= oi.ready_at]
    ready.sort(key=lambda oi: FOOD_PRIORITY.get(oi.category, 999))
    for oi in ready:
        oi.served_at = STATE.clock

        # assign a dining duration of 5–15 seconds (for quick demo)
        dining_time = random.randint(5, 15)
        tbl = next(t for t in STATE.tables if t.id == oi.table_id)
        tbl.leave_at = STATE.clock + dining_time

        price = next(m.price for m in STATE.menu if m.id == oi.item_id)
        STATE.revenue += price
        STATE.log.append(
          f"[{STATE.clock:05}s] 🍽️ Served {oi.category} '{oi.item_id}' "
          f"to T{oi.table_id} (+${price:.2f}); will leave at {tbl.leave_at}s"
        )

# This is the tool the Agent sees:
seat_customer = function_tool(_seat_customer_impl)