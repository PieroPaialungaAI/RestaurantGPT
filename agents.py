from openai import OpenAI
from tools import seat_customer, seat_schema   # same Python fn + JSON schema
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HOST = client.beta.assistants.create(
    name="Host Bot",
    model="gpt-4o-mini",
    instructions=(
        "You are a restaurant host. When you receive a JSON message that "
        "includes 'event':'ARRIVAL', you MUST call the function "
        "`seat_customer` with the provided party_size and cust_id. "
    ),
    tools=[{"type": "function", "function": seat_schema}],
)


HOST_ID = HOST.id        # keep for re‑use