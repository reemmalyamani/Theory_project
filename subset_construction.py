"""
Subset Construction Algorithm (NFA -> DFA)

This module takes the five parts of an NFA as plain
Python values and returns an equivalent DFA.

Expected NFA input format
-------------------------
states            : set of state names,          e.g. {"q0", "q1", "q2"}
alphabet          : set of input symbols,        e.g. {"0", "1"}
initial_state     : one state name,              e.g. "q0"
accepting_states  : set of state names,          e.g. {"q2"}
transitions       : dict {(state, symbol): set_of_destination_states}
                    e.g. {("q0", "0"): {"q0", "q1"}, ("q1", "1"): {"q2"}}
                    Epsilon transitions use the symbol "ε" or "λ".
                    A missing key means the transition goes to the empty set.
"""

from collections import deque

EPSILON_SYMBOLS = {"ε", "λ"}


class DFA:
    """Result of the subset construction.

    Every DFA state is a frozenset of NFA states.
    The empty frozenset is the dead (trap) state ∅, if it is reachable.
    """

    def __init__(self, states, alphabet, initial_state, accepting_states, transitions):
        self.states = states                    # list of frozensets, in discovery order
        self.alphabet = alphabet                # sorted list of symbols
        self.initial_state = initial_state      # frozenset
        self.accepting_states = accepting_states  # set of frozensets
        self.transitions = transitions          # {(frozenset, symbol): frozenset}

    # ---------- helpers for displaying the DFA ----------

    @staticmethod
    def state_name(subset):
        """Turn a frozenset of NFA states into a readable name like {q0,q1}."""
        if not subset:
            return "∅"
        return "{" + ",".join(sorted(subset)) + "}"

    def next_state(self, state, symbol):
        return self.transitions[(state, symbol)]

    def accepts(self, word):
        """Run the DFA on a sequence of symbols (string or list)."""
        current = self.initial_state
        for symbol in word:
            if symbol not in self.alphabet:
                return False
            current = self.transitions[(current, symbol)]
        return current in self.accepting_states

    def transition_table(self):
        """Return the transition table as a list of rows (list of strings).

        First row is the header. The first column marks the
        initial state with '→' and accepting states with '*'.
        """
        rows = [["", "State"] + list(self.alphabet)]
        for state in self.states:
            mark = ""
            if state == self.initial_state:
                mark += "→"
            if state in self.accepting_states:
                mark += "*"
            row = [mark, self.state_name(state)]
            for symbol in self.alphabet:
                row.append(self.state_name(self.transitions[(state, symbol)]))
            rows.append(row)
        return rows

    def table_as_text(self):
        rows = self.transition_table()
        widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
        lines = []
        for index, row in enumerate(rows):
            lines.append("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
            if index == 0:
                lines.append("  ".join("-" * w for w in widths))
        return "\n".join(lines)

    def summary(self):
        text = [
            "DFA states:       " + ", ".join(self.state_name(s) for s in self.states),
            "Initial state:    " + self.state_name(self.initial_state),
            "Accepting states: " + (", ".join(self.state_name(s) for s in self.states
                                              if s in self.accepting_states) or "none"),
            "",
            "Transition table:",
            self.table_as_text(),
        ]
        return "\n".join(text)


# ---------- the algorithm ----------

def epsilon_closure(nfa_states, transitions):
    """All NFA states reachable from `nfa_states` using only ε/λ moves
    (including the states themselves)."""
    closure = set(nfa_states)
    stack = list(nfa_states)
    while stack:
        state = stack.pop()
        for eps in EPSILON_SYMBOLS:
            for nxt in transitions.get((state, eps), set()):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
    return frozenset(closure)


def move(nfa_states, symbol, transitions):
    """Set of NFA states reachable from `nfa_states` by reading `symbol` once."""
    result = set()
    for state in nfa_states:
        result |= set(transitions.get((state, symbol), set()))
    return result


def subset_construction(states, alphabet, initial_state, accepting_states, transitions):
    """Convert an NFA (optionally with ε/λ transitions) into an equivalent DFA.

    Only DFA states reachable from the initial state are generated.
    The result is a complete DFA: if some subset has no move on a symbol,
    it goes to the dead state ∅ (which loops to itself on every symbol).
    """
    accepting_states = set(accepting_states)
    symbols = sorted(s for s in alphabet if s not in EPSILON_SYMBOLS)

    # 1) DFA initial state = ε-closure of the NFA initial state
    dfa_initial = epsilon_closure({initial_state}, transitions)

    dfa_states = [dfa_initial]
    seen = {dfa_initial}
    dfa_transitions = {}
    queue = deque([dfa_initial])

    # 2) Explore every reachable subset
    while queue:
        current = queue.popleft()
        for symbol in symbols:
            # 3) DFA transition: ε-closure( move(current, symbol) )
            target = epsilon_closure(move(current, symbol, transitions), transitions)
            dfa_transitions[(current, symbol)] = target
            if target not in seen:
                seen.add(target)
                dfa_states.append(target)
                queue.append(target)

    # 4) A DFA state accepts if it contains at least one NFA accepting state
    dfa_accepting = {s for s in dfa_states if s & accepting_states}

    return DFA(dfa_states, symbols, dfa_initial, dfa_accepting, dfa_transitions)


# ---------- quick demo / self-test ----------

if __name__ == "__main__":
    from itertools import product

    def nfa_accepts(word, initial_state, accepting_states, transitions):
        """Direct NFA simulation, used only to check the DFA is equivalent."""
        current = epsilon_closure({initial_state}, transitions)
        for symbol in word:
            current = epsilon_closure(move(current, symbol, transitions), transitions)
        return bool(current & set(accepting_states))

    tests = [
        ("Test 1: strings over {0,1} ending in 01",
         dict(states={"q0", "q1", "q2"}, alphabet={"0", "1"},
              initial_state="q0", accepting_states={"q2"},
              transitions={("q0", "0"): {"q0", "q1"}, ("q0", "1"): {"q0"},
                           ("q1", "1"): {"q2"}})),
        ("Test 2: third symbol from the end is 1",
         dict(states={"p", "q", "r", "s"}, alphabet={"0", "1"},
              initial_state="p", accepting_states={"s"},
              transitions={("p", "0"): {"p"}, ("p", "1"): {"p", "q"},
                           ("q", "0"): {"r"}, ("q", "1"): {"r"},
                           ("r", "0"): {"s"}, ("r", "1"): {"s"}})),
        ("Test 3: ε-NFA for a*b* | c",
         dict(states={"s", "a", "b", "c", "f"}, alphabet={"a", "b", "c"},
              initial_state="s", accepting_states={"f"},
              transitions={("s", "ε"): {"a", "c"},
                           ("a", "a"): {"a"}, ("a", "ε"): {"b"},
                           ("b", "b"): {"b"}, ("b", "ε"): {"f"},
                           ("c", "c"): {"f"}})),
    ]

    for title, nfa in tests:
        dfa = subset_construction(**nfa)
        print("=" * 60)
        print(title)
        print("=" * 60)
        print(dfa.summary())

        # Verify: DFA and NFA agree on every string up to length 8
        ok = True
        for length in range(9):
            for word in product(dfa.alphabet, repeat=length):
                if dfa.accepts(word) != nfa_accepts(word, nfa["initial_state"],
                                                    nfa["accepting_states"],
                                                    nfa["transitions"]):
                    ok = False
                    print("MISMATCH on", "".join(word))
        print("\nEquivalence check (all strings up to length 8):", "PASSED" if ok else "FAILED")
        print()
