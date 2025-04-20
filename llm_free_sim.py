from llm_free_models import * 
import random


if __name__ == "__main__":
    random.seed(42)                       # for reproducibility
    R = Restaurant(num_tables=3, arrival_prob=0.5, tick_length=10)
    R.run(total_time=180)  # simulate 3 hours = 180 minutes
