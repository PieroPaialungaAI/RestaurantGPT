import pandas as pd
import math
import re
import json
from constants import * 

def load_menu_from_csv(path: str) -> None:
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        MENU.append(MenuItem(
            id=int(row["id"]),
            category=row["category"],
            name=row["name"],
            description=row["description"],
            prep_time=int(row["prep_time"]),
            price=float(row["price"]),
        ))


def preprocess_menu(path, eat_time_factor=0.5):
    df = pd.read_csv(path)
    return list(df[['name', 'prep_time', 'eat_time']].itertuples(index=False, name=None))


def filter_menu_items(food_names, eat_time_factor=0.5, path = MENU_FILE):
    """
    Given a CSV menu at `path` and a list of `food_names`, 
    returns a list of (name, prep_time, eat_time) tuples in the same format
    as preprocess_menu, preserving the order in `food_names`.
    """
    # Load and compute eat_time if not already present
    df = pd.read_csv(path)
    if 'eat_time' not in df.columns:
        df['eat_time'] = (df['prep_time'] * eat_time_factor).apply(math.ceil).clip(lower=1)
    
    # Build a lookup for quick access
    menu_dict = {
        row['name']: (row['name'], row['prep_time'], row['eat_time'])
        for _, row in df.iterrows()
    }
    
    # Assemble results in the order of food_names, skipping missing items
    result = [menu_dict[name] for name in food_names if name in menu_dict]
    return result



def extract_json_dict(raw: str):
    """
    Given a string like:
        ```json
        { "foo": 1, "bar": 2 }
        ```
    returns the Python dict { "foo": 1, "bar": 2 }.
    """
    # 1) Remove ``` fences and optional "json" tag
    #    This regex finds the first `{...}` block inside.
    m = re.search(r'\{.*\}', raw, flags=re.DOTALL)
    if not m:
        raise ValueError("No JSON object found in input")
    json_text = m.group(0)

    # 2) Parse it
    return json.loads(json_text)