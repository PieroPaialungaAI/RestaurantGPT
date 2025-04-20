# restaurant_sim_stream.py
import random
import time
import sys

class Table:
    def __init__(self, id, capacity=1):
        self.id = id
        self.capacity = capacity
        self.is_free = True
        self.cust_id = None
        self.cooking_complete_at = None
        self.leave_at = None

    def seat(self, cust_id, clock, cook_time):
        self.is_free = False
        self.cust_id = cust_id
        self.cooking_complete_at = clock + cook_time
        msg = f"[{clock:04}m] 🪑 Seated customer {cust_id} at T{self.id}"
        print(msg); sys.stdout.flush()

    def start_eating(self, clock, eat_time):
        self.leave_at = clock + eat_time
        msg = (f"[{clock:04}m] 🍽️ Customer {self.cust_id} at T{self.id} "
               f"starts eating (will leave at {self.leave_at}m)")
        print(msg); sys.stdout.flush()

    def depart(self, clock):
        msg = f"[{clock:04}m] 💸 Customer {self.cust_id} left T{self.id}"
        print(msg); sys.stdout.flush()
        self.is_free = True
        self.cust_id = None
        self.cooking_complete_at = None
        self.leave_at = None

class Restaurant:
    def __init__(self, num_tables, arrival_prob=0.33, tick_length=1, real_pause=0.5):
        self.tables = [Table(i) for i in range(num_tables)]
        self.queue = []
        self.clock = 0
        self.next_cust_id = 1
        self.arrival_prob = arrival_prob
        self.tick = tick_length
        self.pause = real_pause

    def open_tables(self):
        return [t for t in self.tables if t.is_free]

    def arrive(self):
        if random.random() < self.arrival_prob:
            cid = self.next_cust_id
            self.next_cust_id += 1
            free = self.open_tables()
            if free:
                table = min(free, key=lambda t: t.capacity)
                cook_time = random.randint(1, 3)  # fast cook for demo
                table.seat(cid, self.clock, cook_time)
            else:
                self.queue.append(cid)
                msg = f"[{self.clock:04}m] ⏳ Queued customer {cid}"
                print(msg); sys.stdout.flush()

    def process_cooking(self):
        for t in self.tables:
            if (not t.is_free
                and t.cooking_complete_at is not None
                and t.cooking_complete_at <= self.clock
                and t.leave_at is None):
                eat_time = random.randint(2, 4)  # fast eat for demo
                t.start_eating(self.clock, eat_time)

    def process_departures(self):
        for t in self.tables:
            if (not t.is_free
                and t.leave_at is not None
                and t.leave_at <= self.clock):
                t.depart(self.clock)

    def seat_from_queue(self):
        while self.queue and self.open_tables():
            cid = self.queue.pop(0)
            table = min(self.open_tables(), key=lambda t: t.capacity)
            cook_time = random.randint(1, 3)
            table.seat(cid, self.clock, cook_time)

    def tick_once(self):
        self.arrive()
        self.process_cooking()
        self.process_departures()
        self.seat_from_queue()
        self.clock += self.tick
        time.sleep(self.pause)

    def run(self, total_time):
        while self.clock < total_time:
            self.tick_once()
        print("\n--- END OF SHIFT ---")
        free = sum(t.is_free for t in self.tables)
        print(f"{free}/{len(self.tables)} tables free at {self.clock}m.")

if __name__ == "__main__":
    random.seed(0)
    R = Restaurant(num_tables=3, arrival_prob=0.6, tick_length=1, real_pause=0.5)
    R.run(total_time=30)
