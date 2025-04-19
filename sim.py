# sim.py
import time, random, json
from models import RestaurantState, Table
import tools
from custom_agents import HOST
from agents import Runner    # orchestrator
from utils import *
from constants import * 


def main():
    # 1) initialise the shared state
    tools.STATE = RestaurantState(tables=[Table(id=i, capacity=2) for i in range(3)])
    next_cust = 1
    load_menu_from_csv(MENU_FILE)
    # 2) main loop
    while tools.STATE.clock < 3600:
        if random.random() < 0.33:
            payload = json.dumps({"event":"ARRIVAL","party_size":1,"cust_id":next_cust})
            res = Runner.run_sync(HOST, payload)
            print("💺", res.final_output)
            next_cust += 1

        tools.release_tables()
        tools.STATE.clock += 60
        time.sleep(0.05)

    # 3) wrap up
    print("\n--- END OF SHIFT ---")
    print("\n".join(tools.STATE.log))
    free = sum(t.status == "open" for t in tools.STATE.tables)
    print(f"{free}/{len(tools.STATE.tables)} tables free.")

if __name__ == "__main__":
    main()
