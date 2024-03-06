from flask import Flask, render_template, request, jsonify


# Custom module
import visualizer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pda_visualize', methods = ['POST'])
def pda_visualize():
    states = request.form['states']
    alphabet = request.form['alphabets']
    stack_alphabet = request.form['stack_alphabet']
    transitions = request.form['transitions']
    start_state = request.form['start']
    start_stack = request.form['start_stack']
    accept_states = request.form['final']

    pda = preprocess_pda(states, alphabet, stack_alphabet, transitions, start_state, start_stack, accept_states)
    print(pda)    

    graph = visualizer.visualize_pda(pda)
    save_path_pda = 'static/output/pda/pda_visualization'
    # Render and save the diagram
    graph.render(save_path_pda, cleanup=True)
    print(f"\n✅ PDA visualization saved to {save_path_pda}.png")

    return render_template('index.html', pda_visualization = f"{save_path_pda}.png")

def preprocess_pda(states, alphabet, stack_alphabet, transitions, start_state, start_stack, accept_states):
    states = states.split(',') 
    states = [v.strip() for v in states]

    alphabet = alphabet.split(',')  # ['a', ' b']
    alphabet = [t.strip() for t in alphabet]  # ['a', 'b']

    stack_alphabet = stack_alphabet.split(',') 
    stack_alphabet = [v.strip() for v in stack_alphabet]

    transitions = transitions.split(';')
    transitions = [t.strip() for t in transitions]
    transitions = [t.split(',') for t in transitions]
    transitions = [[t.strip() for t in transition]
                   for transition in transitions]
    transitions_dict = {}
    for t in transitions:
        transitions_dict[(t[0], t[1], t[2])] = [(t[3], t[4])]

    start_state = start_state.strip()

    start_stack = start_stack.strip()

    accept_states = accept_states.split(',') 
    accept_states = [v.strip() for v in accept_states]

    pda = {
        'states': states,
        'alphabet': alphabet,
        'stack_alphabet': stack_alphabet,
        'transitions': transitions_dict,
        'start_state': start_state,
        'start_stack': start_stack,
        'accept_states': accept_states
    }

    return pda



@app.route('/rg_visualize', methods = ['POST'])
def rg_visualize():
    states = request.form['states']  # q0, q1, q2, qf
    alphabets = request.form['alphabets']  # a, b
    # q0, a, q1; q1, b, q2; q2, a, qf
    transitions = request.form['transitions']
    start = request.form['start']  # q0
    final = request.form['final']  # qf

    dfa = preprocess_dfa(states, alphabets, transitions, start, final)

    # 1) Visualize the DFA
    graph = visualizer.visualize_dfa(dfa)
    save_path_dfa = 'static/output/dfa/dfa_visualization'
    # Render and save the diagram
    graph.render(save_path_dfa, cleanup=True)
    print(f"\n✅ DFA visualization saved to {save_path_dfa}.png")

    # 2) covert to rg
    rg = visualizer.convert_dfa_to_rg(dfa)
    graph = visualizer.visualize_rg(rg)
    save_path_rg = 'static/output/rg/rg_visualization'
    graph.render(save_path_rg, cleanup=True)
    print(f"\n✅ RG visualization saved to {save_path_rg}.png")
    return render_template('index.html', dfa_visualization_conv = f"{save_path_dfa}.png", rg_visualization_conv = f"{save_path_rg}.png")

@app.route('/rg_dfa_visualize', methods = ['POST'])
def rg_dfa_visualize():
    variables = request.form['variables']
    terminals = request.form['terminals']
    productions = request.form['productions']
    start = request.form['start']

    rg = preprocess_rg(variables, terminals, productions, start)
    print(rg)
    graph = visualizer.visualize_rg(rg)
    save_path_rg = 'static/output/rg/rg_visualization'
    graph.render(save_path_rg, cleanup=True)
    print(f"\n✅ RG visualization saved to {save_path_rg}.png")

    dfa = visualizer.convert_rg_to_dfa(rg)
    graph = visualizer.visualize_dfa(dfa)
    save_path_dfa = 'static/output/dfa/dfa_visualization'
    # Render and save the diagram
    graph.render(save_path_dfa, cleanup=True)
    print(f"\n✅ DFA visualization saved to {save_path_dfa}.png")

    return render_template('index.html', dfa_visualization_rev = f"{save_path_dfa}.png", rg_visualization_rev = f"{save_path_rg}.png")

