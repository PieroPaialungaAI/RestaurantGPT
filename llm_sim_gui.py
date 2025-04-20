from llm_models_gui import RestaurantGUI
from utils import * 
import random
from llm_models import Restaurant

if __name__ == "__main__":
    random.seed(42)
    menu = preprocess_menu(MENU_FILE, eat_time_factor=0.5)
    R = Restaurant(
        num_tables=5,
        arrival_prob=0.7,
        tick_length=1,
        real_pause=1.0,    # smoother for GUI
        query_prob=0.8,
        menu=menu
    )
    app = RestaurantGUI(R)
