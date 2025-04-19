# agents.py
import os, json
from agents import Agent, Runner, function_tool
import os, json
from tools import *


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


ORDER_AGENT = Agent(
    name="Order Bot",
    model="gpt-4o-mini",
    instructions=(
        "You are the server taking orders. I will give you JSON like:\n"
        "  {\"event\":\"ORDER\",\"table_id\":X,\"preferences\":\"…\"}\n"
        "You have two tools:\n"
        "  1) get_menu() → returns the menu\n"
        "  2) place_order(table_id, item_ids)\n"
        "If the user gave me preferences, call get_menu(), pick item IDs "
        "based on those preferences, then call place_order().\n"
        "If they already list item IDs, call place_order() directly.\n"
        "Return *only* the output of the place_order tool call."
    ),
    tools=[get_menu, place_order],
)
