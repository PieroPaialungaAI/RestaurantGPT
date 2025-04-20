# sim.py
import time, random, json

from models import RestaurantState, Table
import tools
from custom_agents import *
from agents import Runner
from utils import load_menu_from_csv
from constants import MENU_FILE

def main():
    # 0) load menu
    load_menu_from_csv(MENU_FILE)

    # 1) init state
    tools.STATE = RestaurantState(
        tables=[Table(id=i, capacity=2) for i in range(3)],
        menu=tools.MENU
    )

    runner = Runner()
    next_cust = 0

    # 2) simulate one hour
    while tools.STATE.clock < 3600:

        if random.random() < 0.33:
            cust = next_cust; next_cust += 1
            if tools.STATE.open_tables(1):
                arrival = {"event":"ARRIVAL","party_size":1,"cust_id":next_cust}
                res = runner.run_sync(HOST, json.dumps(arrival))
                print("💺", res.final_output)
            else:
                tools.STATE.queue.append(cust)
                print(f"⏳ Queued customer {cust}")

        # 2b) take orders on any newly seated tables
        for t in tools.STATE.tables:
            # has this table already placed *any* orders?
            already_ordered = any(oi.table_id == t.id and oi.cust_id == t.occupied_by for oi in tools.STATE.order_items)
            if t.status == "occupied" and not already_ordered:
                order_event = {
                    "event":       "ORDER",
                    "table_id":    t.id,
                    "preferences": "I’d like something light and vegetarian"
                }
                ores = runner.run_sync(ORDER_AGENT, json.dumps(order_event))
                print("🍽️", ores.final_output)
        tools.cook_and_serve()
        tools.release_tables()
        tools.seat_from_queue()  
        tools.STATE.clock += 60 
        time.sleep(0.5)

    # 3) summary
    print("\n--- END OF SHIFT ---")
    print("\n".join(tools.STATE.log))
    free = sum(t.status == "open" for t in tools.STATE.tables)
    print(f"{free}/{len(tools.STATE.tables)} tables free.")
    print(f"Total revenue: ${tools.STATE.revenue:.2f}")

if __name__ == "__main__":
    main()

