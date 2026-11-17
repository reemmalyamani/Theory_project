class NFA:
    def __init__(self, states, alphabet, initial_state, accepting_states, transitions):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.accepting_states = set(accepting_states)
        self.transitions = {
            (source, symbol): set(destinations)
            for (source, symbol), destinations in transitions.items()
        }
        self.validate()

    def validate(self):
        if not self.states:
            raise ValueError("Enter at least one state.")
        if not self.alphabet:
            raise ValueError("Enter at least one alphabet symbol.")
        if self.initial_state not in self.states:
            raise ValueError("The initial state must be one of the NFA states.")
        if not self.accepting_states.issubset(self.states):
            raise ValueError("All accepting states must belong to the NFA states.")
        if self.alphabet & {"ε", "λ"}:
            raise ValueError("Do not include ε or λ in the input alphabet.")
        for (source, symbol), destinations in self.transitions.items():
            if source not in self.states:
                raise ValueError(f"Unknown transition source: {source}")
            if symbol not in self.alphabet and symbol not in {"ε", "λ"}:
                raise ValueError(f"Unknown transition symbol: {symbol}")
            if not destinations.issubset(self.states):
                raise ValueError(f"Unknown destination in transition ({source}, {symbol}).")

    def get_next_states(self, state, symbol):
        return set(self.transitions.get((state, symbol), set()))
