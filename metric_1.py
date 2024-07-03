import sys
# sys.path.insert(0,'/home/angelo/usr/lib/python3.10/site-packages/')
import spot

def metric(phi, atom):
    i_phi = iter(phi)
    if phi._is(spot.op_X): # next
        sub_phi = next(i_phi)
        return 1.0 * metric(sub_phi, atom)
    elif phi._is(spot.op_U): # until
        sub_phi_1 = next(i_phi)
        sub_phi_2 = next(i_phi)
        return 0.3*metric(sub_phi_1, atom) + 0.7*metric(sub_phi_2, atom)
    elif phi._is(spot.op_F): # eventually
        sub_phi = next(i_phi)
        return 0.3 * metric(sub_phi, atom)
    elif phi._is(spot.op_G): # globally
        sub_phi = next(i_phi)
        return 0.7 * metric(sub_phi, atom)
    elif phi._is(spot.op_And): # conjunction
        my_metric = 0.0
        for sub_phi in phi:
            my_metric = max(metric(sub_phi, atom), my_metric)
        return my_metric
    elif phi._is(spot.op_Or): # disjunction
        my_metric = 0.0
        n = 0
        for sub_phi in phi:
            my_metric += metric(sub_phi, atom)
            n += 1
        return my_metric / n
    elif phi._is(spot.op_Not): # negation
        sub_phi = next(i_phi)
        return metric(sub_phi, atom)
    else: # atomic proposition
        return 1.0 if phi.to_str() == atom else 0.0

# # print(dir(spot))
# phi = spot.formula('(Xp && q) || a || b')
# # print(dir(phi))
# payoffs = get_payoffs(phi, [['p', 'q'], ['a', 'b']])
# print(payoffs)
# costs = {'[\'p\', \'q\']': 20, '[\'a\', \'b\']': 10}
# resource_bound = 25
# optimal_atoms = knapsack(payoffs, costs, resource_bound)
# print(f'Optimal atoms according to metric: {optimal_atoms}')
