import sys
# sys.path.insert(0,'/home/angelo/usr/lib/python3.10/site-packages/')
import spot

def metric(phi, atom):
    i_phi = iter(phi)
    if phi._is(spot.op_X): # next
        sub_phi = next(i_phi)
        return 0.1 * metric(sub_phi, atom)
    elif phi._is(spot.op_U): # until
        sub_phi_1 = next(i_phi)
        sub_phi_2 = next(i_phi)
        return 0.9*metric(sub_phi_1, atom) + 0.1*metric(sub_phi_2, atom)
    elif phi._is(spot.op_F): # eventually
        sub_phi = next(i_phi)
        return 0.9 * metric(sub_phi, atom)
    elif phi._is(spot.op_G): # globally
        sub_phi = next(i_phi)
        return 0.1 * metric(sub_phi, atom)
    elif phi._is(spot.op_And): # conjunction
        my_metric = 0.0
        for sub_phi in phi:
            my_metric = min(metric(sub_phi, atom), my_metric)
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
