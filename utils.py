# menu_loader.py
import pandas as pd
from menu import MENU, MenuItem

def load_menu_from_csv(path: str) -> None:
    """
    Reads a CSV with columns:
      id,name,description,prep_time,price
    and populates the global MENU list with MenuItem instances.
    """
    df = pd.read_csv(path)
    for _, row in df.iterrows():
        MENU.append(MenuItem(
            id=int(row['id']),
            name=row['name'],
            description=row['description'],
            prep_time=int(row['prep_time']),
            price=float(row['price'])
        ))
