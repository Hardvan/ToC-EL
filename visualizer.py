import graphviz as gv


def visualize_dfa(dfa):
    """Visualizes a DFA using Graphviz.

    Args:
        dfa: A dictionary representing the DFA, with the following structure:
            - 'states': A list of states.
            - 'alphabet': A list of input symbols.
            - 'transitions': A dictionary of transitions, where keys are tuples
              of (state, input symbol), and values are the next states.
            - 'start_state': The start state.
            - 'accept_states': A list of accepting states.

    Returns:
        A Graphviz object representing the DFA.
    """

    graph = gv.Digraph(format='png')  # Choose a suitable output format

    # Add nodes for states, highlighting accepting states
    for state in dfa['states']:
        shape = 'doublecircle' if state in dfa['accept_states'] else 'circle'
        graph.node(state, shape=shape)

    # Add edges for transitions
    for (state, symbol), next_state in dfa['transitions'].items():
        # Special handling for empty string
        label = f"{symbol}" if symbol != 'λ' else 'ε'
        graph.edge(state, next_state, label=label)

    # Highlight the start state
    graph.node(dfa['start_state'], shape='circle',
               style='filled', fillcolor='lightblue')

    return graph


# Example usage:

if __name__ == '__main__':
    dfa = {
        'states': ['q0', 'q1', 'q2'],
        'alphabet': ['0', '1'],
        'transitions': {
            ('q0', '0'): 'q0',
            ('q0', '1'): 'q1',
            ('q1', '0'): 'q2',
            ('q1', '1'): 'q0',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        },
        'start_state': 'q0',
        'accept_states': ['q2']
    }

    graph = visualize_dfa(dfa)
    graph.render('images/dfa_visualization')  # Render and save the diagram
