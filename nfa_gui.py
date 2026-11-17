import tkinter as tk
from tkinter import messagebox
from nfa_input import NFA


def parse_set(text):
    return {part.strip() for part in text.split(",") if part.strip()}


def parse_transitions(text):
    """Each line: source,symbol:destination1,destination2"""
    transitions = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.count(":") != 1:
            raise ValueError(f"Transition line {line_number}: expected one ':'.")
        left, right = line.split(":", 1)
        parts = [part.strip() for part in left.split(",")]
        if len(parts) != 2 or not all(parts):
            raise ValueError(f"Transition line {line_number}: use source,symbol:destinations")
        source, symbol = parts
        key = (source, symbol)
        if key in transitions:
            raise ValueError(f"Duplicate transition for ({source}, {symbol}). Combine destinations on one line.")
        transitions[key] = parse_set(right)
    return transitions


class NFAInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA Input – CSC339")
        self.root.geometry("570x600")
        self.nfa = None  # Member 2 can use this after a successful save.

        frame = tk.Frame(root, padx=20, pady=15)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="NFA Input & Representation", font=("Arial", 16, "bold")).pack(pady=(0, 12))

        self.entries = {}
        for label, example in [
            ("States", "q0,q1,q2"),
            ("Alphabet", "0,1"),
            ("Initial state", "q0"),
            ("Accepting states", "q2"),
        ]:
            tk.Label(frame, text=f"{label} (example: {example})", anchor="w").pack(fill="x")
            entry = tk.Entry(frame)
            entry.pack(fill="x", pady=(2, 10))
            self.entries[label] = entry

        tk.Label(frame, text="Transitions: source,symbol:destination1,destination2", anchor="w").pack(fill="x")
        self.transition_text = tk.Text(frame, height=9)
        self.transition_text.pack(fill="both", expand=True, pady=(4, 8))
        tk.Label(frame, text="One transition per line. Use ε or λ for epsilon transitions; leave destinations blank for ∅.", wraplength=520, justify="left").pack(anchor="w")
        tk.Button(frame, text="Save NFA", command=self.save_nfa).pack(pady=14)
        self.status = tk.Label(frame, text="No NFA saved yet.", anchor="w")
        self.status.pack(fill="x")

    def save_nfa(self):
        try:
            nfa = NFA(
                states=parse_set(self.entries["States"].get()),
                alphabet=parse_set(self.entries["Alphabet"].get()),
                initial_state=self.entries["Initial state"].get().strip(),
                accepting_states=parse_set(self.entries["Accepting states"].get()),
                transitions=parse_transitions(self.transition_text.get("1.0", "end")),
            )
        except ValueError as exc:
            self.status.config(text="Invalid input – NFA not saved.")
            messagebox.showerror("Invalid NFA", str(exc))
            return
        self.nfa = nfa
        self.status.config(text=f"Saved NFA with {len(nfa.states)} states and {len(nfa.transitions)} transitions.")
        print("NFA saved:", vars(nfa))
        messagebox.showinfo("Success", "NFA saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = NFAInputApp(root)
    root.mainloop()
