import openai, os, json
from tools import seat_customer

openai.api_key = os.getenv("OPENAI_API_KEY")

seat_schema = {
    "name": "seat_customer",
    "description": "Assign a customer to a table or put them in the queue.",
    "parameters": {
        "type": "object",
        "properties": {
            "party_size": {"type": "integer"},
            "cust_id": {"type": "integer"}
        },
        "required": ["party_size", "cust_id"]
    }
}

HOST = openai.beta.assistants.create(
    name="Host Bot",
    model="gpt-4o-mini",
    system_prompt=(
        "You are a restaurant host. Whenever you get an 'ARRIVAL' event "
        "with a party_size and cust_id, decide whether to call "
        "`seat_customer`. No other actions."
    ),
    tools=[seat_schema],
)
