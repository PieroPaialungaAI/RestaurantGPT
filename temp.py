# sim.py
import time, random, json
from models import RestaurantState, Table
import tools
from custom_agents import HOST
from agents import Runner    # orchestrator
from utils import *
from constants import * 


# 1) initialise the shared state
tools.STATE = RestaurantState(tables=[Table(id=i, capacity=2) for i in range(3)])
next_cust = 1
load_menu_from_csv(MENU_FILE)
print(MENU)