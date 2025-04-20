from agents import function_tool
from constants import *
import pandas as pd 

@function_tool
def check_wait_time(waiting_time, queue, food = None) -> str:
    return {'waiting_time': waiting_time, queue : queue, food : food}
    """Quiz, joke, or chat to keep a waiting customer entertained."""
    # your actual entertainment logic goes here
    

@function_tool
def get_menu():
    df = pd.read_csv(MENU_FILE)
    # convert to list of dicts (or JSON-serializable structure)
    return df.to_dict(orient="records")
