from agents import function_tool
from constants import *
import pandas as pd 

@function_tool
def get_menu():
    df = pd.read_csv(MENU_FILE)
    # convert to list of dicts (or JSON-serializable structure)
    return df.to_dict(orient="records")
