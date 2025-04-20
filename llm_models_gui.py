import tkinter as tk
import threading
import time
import random 
from llm_models import Restaurant
import random
import time
import math
import sys
from utils import *
from constants import *
import time, random, json
from custom_agents import *
from utils import *
from constants import * 
from agents import Runner

class RestaurantGUI:
    def __init__(self, restaurant):
        self.restaurant = restaurant
        self.root = tk.Tk()
        self.root.title("Restaurant Simulation")

        # Top: clock
        self.clock_label = tk.Label(self.root, text="Time: 0m", font=("Helvetica", 16))
        self.clock_label.pack(pady=10)

        # Middle: frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=10)

        # Left: table status
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=20)

        self.table_labels = []
        for table in self.restaurant.tables:
            lbl = tk.Label(self.left_frame, text=f"Table {table.id}: Free", width=30, anchor="w", font=("Helvetica", 12))
            lbl.pack(pady=2)
            self.table_labels.append(lbl)

        # Right: event log
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, padx=20)

        self.text_area = tk.Text(self.right_frame, width=80, height=30, font=("Courier", 10))
        self.text_area.pack()

        # Start simulation in separate thread
        self.simulation_thread = threading.Thread(target=self.run_simulation)
        self.simulation_thread.start()

        # Start GUI update loop
        self.update_gui()
        self.root.mainloop()

    def update_gui(self):
        # Update clock
        self.clock_label.config(text=f"Time: {self.restaurant.clock}m")

        # Update tables
        for i, table in enumerate(self.restaurant.tables):
            if table.is_free:
                text = f"Table {table.id}: Free"
                color = "green"
            else:
                text = f"Table {table.id}: Occupied by {table.cust_name} (#{table.cust_id})"
                color = "red"
            self.table_labels[i].config(text=text, fg=color)

        # Update event log
        try:
            with open("restaurant_log.txt", "r") as f:
                lines = f.readlines()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, "".join(lines[-30:]))  # last 30 events
                self.text_area.see(tk.END)  # auto-scroll
        except FileNotFoundError:
            pass

        self.root.after(1000, self.update_gui)  # update every second

    def run_simulation(self):
        import asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())  # << ADD THIS LINE
        self.restaurant.run(total_time=60)


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
