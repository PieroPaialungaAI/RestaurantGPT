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
        msg = (f"[{clock:04}m] 🪑 Seated customer {cust_id} at T{self.id} "
               f"ordering {plate!r} (cook {cook_time}m, eat {eat_time}m)")
        print(msg); sys.stdout.flush()

    def start_eating(self, clock):
        self.leave_at = clock + self._scheduled_eat_time
        msg = (f"[{clock:04}m] 🍽️ Customer {self.cust_id} at T{self.id} "
               f"starts eating their {self.plate!r} (leaves at {self.leave_at}m)")
        print(msg); sys.stdout.flush()

    def depart(self, clock):
        msg = (f"[{clock:04}m] 💸 Customer {self.cust_id} finished their "
               f"{self.plate!r} and left T{self.id}")
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
        self.queue = []  # items are tuples: (cust_id, plate, cook_time, eat_time)
        self.clock = 0
        self.next_cust_id = 1
        self.arrival_prob = arrival_prob
        self.tick = tick_length
        self.pause = real_pause

        # menu: list of (name, cook_time, eat_time)
        self.menu = menu or [
            ("Burger", 2, 4),
            ("Pasta", 3, 5),
            ("Salad", 1, 2),
            ("Steak", 4, 6),
            ("Soup", 1, 3),
        ]

        # probability each tick to trigger a customer query
        self.query_prob = query_prob

        # precompute average service time (cook + eat)
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
            plate, cook_time, eat_time = self._pick_dish()
            if free:
                table = min(free, key=lambda t: t.capacity)
                table.seat(cid, self.clock, plate, cook_time, eat_time)
                
                
            else:
                self.queue.append((cid, plate, cook_time, eat_time))
                msg = (f"[{self.clock:04}m] ⏳ Queued customer {cid} "
                       f"waiting for {plate!r}")
                print(msg); sys.stdout.flush()

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
            cid, plate, cook_time, eat_time = self.queue.pop(0)
            table = min(self.open_tables(), key=lambda t: t.capacity)
            table.seat(cid, self.clock, plate, cook_time, eat_time)

    def estimate_queue_time(self, cid):
        # position in queue
        positions = [item[0] for item in self.queue]
        idx = positions.index(cid)
        # compute when each table will next free up
        free_times = []
        for t in self.tables:
            if t.is_free:
                free_times.append(0)
            else:
                if t.leave_at is not None:
                    free_times.append(max(0, t.leave_at - self.clock))
                else:
                    cook_left = max(0, t.cooking_complete_at - self.clock)
                    eat_time = t._scheduled_eat_time
                    free_times.append(cook_left + eat_time)
        free_times.sort()
        # your wait is when the idx-th table frees
        return free_times[idx] if idx < len(free_times) else sum(free_times)

    def estimate_food_time(self, cid):
        for t in self.tables:
            if not t.is_free and t.cust_id == cid:
                # still cooking?
                if t.cooking_complete_at and t.cooking_complete_at > self.clock:
                    return t.cooking_complete_at - self.clock
                # already eating?
                if t.leave_at:
                    return max(0, t.leave_at - self.clock)
        return None

    def handle_random_query(self):
        # build lists of queue and seated customers
        queue_ids = [cid for cid, *_ in self.queue]
        seated_ids = [t.cust_id for t in self.tables if not t.is_free]
        # decide query type
        if queue_ids and (not seated_ids or random.random() < 0.7):
            cid = random.choice(queue_ids)
            wait = self.estimate_queue_time(cid)
            print(f"[{self.clock:04}m] ❓ Customer {cid}: How long will I be in line?")
            print(f"[{self.clock:04}m] ➡️ Estimated wait for customer {cid}: {wait}m")
        elif seated_ids:
            cid = random.choice(seated_ids)
            wait = self.estimate_food_time(cid)
            print(f"[{self.clock:04}m] ❓ Customer {cid}: How long will the food take me?")
            if wait is None:
                print(f"[{self.clock:04}m] ➡️ Your order is ready—enjoy!")
            else:
                print(f"[{self.clock:04}m] ➡️ Estimated food wait for customer {cid}: {wait}m")

    def tick_once(self):
        self.arrive()
        self.process_cooking()
        self.process_departures()
        self.seat_from_queue()

        # random customer query
        if self.query_prob > 0 and random.random() < self.query_prob:
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

    # A “data pipeline” menu with big latencies


    # real “slow” menu: cook + eat times tuned for 20–30 s per customer
    menu = preprocess_menu(MENU_FILE, eat_time_factor=0.5)

    R = Restaurant(
        num_tables=2,
        arrival_prob=0.7,
        tick_length=1,      # 1 simulated minute per loop
        real_pause=5.0,     # 5 s real per loop
        query_prob=0.4,     # always ask wait times
        menu=menu
    )

    R.run(total_time=60)  # run 60 simulated minutes (~5 real minutes)