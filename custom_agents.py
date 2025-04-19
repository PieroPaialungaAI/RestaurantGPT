# agents.py
import os, json
from agents import Agent, Runner, function_tool
import os, json
from tools import RestaurantState, Table, release_tables
from tools import seat_customer


HOST = Agent(
    name="Host Bot",
    instructions=(
        "You are a restaurant host. I will send you a JSON string like "
        "'{\"event\":\"ARRIVAL\",\"party_size\":X,\"cust_id\":Y}'. "
        "You must call the Python function `seat_customer(party_size, cust_id)` "
        "and return its result as your final output—no other replies."
    ),
    tools=[seat_customer],       # SDK auto‑generates the schema from your function signature
    model ="gpt-4o-mini",
)
