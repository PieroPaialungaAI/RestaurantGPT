from openai import OpenAI
from tools import seat_customer, seat_schema   # same Python fn + JSON schema
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HOST = client.beta.assistants.create(
    name="Host Bot",
    model="gpt-4o-mini",
    instructions=(
        "You are a restaurant host. Whenever you receive an ARRIVAL event "
        "with party_size and cust_id, call the function seat_customer. "
        "If no action is needed, say 'ACK' and do nothing."
    ),
    tools=[{"type": "function", "function": seat_schema}],
)

HOST_ID = HOST.id        # keep for re‑use