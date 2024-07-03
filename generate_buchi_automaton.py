def generate_hoa(trace):
    # Split the trace into events
    events = [event.split(",") for event in trace]

    # Create the list of atomic propositions (APs)
    aps = sorted(set(atom for event in events for atom in event))
    
    # Create states
    num_states = len(events) + 1  # Including the final accepting state
    states = range(num_states)

    # Create transitions
    transitions = []
    for i, event in enumerate(events):
        condition = " & ".join([f"({aps.index(atom)})" for atom in event])
        transitions.append((i, condition, i + 1))
    
    # Add transitions to the accepting state
    transitions.append((num_states - 1, "t", num_states - 1))  # t is a transition that always matches
    
    # Generate HOA format output
    hoa_output = []
    hoa_output.append("HOA: v1")
    hoa_output.append(f"States: {num_states}")
    hoa_output.append("Start: 0")
    hoa_output.append(f"AP: {len(aps)} " + " ".join(f'"{ap}"' for ap in aps))
    hoa_output.append("--BODY--")

    for state in states:
        hoa_output.append(f"State: {state}")
        for (src, cond, dst) in transitions:
            if src == state:
                hoa_output.append(f"[{cond}] {dst}")

    hoa_output.append("--END--")
    hoa_output.append("Acceptance: 1 Inf(0)")  # Default acceptance condition

    return "\n".join(hoa_output)

# # Example usage
# trace = ["a,b", "c", "d"]
# hoa_automaton = generate_hoa(trace)
# print(hoa_automaton)
