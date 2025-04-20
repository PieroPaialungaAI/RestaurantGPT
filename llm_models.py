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
# list of first names from your NAMES constant
# assume NAMES = [ ... ] is defined in constants.py
import logging

# Set up logging



def log(msg):
    logging.info(msg)

class Table:
    def __init__(self, id, capacity=1):
        self.id = id
        self.capacity = capacity
        self.is_free = True
        self.cust_id = None
        self.orders = []            # list of (plate, cook_time, eat_time)
        self.current_phase = None   # "cooking" or "eating"
        self.cooking_complete_at = None
        self.leave_at = None

    def seat(self, cust_id, cust_name, clock, orders):
        self.is_free = False
        self.cust_id = cust_id
        self.orders = list(orders)  # copy the list of tuples
        # start first dish cooking immediately
        plate, cook_time, eat_time = self.orders.pop(0)
        self.current_phase = "cooking"
        self._scheduled_eat_time = eat_time
        self._remaining_orders = self.orders  # save the tail
        self.cooking_complete_at = clock + cook_time
        self.leave_at = None
        msg = (f"[{clock:04}m] 🪑 Seated {cust_name} (#{cust_id}) at T{self.id} "
               f"ordering {len(orders)} dishes; first: {plate!r} "
               f"(cook {cook_time}m, eat {eat_time}m)")
        print(msg); sys.stdout.flush()
        

    def start_eating(self, clock):
        self.current_phase = "eating"
        self.leave_at = clock + self._scheduled_eat_time
        plate = self.plate if hasattr(self, 'plate') else "dish"
        msg = (f"[{clock:04}m] 🍽️ {plate!r} ready for {self.cust_name} "
               f"(#{self.cust_id}) at T{self.id}, eating until {self.leave_at}m")
        print(msg); sys.stdout.flush()

    def finish_phase(self, clock):
        """Called when eating of current dish finishes."""
        if self._remaining_orders:
            # move to next dish
            plate, cook_time, eat_time = self._remaining_orders.pop(0)
            self.current_phase = "cooking"
            self._scheduled_eat_time = eat_time
            self.cooking_complete_at = clock + cook_time
            self.leave_at = None
            self.plate = plate
            msg = (f"[{clock:04}m] 🔄 Next dish for {self.cust_name} (#{self.cust_id}) "
                   f"at T{self.id}: {plate!r} (cook {cook_time}m, eat {eat_time}m)")
            print(msg); sys.stdout.flush()
        else:
            # no more dishes: depart
            msg = (f"[{clock:04}m] 💸 {self.cust_name} (#{self.cust_id}) "
                   f"finished all dishes and left T{self.id}")
            print(msg); sys.stdout.flush()
            self.is_free = True
            self.cust_id = None
            self.orders = []
            self.current_phase = None
            self.cooking_complete_at = None
            self.leave_at = None