def preprocess_rg(variables, terminals, productions, start):
    variables = variables.split(',') 
    variables = [v.strip() for v in variables] 

    terminals = terminals.split(',')  # ['a', ' b']
    terminals = [t.strip() for t in terminals]  # ['a', 'b']

    productions = productions.split(';')
    productions = [t.strip() for t in productions]
    productions = [t.split(',') for t in productions]
    productions = [[t.strip() for t in production]
                   for production in productions]
    productions_dict = {}
    for t in productions:
        productions_dict[t[0]] = t[1:]


    start = start.strip()  # 'S'

    rg = {
        'variables': variables,
        'terminals': terminals,
        'productions': productions_dict,
        'start_variable': start
    }

    print(f"DFA: {rg}")

    return rg



@app.route('/dfa_visualize', methods=['POST'])
def dfa_visualize():

    states = request.form['states']  # q0, q1, q2, qf
    alphabets = request.form['alphabets']  # a, b
    # q0, a, q1; q1, b, q2; q2, a, qf
    transitions = request.form['transitions']
    start = request.form['start']  # q0
    final = request.form['final']  # qf
    input_string = request.form['input_string'].strip()  # ababab

    dfa = preprocess_dfa(states, alphabets, transitions, start, final)

    # 1) Visualize the DFA
    graph = visualizer.visualize_dfa(dfa)
    save_path_dfa = 'static/output/dfa/dfa_visualization'
    # Render and save the diagram
    graph.render(save_path_dfa, cleanup=True)
    print(f"\n✅ DFA visualization saved to {save_path_dfa}.png")

    # 2) Visualize the DFA path for the input string
    s = input_string
    graph, accepted, path = visualizer.visualize_dfa_path(dfa, s)
    print(f"String: {s}, Accepted: {accepted}, Path: {path}")
    save_path_trace = f'static/output/dfa/dfa_path_visualization_{s}'
    graph.render(save_path_trace, cleanup=True)
    print(f"\n✅ DFA path visualization saved to {save_path_trace}.png")

    return render_template("index.html",
                           dfa_visualization=f"{save_path_dfa}.png",
                           dfa_path_visualization=f"{save_path_trace}.png",
                           accepted=accepted, path=path)


@app.route('/nfa_visualize', methods=['POST'])
def nfa_visualize():

    states = request.form['states']
    alphabets = request.form['alphabets']
    transitions = request.form['transitions']
    start = request.form['start']
    final = request.form['final']

    nfa = preprocess_nfa(states, alphabets, transitions, start, final)

    # 1) Visualize the NFA
    graph = visualizer.visualize_nfa(nfa)
    save_path_nfa = 'static/output/nfa/nfa_visualization'
    # Render and save the diagram
    graph.render(save_path_nfa, cleanup=True)
    print(f"\n✅ NFA visualization saved to {save_path_nfa}.png")

    # 2) Convert NFA to DFA
    dfa = visualizer.convert_nfa_to_dfa(nfa)
    graph = visualizer.visualize_dfa(dfa)
    save_path_dfa = 'static/output/nfa/nfa_to_dfa_visualization'
    # Render and save the diagram
    graph.render(save_path_dfa, cleanup=True)
    print(f"\n✅ NFA to DFA visualization saved to {save_path_dfa}.png")

    return render_template("index.html",
                           nfa_visualization=f"{save_path_nfa}.png",
                           nfa_to_dfa_visualization=f"{save_path_dfa}.png")


@app.route('/enfa_visualize', methods=['POST'])
def enfa_visualize():

    states = request.form['states']
    alphabets = request.form['alphabets']
    transitions = request.form['transitions']
    start = request.form['start']
    final = request.form['final']

    e_nfa = preprocess_enfa(states, alphabets, transitions, start, final)

    # Calculate epsilon closures (optional, if not already provided in e_nfa)
    e_nfa['epsilon_closures'] = visualizer.calculate_epsilon_closures(e_nfa)
    print(f"Epsilon closures: {e_nfa['epsilon_closures']}")

    # 1) Visualize the e-NFA
    graph = visualizer.visualize_e_nfa(e_nfa)
    save_path_enfa = 'static/output/enfa/enfa_visualization'
    # Render and save the diagram
    graph.render(save_path_enfa, cleanup=True)
    print(f"\n✅ e-NFA visualization saved to {save_path_enfa}.png")

    return render_template("index.html",
                           epsilon_closures=e_nfa['epsilon_closures'],
                           enfa_visualization=f"{save_path_enfa}.png")


