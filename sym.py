import asyncio, random, json, os, tools
from agents import client, HOST_ID
from models import RestaurantState, Table
from tools import seat_customer, release_tables

# ---------- init ----------
tools.STATE = RestaurantState(tables=[Table(id=i, capacity=2) for i in range(3)])

async def host(arrival: dict):
    th = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=th.id, role="user",
        content=json.dumps({"event": "ARRIVAL", **arrival})
    )
    run = client.beta.threads.runs.create(thread_id=th.id, assistant_id=HOST_ID)
    while run.status not in ("completed", "failed"):
        await asyncio.sleep(.2)
        run = client.beta.threads.runs.retrieve(thread_id=th.id, run_id=run.id)
    
    msgs = client.beta.threads.messages.list(thread_id=th.id).data[::-1]
    print("→ Assistant raw reply:", msgs[0].content[0].dict())           # debug
    print(msgs)
    for m in msgs:
        if m.role == "assistant":
            node = m.content[0]
            print(node.type)
            if node.type == "tool":                         # real tool call
                args = json.loads(node.arguments)
                seat_customer(**args)
                break
            # if node.type == "text":                        # fallback: JSON echo
            #     try:
            #         data = json.loads(node.text.value)
            #         if data.get("event") == "ARRIVAL":
            #             seat_customer(party_size=data["party_size"],
            #                         cust_id=data["cust_id"])
            #     except json.JSONDecodeError:
            #         pass

async def sim():
    cust_id = 1
    for _ in range(10):                       # exactly 10 ticks
        await host({"party_size": 1, "cust_id": cust_id})  # force arrival
        cust_id += 1
        release_tables()
        tools.STATE.clock += 6
        await asyncio.sleep(.05)

    print("\n".join(tools.STATE.log) or "STATE.log is empty")

if __name__ == "__main__":
    asyncio.run(sim())

