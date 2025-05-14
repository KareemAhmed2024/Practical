class NFA:
    def __init__(self, num_states, alphabet, transitions, start_state, accept_states):
        self.num_states = num_states  # Number of states in NFA
        self.alphabet = alphabet  # List of symbols in the alphabet
        self.transitions = transitions  # Transitions in the form {state: {symbol: [next_states]}}
        self.start_state = start_state  # Starting state
        self.accept_states = accept_states  # Accept states (set of states)

class DFA:
    def __init__(self, num_states, alphabet, transitions, start_state, accept_states):
        self.num_states = num_states  # Number of states in DFA
        self.alphabet = alphabet  # List of symbols in the alphabet
        self.transitions = transitions  # Transitions in the form {state: {symbol: next_state}}
        self.start_state = start_state  # Starting state
        self.accept_states = accept_states  # Accept states (set of states)

def epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)
    
    while stack:
        current_state = stack.pop()
        for next_state in nfa.transitions.get(current_state, {}).get('ε', []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    
    return closure


def move(nfa, states, symbol):
    # Move from a set of states on a symbol
    next_states = set()
    for state in states:
        if symbol in nfa.transitions.get(state, {}):
            next_states.update(nfa.transitions[state][symbol])
    return next_states

def nfa_to_dfa(nfa):
    start_closure = epsilon_closure(nfa, {nfa.start_state})
    start_state = frozenset(start_closure)
    
    dfa = DFA(
        num_states=0,
        alphabet=nfa.alphabet,
        transitions={},
        start_state=start_state,
        accept_states=set()
    )
    
    unmarked_states = [start_state]
    state_map = {start_state: dfa.num_states}
    dfa.num_states += 1
    
    while unmarked_states:
        current_dfa_state = unmarked_states.pop()
        for symbol in nfa.alphabet:
            if symbol != 'ε':
                next_nfa_states = move(nfa, current_dfa_state, symbol)
                next_closure = epsilon_closure(nfa, next_nfa_states)
                next_dfa_state = frozenset(next_closure)
                
                if next_dfa_state:
                    if next_dfa_state not in state_map:
                        state_map[next_dfa_state] = dfa.num_states
                        dfa.num_states += 1
                        unmarked_states.append(next_dfa_state)
                    
                    dfa.transitions.setdefault(current_dfa_state, {})[symbol] = next_dfa_state
                    
                    if any(state in nfa.accept_states for state in next_closure):
                        dfa.accept_states.add(next_dfa_state)
    
    return dfa

# Example usage
nfa = NFA(
    num_states=3,
    alphabet=['a', 'b'],
    transitions={
        0: {'ε': [1], 'a': [0], 'b': [1]},
        1: {'a': [2], 'b': [2]},
        2: {'b': [0]}
    },
    start_state=0,
    accept_states={2}
)

dfa = nfa_to_dfa(nfa)

# Output DFA transitions and accept states
print(f'DFA Start State: {dfa.start_state}')
print('DFA Transitions:')
for state, transitions in dfa.transitions.items():
    for symbol, next_state in transitions.items():
        print(f'  {state} --{symbol}--> {next_state}')
print(f'DFA Accept States: {dfa.accept_states}')
