import sys
import string
# sys.path.insert(0,'/home/angelo/usr/lib/python3.10/site-packages/')
import spot
import random

def check(f):
    global ok
    if f._is(spot.op_Implies) or f._is(spot.op_Xor) or f._is(spot.op_W) or f._is(spot.op_M) or f._is(spot.op_R) or f._is(spot.op_ff) or f._is(spot.op_tt) or f._is(spot.op_Equiv):
        ok = False
    return False

def random_split(input_string, num_parts):
    # Remove the brackets and split the string into a list
    elements = input_string.strip('[]').split(', ')
    
    # Shuffle the list to ensure randomness
    random.shuffle(elements)
    
    # Calculate the size of each part
    part_size = len(elements) // num_parts
    remainder = len(elements) % num_parts
    
    # Create the list of parts
    parts = []
    start = 0
    
    for i in range(num_parts):
        end = start + part_size + (1 if i < remainder else 0)
        parts.append(elements[start:end])
        start = end
    
    # Randomly decide which parts to keep
    keep_count = random.randint(1, num_parts)
    parts_to_keep = random.sample(parts, keep_count)
    
    return parts_to_keep

def main(args):
    global ok
    # n = 1000
    n = int(args[1])
    # min_size_ltl = int(args[2])
    # max_size_ltl = int(args[3])
    ap = list(string.ascii_lowercase)
    with open('props.txt', 'w') as file:
        count = 0
        for ltl in spot.randltl(list(ap)):
            if count >= n: break
            ok = True
            ltl.traverse(check)
            if not ok: continue
            atoms = str(spot.atomic_prop_collect(ltl)).replace('"', '').replace('\'', '').replace('{', '[').replace('}', ']')
            if len(atoms.split(',')) < 5: continue
            file.write(str(ltl).replace('|', '||').replace('&', '&&') + '$ ')
            file.write(atoms + '$ ')
            sim = [s for s in random_split(atoms, 3) if len(s)>1]
            file.write(str(sim)[1:-1].replace('\'', '') + '$ ')
            costs = ';'.join([str(s).replace('\'', '') + ':' + str(random.uniform(0, 30)) for s in sim])
            file.write(costs + '$ ')
            file.write(str(random.uniform(0,50)))
            file.write('\n')
            count += 1

if __name__ == '__main__':
    main(sys.argv)