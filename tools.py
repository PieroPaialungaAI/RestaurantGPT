import random, asyncio, time
from models import RestaurantState, Table

STATE: RestaurantState | None = None      # set by sim.py

def seat_customer(party_size: int, cust_id: int) -> str:
    global STATE
    free = STATE.open_tables(party_size)
    if free:
        table = min(free, key=lambda t: t.capacity)    # tightest fit
        table.status, table.occupied_by = "occupied", cust_id
        table.leave_at = STATE.clock + random.randint(600, 1200)  # 10‑20 min
        msg = f"🪑 Seated customer {cust_id} at T{table.id}"
    else:
        STATE.queue.append(cust_id)
        msg = f"⏳ Queued customer {cust_id}"
    print(msg)
    STATE.log.append(f"[{STATE.clock:05}s] {msg}")
    return msg

def release_tables():
    """Called by the sim loop every tick."""
    global STATE
    for t in STATE.tables:
        if t.status == "occupied" and STATE.clock >= t.leave_at:
            STATE.log.append(f"[{STATE.clock:05}s] 💸 Customer {t.occupied_by} left T{t.id}")
            t.status, t.occupied_by, t.leave_at = "open", None, None
    # try to seat queued patrons
    still_waiting = STATE.queue[:]
    STATE.queue.clear()
    for cust in still_waiting:
        seat_customer(1, cust)            # party size = 1 for now


seat_schema = {
    "name": "seat_customer",
    "description": "Assign a customer to a table or put them in the queue.",
    "parameters": {
        "type": "object",
        "properties": {
            "party_size": {"type": "integer"},
            "cust_id": {"type": "integer"}
        },
        "required": ["party_size", "cust_id"]
    }
}
