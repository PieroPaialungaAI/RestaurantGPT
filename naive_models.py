import random
import time
import math
import sys
from utils import *
from constants import *

class Table:
    def __init__(self, id, capacity=1):
        self.id = id
        self.capacity = capacity
        self.is_free = True
        self.cust_id = None
        self.plate = None
        self.cooking_complete_at = None
        self.leave_at = None

    def seat(self, cust_id, clock, plate, cook_time, eat_time):
        self.is_free = False
        self.cust_id = cust_id
        self.plate = plate
        self.cooking_complete_at = clock + cook_time
        self._scheduled_eat_time = eat_time
        msg = (
            f"[{clock:04}m] 🪑 Seated customer {cust_id} at T{self.id} "
            f"ordering {plate!r} (cook {cook_time}m, eat {eat_time}m)"
        )
        print(msg); sys.stdout.flush()

    def start_eating(self, clock):
        self.leave_at = clock + self._scheduled_eat_time
        msg = (
            f"[{clock:04}m] 🍽️ Customer {self.cust_id} at T{self.id} "
            f"starts eating their {self.plate!r} (leaves at {self.leave_at}m)"
        )
        print(msg); sys.stdout.flush()

    def depart(self, clock):
        msg = (
            f"[{clock:04}m] 💸 Customer {self.cust_id} finished their "
            f"{self.plate!r} and left T{self.id}"
        )
        print(msg); sys.stdout.flush()
        self.is_free = True
        self.cust_id = None
        self.plate = None
        self.cooking_complete_at = None
        self.leave_at = None

class Restaurant:
    def __init__(self, num_tables, arrival_prob=0.33,
                 tick_length=1, real_pause=0.5, menu=None,
                 query_prob=0.0):
        self.tables = [Table(i) for i in range(num_tables)]
        # queue holds only customer IDs
        self.queue = []
        self.clock = 0
        self.next_cust_id = 1
        self.arrival_prob = arrival_prob
        self.tick = tick_length
        self.pause = real_pause
        self.menu = menu or [
            ("Burger", 2, 4),
            ("Pasta", 3, 5),
            ("Salad", 1, 2),
            ("Steak", 4, 6),
            ("Soup", 1, 3),
        ]
        self.query_prob = query_prob

        total = sum(c + e for _, c, e in self.menu)
        self.avg_service_time = total / len(self.menu)

    def open_tables(self):
        return [t for t in self.tables if t.is_free]

    def _pick_dish(self):
        return random.choice(self.menu)

    def arrive(self):
        if random.random() < self.arrival_prob:
            cid = self.next_cust_id
            self.next_cust_id += 1
            free = self.open_tables()
            if free:
                # pick dish only when seating immediately
                plate, cook_time, eat_time = self._pick_dish()
                table = min(free, key=lambda t: t.capacity)
                table.seat(cid, self.clock, plate, cook_time, eat_time)
            else:
                self.queue.append(cid)
                print(f"[{self.clock:04}m] ⏳ Queued customer {cid} (waiting)")

    def process_cooking(self):
        for t in self.tables:
            if (not t.is_free
                and t.cooking_complete_at is not None
                and t.cooking_complete_at <= self.clock
                and t.leave_at is None):
                t.start_eating(self.clock)

    def process_departures(self):
        for t in self.tables:
            if (not t.is_free
                and t.leave_at is not None
                and t.leave_at <= self.clock):
                t.depart(self.clock)

    def seat_from_queue(self):
        while self.queue and self.open_tables():
            cid = self.queue.pop(0)
            # pick dish at seating time
            plate, cook_time, eat_time = self._pick_dish()
            table = min(self.open_tables(), key=lambda t: t.capacity)
            table.seat(cid, self.clock, plate, cook_time, eat_time)

    def estimate_queue_time(self, cid):
        positions = list(self.queue)
        idx = positions.index(cid)
        raw_wait = (idx + 1) * self.avg_service_time / len(self.tables)
        return math.ceil(raw_wait)

    def estimate_food_time(self, cid):
        for t in self.tables:
            if t.cust_id == cid:
                if t.cooking_complete_at > self.clock:
                    return t.cooking_complete_at - self.clock
                return max(0, t.leave_at - self.clock)
        return None

    def handle_random_query(self):
        queue_ids = list(self.queue)
        seated_ids = [t.cust_id for t in self.tables if not t.is_free]
        if queue_ids and (not seated_ids or random.random() < 0.7):
            cid = random.choice(queue_ids)
            wait = self.estimate_queue_time(cid)
            print(f"[{self.clock:04}m] ❓ Customer {cid}: How long will I be in line?")
            print(f"[{self.clock:04}m] ➡️ Estimated wait for customer {cid}: {wait}m")
            
        elif seated_ids:
            cid = random.choice(seated_ids)
            wait = self.estimate_food_time(cid)
            table = next(t for t in self.tables if t.cust_id == cid)
            food  = table.plate
            print(f"[{self.clock:04}m] ❓ Customer {cid}: How long will the {food} take me?")
            if wait is None:
                print(f"[{self.clock:04}m] ➡️ Ready now!")
            else:
                print(f"[{self.clock:04}m] ➡️ Estimated food wait for customer {cid}: {wait}m")

    def tick_once(self):
        self.arrive()
        self.process_cooking()
        self.process_departures()
        self.seat_from_queue()
        if self.query_prob and random.random() < self.query_prob:
            self.handle_random_query()
        self.clock += self.tick
        time.sleep(self.pause)

    def run(self, total_time):
        while self.clock < total_time:
            self.tick_once()
        print("\n--- END OF SHIFT ---")
        free = sum(t.is_free for t in self.tables)
        print(f"{free}/{len(self.tables)} tables free at {self.clock}m.")

if __name__ == "__main__":
    random.seed(42)
    menu = preprocess_menu(MENU_FILE, eat_time_factor=0.5)
    R = Restaurant(
        num_tables=2,
        arrival_prob=0.7,
        tick_length=1,
        real_pause=5.0,
        query_prob=0.4,
        menu=menu
    )
    R.run(total_time=60)