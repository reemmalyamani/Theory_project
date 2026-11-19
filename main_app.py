"""
Member 4: Interface Integration & Testing
Connects: NFA input (nfa_gui) -> subset construction -> DFA output (dfa_output).

Run:  python main_app.py
"""
import tkinter as tk
from tkinter import messagebox

from nfa_gui import NFAInputApp, parse_set, parse_transitions
from nfa_input import NFA
from subset_construction import subset_construction
from dfa_output import show_dfa_output

EPSILON = {"ε", "λ"}


def build_nfa_from_fields(states_text, alphabet_text, initial_text,
                          accepting_text, transitions_text):
    """Parse the raw GUI text and return a validated NFA.
    Raises ValueError with a readable message on any problem."""
    states = parse_set(states_text)
    alphabet = parse_set(alphabet_text)
    initial = initial_text.strip()
    accepting = parse_set(accepting_text)

    # Extra checks on top of NFA.validate()
    if not states:
        raise ValueError("Enter at least one state.")
    if not alphabet:
        raise ValueError("Enter at least one alphabet symbol.")
    if not initial:
        raise ValueError("Enter an initial state.")
    bad_symbols = [a for a in alphabet if len(a) != 1 and a not in EPSILON]
    if bad_symbols:
        raise ValueError("Alphabet symbols must be single characters. "
                         f"Problem: {', '.join(sorted(bad_symbols))}")

    transitions = parse_transitions(transitions_text)
    if not transitions:
        raise ValueError("Enter at least one transition.")

    return NFA(states, alphabet, initial, accepting, transitions)


class IntegratedApp(NFAInputApp):
    """NFA input window + a 'Convert to DFA' button that opens the DFA output."""

    def __init__(self, root):
        super().__init__(root)
        self.root.title("NFA to DFA Converter – CSC339")
        self.root.geometry("570x680")
        self.dfa = None

        # Put the button in the same frame as the Save button / status label.
        container = self.status.master
        tk.Button(container, text="Convert to DFA", bg="#4CAF50", fg="white",
                  command=self.convert).pack(pady=(0, 10), before=self.status)

    def convert(self):
        # 1) Read + validate the current input fields directly,
        #    so the user does not have to press "Save NFA" first.
        try:
            nfa = build_nfa_from_fields(
                self.entries["States"].get(),
                self.entries["Alphabet"].get(),
                self.entries["Initial state"].get(),
                self.entries["Accepting states"].get(),
                self.transition_text.get("1.0", "end"),
            )
        except ValueError as exc:
            self.status.config(text="Invalid input – conversion not run.")
            messagebox.showerror("Invalid NFA", str(exc))
            return
        self.nfa = nfa

        # 2) Run the subset construction
        try:
            self.dfa = subset_construction(
                nfa.states, nfa.alphabet, nfa.initial_state,
                nfa.accepting_states, nfa.transitions,
            )
        except Exception as exc:
            self.status.config(text="Conversion failed.")
            messagebox.showerror("Conversion error", str(exc))
            return

        self.status.config(
            text=f"Converted: NFA {len(nfa.states)} states -> DFA {len(self.dfa.states)} states.")

        # 3) Show the DFA output window
        show_dfa_output(self.root, self.dfa)


if __name__ == "__main__":
    root = tk.Tk()
    IntegratedApp(root)
    root.mainloop()
