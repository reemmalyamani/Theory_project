# NFA to DFA Converter (CSC339)

A desktop tool that converts an NFA (with optional ε/λ-transitions) into an equivalent DFA using the **subset construction** algorithm. It shows the DFA states, its transition table, and a Graphviz diagram.

## Files

| File | Purpose |
|------|---------|
| `main_app.py` | **Start here.** Input window + "Convert to DFA" button that connects everything |
| `nfa_gui.py` | NFA input form and input parsing |
| `nfa_input.py` | `NFA` class with validation |
| `subset_construction.py` | Subset construction algorithm and `DFA` class |
| `dfa_output.py` | DFA output window (states, table, Graphviz diagram) |
| `test_cases.py` | Automated tests (three NFA test cases) |
| `requirements.txt` | Python packages needed |

## Requirements

- **Python 3.8 or newer** (with Tkinter)
- Python packages: `graphviz`, `pillow`
- The **Graphviz program** itself (the `dot` command). The Python `graphviz` package only calls it; it does not include it.

## Installation

### 1. Install Python and Tkinter

- **Windows / macOS:** install Python from <https://www.python.org/downloads/>. Tkinter is included.
- **Linux (Debian/Ubuntu):** `sudo apt install python3 python3-tk`

### 2. Install the Graphviz program

- **Windows:** download the installer from <https://graphviz.org/download/>. During installation choose **"Add Graphviz to the system PATH"**, then restart your terminal.
- **macOS:** `brew install graphviz`
- **Linux (Debian/Ubuntu):** `sudo apt install graphviz`

Check that it works:

```
dot -V
```

### 3. Install the Python packages

Open a terminal in the project folder and run:

```
pip install -r requirements.txt
```

(or `pip install graphviz pillow`)

## Running the project

Put all the `.py` files in the same folder, then:

```
python main_app.py
```

(On macOS/Linux you may need `python3` instead of `python`.)

### How to use

1. Fill in the fields:
   - **States:** `q0,q1,q2`
   - **Alphabet:** `0,1` (single characters; do **not** include ε or λ)
   - **Initial state:** `q0`
   - **Accepting states:** `q2`
   - **Transitions**, one per line, in the form `source,symbol:destination1,destination2`
2. Click **Convert to DFA**. (The *Save NFA* button only validates and stores the NFA; converting does not require it.)
3. The DFA window opens with the state list, transition table and diagram. Use **Save graph (PNG + DOT)** to export the diagram into the project folder.

Rules for transitions: use `ε` or `λ` for epsilon moves, leave the destinations empty for ∅, and write each `(state, symbol)` pair on only one line (combine the destinations).

### Example (strings ending in `01`)

```
States:           q0,q1,q2
Alphabet:         0,1
Initial state:    q0
Accepting states: q2

q0,0:q0,q1
q0,1:q0
q1,1:q2
```

Expected result: a DFA with 3 states, `{q0}` (initial), `{q0,q1}` and `{q0,q2}` (accepting).

## Running the tests

The tests need only Python (no Tkinter or Graphviz):

```
python test_cases.py
```

They cover three NFAs (strings ending in `01`, third symbol from the end is `1`, and an ε-NFA for `a*b* | c`) and check the DFA against a direct NFA simulation on all strings up to length 8. Expected output ends with `OK`.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'tkinter'`** – install Tkinter (`sudo apt install python3-tk` on Linux; reinstall Python with Tkinter on Windows).
- **`ModuleNotFoundError: No module named 'graphviz'` or `'PIL'`** – run `pip install -r requirements.txt`.
- **"Could not render graph: failed to execute 'dot'"** – the Graphviz program is not installed or not on your PATH (see step 2). The states and table still display without it.
- **"Invalid NFA" dialog** – read the message; typical causes are an initial state that is not in the state list, an unknown symbol in a transition, or a duplicate `(state, symbol)` line.
