
# RestaurantGPT 🍽️🤖

![Python Restaurant](image/Python_restaurant.png)


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

[12:31:23] The customer Emma is talking to the waiter, saying this I'd like to start with the **Bruschetta** for the appetizer. Then, I'll have the **Spaghetti Carbonara** for the first course. For dessert, I'll enjoy the **Tiramisu**. 

Could you also recommend a wine to go with this meal?
[12:31:25] The processed response from our LLM is {'food': ['Bruschetta', 'Spaghetti Carbonara', 'Tiramisu', 'Chianti Classico'], 'status': 'successful'}
[12:31:25] [0000m] ❓ Customer 1: How long will the food take me?
[12:31:25] [0000m] ➡️ Estimated food wait for customer 1: 15m
[12:31:26] Our LLM took care of Emma with this: RunResult:
- Last agent: Agent(name="Entertainer", ...)
- Final output (str):
    Hi Emma! Thank you for your patience. The wait to get in is about 15 minutes. Almost there—just enough time to start dreaming about that delicious Risotto alla Milanese! 🍽️
- 1 new item(s)
- 1 raw response(s)
- 0 input guardrail result(s)
- 0 output guardrail result(s)
(See `RunResult` for more details)
[12:31:31] The customer Liam is talking to the waiter, saying this I'd like to start with a **Bruschetta**, followed by the **Spaghetti Carbonara**. Could I also have a glass of **Chianti Classico** wine? For dessert, I'll have the **Tiramisu**. Thank you!
[12:31:33] The processed response from our LLM is {'food': ['Bruschetta', 'Spaghetti Carbonara', 'Chianti Classico', 'Tiramisu'], 'status': 'successfull'}


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