class Restaurant:
    def __init__(self, num_tables, arrival_prob=0.33,
                 tick_length=1, real_pause=0.5, menu=None,
                 query_prob=0.0):
        self.tables = [Table(i) for i in range(num_tables)]
        self.queue = []                 # just customer IDs
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
        self.runner = Runner()
        self.query_prob = query_prob
        self.names = {}
        self.load_logging()

    def load_logging(self):
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s',
                            datefmt='%H:%M:%S', handlers=[
        logging.FileHandler("restaurant_log.txt", mode='w'),
        logging.StreamHandler(sys.stdout)])


    def log_to_msg(self,msg):
        logging.info(msg)
    



    def open_tables(self):
        return [t for t in self.tables if t.is_free]

    def _pick_orders(self, cname):
        """Choose between 1–3 random menu items as a list."""
        #n = random.randint(1, 3)
        #return random.sample(self.menu, n)
        customer_text = call_agent(runner = self.runner, msg= '', class_agent="customer").final_output
        msg = f'The customer {cname} is talking to the waiter, saying this {customer_text}'
        print(msg)
        self.log_to_msg(msg)
        menu_asker_output = call_agent(runner = self.runner, msg = json.dumps(customer_text), class_agent="waiter").final_output
        output = extract_json_dict(menu_asker_output)
        msg = f'The processed response from our LLM is {output}'
        print(msg)
        self.log_to_msg(msg)
        if output['status'] == 'successfull':
            return filter_menu_items(output['food'])
        else:
            n = random.randint(1, 3)
            return random.sample(self.menu, n)



    def _assign_name(self, cid):
        name = random.choice(NAMES)
        self.names[cid] = name
        return name

    def arrive(self):
        if random.random() < self.arrival_prob:
            cid = self.next_cust_id
            self.next_cust_id += 1
            cname = self._assign_name(cid)
            free = self.open_tables()
            if free:
                orders = self._pick_orders(cname)
                table = min(free, key=lambda t: t.capacity)
                table.cust_name = cname
                plate, cook_time, eat_time = orders[0]
                table.plate = plate
                table.seat(cid, cname, self.clock, orders)
            else:
                self.queue.append(cid)
                msg = f"[{self.clock:04}m] ⏳ Queued {cname} (#{cid}) – waiting"
                print(msg)
                self.log_to_msg(msg)

    def process_cooking(self):
        for t in self.tables:
            if (not t.is_free and
                t.current_phase=="cooking" and
                t.cooking_complete_at <= self.clock):
                # cooking done → start eating
                t.cust_name = self.names[t.cust_id]
                t.start_eating(self.clock)

    def process_departures(self):
        for t in self.tables:
            if (not t.is_free and
                t.current_phase=="eating" and
                t.leave_at <= self.clock):
                t.cust_name = self.names[t.cust_id]
                t.finish_phase(self.clock)

    def seat_from_queue(self):
        while self.queue and self.open_tables():
            cid = self.queue.pop(0)
            cname = self.names[cid]
            orders = self._pick_orders(cname=cname)
            table = min(self.open_tables(), key=lambda t: t.capacity)
            table.cust_name = cname
            plate, cook_time, eat_time = orders[0]
            table.plate = plate
            table.seat(cid, cname, self.clock, orders)

    def estimate_queue_time(self, cid):
        # same logic as before: position in queue × avg service
        avg = sum(c+e for _,c,e in self.menu) / len(self.menu)
        idx = self.queue.index(cid)
        return math.ceil((idx+1)*avg/len(self.tables))

    def estimate_food_time(self, cid):
        for t in self.tables:
            if t.cust_id == cid:
                # if they’re still cooking, time until cook‐done
                if t.current_phase == "cooking":
                    return max(0, t.cooking_complete_at - self.clock)
                # if they’re eating, time until they finish eating
                if t.current_phase == "eating":
                    return max(0, t.leave_at - self.clock)
        return None

    def handle_random_query(self):
        queue_ids = list(self.queue)
        seated_ids = [t.cust_id for t in self.tables if not t.is_free]
        if queue_ids and (not seated_ids or random.random() < 0.7):
            cid = random.choice(queue_ids)
            wait = self.estimate_queue_time(cid)
            cname = self.names[cid]
            msg = f"[{self.clock:04}m] ❓ Customer {cid}: How long will I be in line?"
            print(msg)
            self.log_to_msg(msg)

            msg = f"[{self.clock:04}m] ➡️ Estimated wait for customer {cid}: {wait}m"
            print(msg)
            self.log_to_msg(msg)
            waiting_message = {
                "customer_id":   cid,
                "customer_name": cname,
                "type":          "line",
                "wait_min":      wait,
                "next_food": None
            }
            output_llm = call_agent(class_agent="entertainer", runner = self.runner, msg = json.dumps(waiting_message))
            msg = f"Our LLM took care of {cname} with this: {output_llm}"
            print(msg)
            self.log_to_msg(msg)
            
        elif seated_ids:
            cid = random.choice(seated_ids)
            wait = self.estimate_food_time(cid)
            table = next(t for t in self.tables if t.cust_id == cid)
            food  = table.plate
            cname = self.names[cid]
            msg = f"[{self.clock:04}m] ❓ Customer {cid}: How long will the food take me?"
            print(msg)
            self.log_to_msg(msg)
            if wait is None:
                msg = f"[{self.clock:04}m] ➡️ Ready now!"
                print(msg)
                self.log_to_msg(msg)
            else:
                msg = f"[{self.clock:04}m] ➡️ Estimated food wait for customer {cid}: {wait}m"
                print(msg)
                self.log_to_msg(msg)
            waiting_message = {
                "customer_id":   cid,
                "customer_name": cname,
                "type":          "line",
                "wait_min":      wait,
                "next_food": food
            }
            output_llm = call_agent(class_agent="entertainer", runner = self.runner, msg = json.dumps(waiting_message))
            msg = f"Our LLM took care of {cname} with this: {output_llm}"
            print(msg)
            self.log_to_msg(msg)





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
        free = sum(t.is_free for t in self.tables)
        msg = f"\n--- END OF SHIFT ---\n{free}/{len(self.tables)} tables free at {self.clock}m."
        print(msg)
        self.log_to_msg(msg)

if __name__ == "__main__":

    
    random.seed(42)
    menu = preprocess_menu(MENU_FILE, eat_time_factor=0.5)
    R = Restaurant(
        num_tables=5,
        arrival_prob=0.7,
        tick_length=1,
        real_pause=5.0,
        query_prob=0.8,
        menu=menu
    )
    R.run(total_time=60)
