from flask import Flask, render_template, request, jsonify


# Custom module
import visualizer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


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
                           result=True,
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
                           result=True,
                           nfa_visualization=f"{save_path_nfa}.png",
                           nfa_to_dfa_visualization=f"{save_path_dfa}.png")


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


if __name__ == "__main__":
    app.run(debug=True)
