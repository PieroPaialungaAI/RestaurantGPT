
# RestaurantGPT 🍽️🤖

**RestaurantGPT** is a live simulation of a restaurant, developed with OpenAI Agents, where customers order, waiters take orders, and entertainers entertain guests, all powered by a Language Model (LLM) backend.

This project combines **Python**, **Open AI agents**, **Tkinter GUI**, and **Object Oriented Programming** to create a dynamic restaurant environment where human-like decisions happen in real-time.

---

## ✨ Features
- **Queue Handling**: we have X tables, and customers will come to sit, if they can. This logic is implemented.
- **Dynamic Customer Behavior**: Customers generate natural conversation with waiters using an LLM to order or ask for suggestions.
- **Real-Time Event Simulation**: Cooking, eating, waiting, and customer departures are simulated based on how long it will take for them to eat the food they ordered.
- **Smart Query Handling**: Customers waiting in line or at the table can ask questions ("How long until my food?"), and an entertainer LLM agent answers them.
- **Live GUI Dashboard**:
  - See which tables are free or occupied.
  - Watch customer interactions live.
  - Time clock and event feed.
- **Log File**: All actions are logged cleanly in `restaurant_log.txt`.

---

## 📂 Folder Structure

```
RestaurantGPT/
├── constants.py        # Menu items, customer names, and system constants
├── custom_agents.py    # Specialized agents (customer, waiter, entertainer)
├── llm_models.py       # Core restaurant simulation logic
├── llm_models_gui.py   # GUI application logic (Tkinter)
├── utils.py            # Utility functions (menu preprocessing, JSON extraction)
├── restaurant_log.txt  # Auto-generated event log
├── README.md           # (this file)
└── requirements.txt    # Required Python libraries
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

You’ll need:
- `tk`
- `openai`
- `agents`
- `asyncio`
- `httpx`

### 2. Set up your environment

You need an OpenAI-compatible API key:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or configure it in a `.env` file.

### 3. Launch the Simulation

```bash
python llm_models_gui.py
```

✅ A live GUI window will open, showing tables, event feed, and simulation clock.

---

## 🛠️ Customization

- **Menu**: Edit `constants.py` (see `MENU_FILE`).
- **Simulation parameters**: You can adjust all the parameters of the restaurant (e.g., number of tables) and the Menu through a .csv file.
- **Customer Queries**: Tune `query_prob` to control how often customers ask questions.
- **Tick Length**: Modify `tick_length` to speed up or slow down the simulation.

---

## 📸 Preview

[10:19:41] The customer Emma is talking to the waiter, saying this Here's the menu:

### Appetizers
- **Bruschetta** - $5.00
- **Caprese Salad** - $7.00
- **Arancini** - $6.50
- **Prosciutto e Melone** - $8.00
- **Burrata** - $9.50

### First Courses
- **Spaghetti Carbonara** - $10.00
- **Fettuccine Alfredo** - $11.00
- **Lasagna** - $12.00
- **Risotto alla Milanese** - $13.50
- **Gnocchi al Pesto** - $11.50

### Second Courses
- **Pollo alla Cacciatora** - $14.00
- **Bistecca alla Fiorentina** - $25.00
- **Osso Buco** - $22.00
- **Saltimbocca alla Romana** - $18.00
- **Branzino al Forno** - $19.00

### Wines
- **Chianti Classico** - $8.00
- **Prosecco** - $7.50
- **Barolo** - $12.00
- **Nero d’Avola** - $9.00
- **Pinot Grigio** - $7.00

### Desserts
- **Tiramisu** - $6.00
- **Panna Cotta** - $5.50
- **Cannoli** - $6.50
- **Gelato al Limone** - $5.00
- **Affogato al Caffè** - $6.00

Do you know what you'd like, or would you like some recommendations based on your preferences?
[10:19:42] The processed response from our LLM is {'food': None, 'status': 'unsuccessfull'}
[10:19:42] [0000m] ❓ Customer 1: How long will the food take me?
[10:19:42] [0000m] ➡️ Estimated food wait for customer 1: 15m
[10:19:44] Our LLM took care of Emma with this: RunResult:
- Last agent: Agent(name="Entertainer", ...)
- Final output (str):
    Hi Emma! It looks like the line is about 15 minutes right now. Just enough time to imagine the delicious Risotto alla Milanese waiting for you. Hang in there, it'll be worth the wait! 🍽️😊
---

## 🤔 Future Plans

- Animated progress bars for cooking and eating phases 🍔📊
- Pause/Resume functionality from GUI
- Different customer personalities (angry, impatient, polite)
- Guardrails on LLM Agents for consistency
- Customer satisfaction Agents after lunch.

---

## 📜 License

Released under the MIT License.

---

## 🙏 Credits

Built with ❤️ by [Piero Paialunga](https://github.com/PieroPaialungaAI).