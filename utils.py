import pandas as pd
from models import *

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