# test_assistant_tool.py
import os, json, time
from openai import OpenAI
from tools import seat_schema, seat_customer

# 1) Build the client with the v2 header
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"},
)

# 2) Create (or retrieve) your Host assistant
assistant = client.beta.assistants.create(
    name="Host Bot",
    model="gpt-4o-mini",
    instructions=(
        "You are a restaurant host. When you receive JSON with "
        "'event':'ARRIVAL', 'party_size', and 'cust_id', you MUST call "
        "the function seat_customer with those exact fields. Do not reply otherwise."
    ),
    tools=[{"type": "function", "function": seat_schema}],
)
AID = assistant.id

# 3) Kick off a thread **and** run the assistant in one shot
run = client.beta.threads.create_and_run(
    assistant_id=AID,
    thread={
        "messages": [
            {
                "role": "user",
                "content": json.dumps({"event": "ARRIVAL", "party_size": 1, "cust_id": 1})
            }
        ]
    },
)

print("▶ initial run.status:", run.status)

# 4) Poll until it finishes (v2 statuses are 'running' → 'succeeded' or 'failed')
while run.status not in ("succeeded", "failed"):
    time.sleep(0.2)
    run = client.beta.threads.runs.poll(   # convenience wrapper
        thread_id=run.thread_id,
        run_id=run.id
    )
    print("… status:", run.status)

if run.status == "failed":
    raise RuntimeError("Assistant run failed")

# 5) Fetch the thread and look for the function‑call message
thread = client.beta.threads.retrieve(thread_id=run.thread_id)
for msg in thread.messages[::-1]:
    if msg.role == "assistant" and msg.content[0].type == "tool":
        args = json.loads(msg.content[0].arguments)
        result = seat_customer(**args)
        print("✅ tool called with", args, "→", result)
        break
else:
    print("⚠️ No tool call detected")
