# restaurant_sim_agent.py

import os
import random
import time
import sys

from openai import OpenAI
from agents import Agent, Runner
from newtools import * 

# ———————— import your newtools to register the @function_tool handlers ————————
import newtools

# ———————— Set up the LLM + Agent ————————


if __name__ == "__main__":
    runner = Runner()
    R = Restaurant(num_tables=3, arrival_prob=0.5, tick_length=10, real_pause=0.2)
    R.run(total_time=180)
