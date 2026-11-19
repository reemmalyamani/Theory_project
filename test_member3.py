import tkinter as tk

from subset_construction import subset_construction
from dfa_output import show_dfa_output


# Test NFA
states = {"q0", "q1", "q2"}
alphabet = {"0", "1"}
initial_state = "q0"
accepting_states = {"q2"}

transitions = {
    ("q0", "0"): {"q0", "q1"},
    ("q0", "1"): {"q0"},
    ("q1", "1"): {"q2"}
}

# Convert NFA to DFA
dfa = subset_construction(
    states,
    alphabet,
    initial_state,
    accepting_states,
    transitions
)

# Display DFA Output
root = tk.Tk()
root.withdraw()

show_dfa_output(root, dfa)

root.mainloop()