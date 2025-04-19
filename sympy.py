import asyncio, random
from models import RestaurantState, Table
from tools import STATE, seat_customer, release_tables
from agents import HOST
import openai, json

# --- build initial state -------------------------------------------------
tables = [Table(id=i, capacity=2) for i in range(3)]      # 3 small tables
STATE = RestaurantState(tables=tables)

async def call_host(arrival):
    """Send arrival message ➜ let Assistant pick function call."""
    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=json.dumps({"event": "ARRIVAL", **arrival})
    )
    
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=HOST.id
    )

    # wait until LLM responds (few hundred ms)
    while run.status not in ("completed", "failed"):
        await asyncio.sleep(0.2)
        run = openai.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
    if run.status == "failed":
        STATE.log.append(f"[{STATE.clock:05}s] ⚠️ Host failed.")
        return

    # get tool call (if any)
    msgs = openai.beta.threads.messages.list(thread_id=thread.id)
    for m in msgs.data[::-1]:
        if m.role == "assistant" and m.content[0].type == "tool_call":
            args = json.loads(m.content[0].arguments)
            seat_customer(**args)
            break

async def simulation():
    next_customer_id = 1
    while STATE.clock < 3600:   # 1‑hour demo
        # 1. customer arrival with p=0.33 each minute
        if random.random() < 0.33:
            await call_host({"party_size": 1, "cust_id": next_customer_id})
            next_customer_id += 1

        # 2. tables finish / queue gets reseated
        release_tables()

        # 3. advance time
        STATE.clock += 60      # 60‑second tick
        await asyncio.sleep(0.05)

    print("--- END OF SHIFT ---")
    for line in STATE.log:
        print(line)
    open_tables = sum(t.status == "open" for t in STATE.tables)
    print(f"{open_tables} / {len(STATE.tables)} tables free.")

asyncio.run(simulation())