def preprocess_dfa(states, alphabets, transitions, start, final):

    # Preprocessing
    states = states.split(',')  # ['q0', ' q1 ', ' q2 ', ' qf ']
    states = [s.strip() for s in states]  # ['q0', 'q1', 'q2', 'qf']

    alphabets = alphabets.split(',')  # ['a', ' b']
    alphabets = [a.strip() for a in alphabets]  # ['a', 'b']

    # ['q0, a, q1', ' q1, b, q2', ' q2, a, qf']
    transitions = transitions.split(';')
    # ['q0, a, q1', 'q1, b, q2', 'q2, a, qf']
    transitions = [t.strip() for t in transitions]
    transitions = [t.split(',') for t in transitions]
    transitions = [[t.strip() for t in transition]
                   for transition in transitions]  # [['q0', 'a', 'q1'], ['q1', 'b', 'q2'], ['q2', 'a', 'qf']]
    transitions_dict = {}
    for t in transitions:
        transitions_dict[(t[0], t[1])] = t[2]

    start = start.strip()  # 'q0'
    final = final.split(',')
    final = [f.strip() for f in final]  # ['qf']

    """dfa = {
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
        }"""

    dfa = {
        'states': states,
        'alphabet': alphabets,
        'transitions': transitions_dict,
        'start_state': start,
        'accept_states': final
    }

    print(f"DFA: {dfa}")

    return dfa


def preprocess_nfa(states, alphabets, transitions, start, final):
    """nfa = {
            'states': ['q0', 'q1', 'q2'],
            'alphabet': ['0', '1'],
            'transitions': {
                ('q0', '0'): ['q0', 'q1'],  # Multiple next states for '0'
                ('q0', '1'): ['q1'],
                ('q1', '0'): ['q2'],
                ('q1', '1'): ['q0'],
                ('q2', '1'): ['q2']
            },
            'start_state': 'q0',
            'accept_states': ['q2']
        }
    """

    # Preprocessing
    states = states.split(',')  # ['q0', ' q1 ', ' q2 ', ' qf ']
    states = [s.strip() for s in states]  # ['q0', 'q1', 'q2', 'qf']

    alphabets = alphabets.split(',')  # ['a', ' b']
    alphabets = [a.strip() for a in alphabets]  # ['a', 'b']

    # q0, 0, q0, q1; q0, 1, q1; q1, 0, q2; q1, 1, q0; q2, 1, q2
    # ['q0, 0, q0, q1', 'q0, 1, q1', 'q1, 0, q2', 'q1, 1, q0', 'q2, 1, q2']
    transitions = transitions.split(';')
    transitions = [t.strip() for t in transitions]
    transitions = [t.split(',') for t in transitions]
    transitions = [[t.strip() for t in transition]
                   for transition in transitions]
    transitions_dict = {}
    for t in transitions:
        transitions_dict[(t[0], t[1])] = t[2:]

    start = start.strip()  # 'q0'
    final = final.split(',')
    final = [f.strip() for f in final]  # ['qf']

    nfa = {
        'states': states,
        'alphabet': alphabets,
        'transitions': transitions_dict,
        'start_state': start,
        'accept_states': final
    }

    print(f"NFA: {nfa}")

    return nfa


def preprocess_enfa(states, alphabets, transitions, start, final):
    """e_nfa = {
            'states': ['q0', 'q1', 'q2', 'q3'],
            'alphabet': ['a', 'b'],
            'transitions': {
                ('q0', 'λ'): ['q1', 'q3'],
                ('q1', 'a'): ['q2'],
                ('q2', 'b'): ['q0'],
                ('q3', 'b'): ['q2']
            },
            'start_state': 'q0',
            'accept_states': ['q2']
        }
    """

    states = states.split(',')
    states = [s.strip() for s in states]

    alphabets = alphabets.split(',')
    alphabets = [a.strip() for a in alphabets]

    transitions = transitions.split(';')
    transitions = [t.strip() for t in transitions]
    transitions = [t.split(',') for t in transitions]
    transitions = [[t.strip() for t in transition]
                   for transition in transitions]
    transitions_dict = {}
    for t in transitions:
        transitions_dict[(t[0], t[1])] = t[2:]

    start = start.strip()
    final = final.split(',')
    final = [f.strip() for f in final]

    e_nfa = {
        'states': states,
        'alphabet': alphabets,
        'transitions': transitions_dict,
        'start_state': start,
        'accept_states': final
    }

    print(f"e-NFA: {e_nfa}")

    return e_nfa


if __name__ == "__main__":
    app.run(debug=True)
