
# RestaurantGPT 🍽️🤖

**RestaurantGPT** is a live simulation of a restaurant where customers order, waiters take orders, and entertainers entertain guests — all powered by a Language Model (LLM) backend.

This project combines **Python**, **async agents**, **Tkinter GUI**, and **LLM reasoning** to create a dynamic restaurant environment where human-like decisions happen in real-time.

---

## ✨ Features

- **Dynamic Customer Behavior**: Customers generate natural conversation with waiters using an LLM before ordering.
- **Real-Time Event Simulation**: Cooking, eating, waiting, and customer departures happen based on real-world time.
- **Smart Query Handling**: Customers waiting in line or at the table can ask questions ("How long until my food?"), and an entertainer agent answers them.
- **Live GUI Dashboard**:
  - See which tables are free or occupied.
  - Watch customer interactions live.
  - Real-time clock and event feed.
- **Log File**: All actions are logged cleanly in `restaurant_log.txt`.

---

## 📂 Folder Structure

```
RestaurantGPT/
├── agents/             # Agent definitions (runner logic)
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
- **Arrival Rate**: Adjust `arrival_prob` in `llm_models.py`.
- **Customer Queries**: Tune `query_prob` to control how often customers ask questions.
- **Tick Length**: Modify `tick_length` to speed up or slow down the simulation.

---

## 📸 Preview

| Tables | Live Events |
|:------|:------------|
| 🟢 Table 0: Free | [00:02] 🪑 Seated Alice at Table 2 |
| 🔴 Table 1: Occupied by Bob | [00:04] 🍽️ Burger ready for Bob |
| 🟢 Table 2: Free | [00:05] 💬 Bob asks: "When will my next dish be ready?" |

---

## 🤔 Future Plans

- Animated progress bars for cooking and eating phases 🍔📊
- Pause/Resume functionality from GUI
- Different customer personalities (angry, impatient, polite)

---

## 📜 License

Released under the MIT License.

---

## 🙏 Credits

Built with ❤️ by [Piero Paialunga](https://github.com/PieroPaialungaAI).
