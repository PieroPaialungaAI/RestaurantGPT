# sim.py
import time, random, json
from custom_agents import *
from utils import *
from constants import * 
from agents import Runner

print(customer_agent)
runner = Runner()
customer_output = call_agent(runner = runner, msg= '', class_agent="customer").final_output
print(customer_output)
menu_asker_output = call_agent(runner = runner, msg = json.dumps(customer_output), class_agent="waiter").final_output
print(extract_json_dict(menu_asker_output))

# 1) initialise the shared state
