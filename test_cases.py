"""
Member 4: three NFA test cases for the subset construction.

Run:  python test_cases.py
Each test checks:
  - the number of DFA states,
  - specific strings that must be accepted / rejected,
  - equivalence with a direct NFA simulation on ALL strings up to length 8.
"""
import unittest
from itertools import product

from subset_construction import subset_construction, epsilon_closure, move

TEST1 = dict(  # strings over {0,1} ending in 01
    states={"q0", "q1", "q2"}, alphabet={"0", "1"},
    initial_state="q0", accepting_states={"q2"},
    transitions={("q0", "0"): {"q0", "q1"}, ("q0", "1"): {"q0"},
                 ("q1", "1"): {"q2"}})

TEST2 = dict(  # third symbol from the end is 1
    states={"p", "q", "r", "s"}, alphabet={"0", "1"},
    initial_state="p", accepting_states={"s"},
    transitions={("p", "0"): {"p"}, ("p", "1"): {"p", "q"},
                 ("q", "0"): {"r"}, ("q", "1"): {"r"},
                 ("r", "0"): {"s"}, ("r", "1"): {"s"}})

TEST3 = dict(  # epsilon-NFA for a*b* | c
    states={"s", "a", "b", "c", "f"}, alphabet={"a", "b", "c"},
    initial_state="s", accepting_states={"f"},
    transitions={("s", "ε"): {"a", "c"},
                 ("a", "a"): {"a"}, ("a", "ε"): {"b"},
                 ("b", "b"): {"b"}, ("b", "ε"): {"f"},
                 ("c", "c"): {"f"}})


def nfa_accepts(word, nfa):
    current = epsilon_closure({nfa["initial_state"]}, nfa["transitions"])
    for symbol in word:
        current = epsilon_closure(move(current, symbol, nfa["transitions"]),
                                  nfa["transitions"])
    return bool(current & set(nfa["accepting_states"]))


class SubsetConstructionTests(unittest.TestCase):
    def check_equivalence(self, nfa, dfa, max_len=8):
        for n in range(max_len + 1):
            for word in product(dfa.alphabet, repeat=n):
                self.assertEqual(dfa.accepts(word), nfa_accepts(word, nfa),
                                 f"mismatch on '{''.join(word)}'")

    def test1_ends_with_01(self):
        dfa = subset_construction(**TEST1)
        self.assertEqual(len(dfa.states), 3)
        for w in ["01", "001", "1101", "0101"]:
            self.assertTrue(dfa.accepts(w), w)
        for w in ["", "0", "1", "10", "011", "0110"]:
            self.assertFalse(dfa.accepts(w), w)
        self.check_equivalence(TEST1, dfa)

    def test2_third_from_end_is_1(self):
        dfa = subset_construction(**TEST2)
        self.assertEqual(len(dfa.states), 8)
        for w in ["100", "111", "0101", "11100"]:
            self.assertTrue(dfa.accepts(w), w)
        for w in ["", "0", "10", "000", "0010", "011"]:
            self.assertFalse(dfa.accepts(w), w)
        self.check_equivalence(TEST2, dfa)

    def test3_epsilon_nfa(self):
        dfa = subset_construction(**TEST3)
        # initial DFA state is the epsilon-closure of s
        self.assertEqual(dfa.initial_state, frozenset({"s", "a", "b", "c", "f"}))
        for w in ["", "a", "aab", "bbb", "abb", "c"]:
            self.assertTrue(dfa.accepts(w), w)
        for w in ["ba", "cc", "ac", "cb", "abc"]:
            self.assertFalse(dfa.accepts(w), w)
        self.check_equivalence(TEST3, dfa)

    def test_dfa_is_complete(self):
        for nfa in (TEST1, TEST2, TEST3):
            dfa = subset_construction(**nfa)
            for state in dfa.states:
                for symbol in dfa.alphabet:
                    self.assertIn((state, symbol), dfa.transitions)


if __name__ == "__main__":
    unittest.main(verbosity=2)
