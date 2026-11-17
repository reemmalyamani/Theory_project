
class NFA:
    def __init__(self, states, alphabet, initial_state,
                 accepting_states, transitions):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.initial_state = initial_state
        self.accepting_states = set(accepting_states)
        self.transitions = transitions

    def get_next_states(self, state, symbol):
        return self.transitions.get((state, symbol), set())
