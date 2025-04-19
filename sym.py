# sim.py
import time, random, json
from models import RestaurantState, Table
import tools
from custom_agents import HOST
from agents import Runner    # orchestrator

# 1) initialise the shared state
tools.STATE = RestaurantState(tables=[Table(id=i, capacity=2) for i in range(3)])

# 2) main loop
next_cust = 1
while tools.STATE.clock < 3600:   # simulate one hour
    # arrival
    if random.random() < 0.33:
        arrival = json.dumps({"event":"ARRIVAL","party_size":1,"cust_id":next_cust})
        result = Runner.run_sync(HOST, arrival)
        print("💺", result.final_output)   # e.g. "🪑 Seated 1 at T0"
        next_cust += 1

    # departures + reseating
    tools.release_tables()

    # advance time & pace
    tools.STATE.clock += 60         # one-minute tick
    time.sleep(0.05)

# 3) wrap up
print("\n--- END OF SHIFT ---")
print("\n".join(tools.STATE.log))
free = sum(t.status=="open" for t in tools.STATE.tables)
print(f"{free}/{len(tools.STATE.tables)} tables free.")
