from llm_models import * 
import random


if __name__ == "__main__":
    random.seed(42)
    menu = preprocess_menu(MENU_FILE, eat_time_factor=0.5)
    R = Restaurant(
        num_tables=5,
        arrival_prob=0.7,
        tick_length=1,
        real_pause=5.0,
        query_prob=0.4,
        menu=menu
    )
    R.run(total_time=60)

