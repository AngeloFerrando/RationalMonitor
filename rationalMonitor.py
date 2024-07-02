import sys
sys.path.insert(0,'/home/angelo/usr/lib/python3.10/site-packages/')
import spot
import time
from enum import Enum
import buddy
import importlib
from timeout_decorator import timeout

class Verdict(Enum):
    ff = 0
    tt = 1
    nf = 2
    nt= 3
    unknown = 4
    undefined = 5
    def __str__(self):
        if self.value == 0:
            return 'False'
        elif self.value == 1:
            return 'True'
        elif self.value == 2:
            return 'Unknown (but it won\'t ever be False)'
        elif self.value == 3:
            return 'Unknown (but it won\'t ever be True)'
        elif self.value == 4:
            return 'Unknown'
        else:
            return 'Undefined'

class RationalMonitor:
    def __init__(self, ltl, ap, sim, costs, resource_bound):
        eLTL = explicit_ltl(spot.formula(ltl).negative_normal_form().to_str(), ap)
        print('Explicit LTL: ', eLTL)
        enLTL = explicit_ltl(spot.formula('!(' + ltl + ')').negative_normal_form().to_str(), ap)
        print('Explicit negation of LTL: ', enLTL)
        self.__pAut = spot.translate(eLTL)
        self.__nAut = spot.translate(enLTL)
        self.__uAut = spot.translate('!('+eLTL+')&'+'!('+enLTL+')')
        # print(self.__uAut.to_str('hoa'))
        self.__pInit, self.__pFin = self.setup(self.__pAut)
        self.__nInit, self.__nFin = self.setup(self.__nAut)
        self.__uInit, self.__uFin = self.setup(self.__uAut)
        self.__ap = ap
        payoffs = get_payoffs(spot.formula(ltl), sim)
        print(f'Payoffs: {payoffs}')
        sim_to_break = knapsack(payoffs, costs, resource_bound)
        print(f'broken sim: {sim_to_break}')
        self.__sim = [s for s in sim if s not in sim_to_break]
        # self.__sim = sim
    def setup(self, aut):
        fin = set()
        states = set()
        statesAux = set()
        init = aut.get_init_state_number()
        states.add(aut.get_init_state_number())
        statesAux.add(aut.get_init_state_number())
        while statesAux:
            s0 = statesAux.pop()
            for t in aut.out(s0):
                if t.dst not in states:
                    states.add(t.dst)
                    statesAux.add(t.dst)
        for s in states:
            aut.set_init_state(s)
            if not aut.is_empty():
                fin.add(s)
        aut.set_init_state(init)
        initSet = set()
        initSet.add(init)
        return initSet, fin
    def next(self, ev):
        print(ev)
        event = buddy.bddtrue
        for ap in self.__ap:
            if ap.startswith('!'): continue
            ind = []
            for s in self.__sim:
                if ap in s:
                    ind = s
                    break
            # print(ind)
            if not ind and ap in ev:
                a = self.__pAut.register_ap(ap+'tt')
                b = self.__pAut.register_ap(ap+'ff')
                bdda = buddy.bdd_ithvar(a)
                bddb = buddy.bdd_nithvar(b)
                event = event & bdda & bddb
            elif not ind and ap not in ev:
                a = self.__pAut.register_ap(ap+'ff')
                b= self.__pAut.register_ap(ap+'tt')
                bdda = buddy.bdd_ithvar(a)
                bddb = buddy.bdd_nithvar(b)
                event = event & bdda & bddb
            elif ind and all(elem in ev for elem in ind):
                a = self.__pAut.register_ap(ap+'tt')
                b = self.__pAut.register_ap(ap+'ff')
                bdda = buddy.bdd_ithvar(a)
                bddb = buddy.bdd_nithvar(b)
                event = event & bdda & bddb
            elif ind and all(elem not in ev for elem in ind):
                a = self.__pAut.register_ap(ap+'ff')
                b = self.__pAut.register_ap(ap+'tt')
                bdda = buddy.bdd_ithvar(a)
                bddb = buddy.bdd_nithvar(b)
                event = event & bdda & bddb
            else:
                a = self.__pAut.register_ap(ap+'tt')
                b = self.__pAut.register_ap(ap+'ff')
                bdda = buddy.bdd_nithvar(a)
                bddb = buddy.bdd_nithvar(b)
                event = event & bdda & bddb
        pInitAux = set()
        while self.__pInit:
            init = self.__pInit.pop()
            for t in self.__pAut.out(init):
                if (t.cond & event) != buddy.bddfalse and t.dst in self.__pFin:
                    pInitAux.add(t.dst)
        self.__pInit = pInitAux
        nInitAux = set()
        while self.__nInit:
            init = self.__nInit.pop()
            for t in self.__nAut.out(init):
                if (t.cond & event) != buddy.bddfalse and t.dst in self.__nFin:
                    nInitAux.add(t.dst)
        self.__nInit = nInitAux
        uInitAux = set()
        while self.__uInit:
            init = self.__uInit.pop()
            for t in self.__uAut.out(init):
                if (t.cond & event) != buddy.bddfalse and t.dst in self.__uFin:
                    uInitAux.add(t.dst)
        self.__uInit = uInitAux
        foundP = len(self.__pInit) > 0
        foundN = len(self.__nInit) > 0
        foundU = len(self.__uInit) > 0
        if not foundN and not foundU:
            return Verdict.tt
        elif not foundP and not foundU:
            return Verdict.ff
        elif not foundP and not foundN:
            return Verdict.undefined
        elif not foundN:
            return Verdict.nf
        elif not foundP:
            return Verdict.nt
        else:
            return Verdict.unknown

def explicit_ltl(ltlstr, ap):
    # print(ltlstr)
    for atom in ap:
        ltlstr = ltlstr.replace('!' + atom, atom + 'ff')
    for atom in ap:
        # print(atom)
        j = 0
        while True:
            i = ltlstr.find(atom, j)
            if i == -1:
                break
            if (i+len(atom)) >= len(ltlstr) or ltlstr[i+len(atom)] != 'f':
                ltlstr = ltlstr[:i] + atom + 'tt' + ltlstr[i+len(atom):]
            j = i+1
    return ltlstr

def get_payoffs(phi, sim):
    payoffs = {}
    for s in sim:
        payoffs[str(s).replace('\'', '').replace(' ', '')] = 0.0
    atomic_propositions = spot.atomic_prop_collect(phi)
    for atomic_proposition in atomic_propositions:
        for s in payoffs:
            if atomic_proposition.to_str() in s.replace('[', '').replace(']', '').split(','):
                payoffs[s] += metric.metric(phi, atomic_proposition.to_str())
    return payoffs

def knapsack(payoffs, costs, resource_bound):
    # Convert input dictionaries to lists for easier indexing
    atoms = list(payoffs.keys())
    payoff_values = [payoffs[atom] for atom in atoms]
    cost_values = [costs[atom] for atom in atoms]
    n = len(atoms)
    
    # Initialize the DP table
    dp = [[0.0 for _ in range(int(resource_bound * 100) + 1)] for _ in range(n + 1)]
    
    # Build the table in bottom-up manner
    for i in range(1, n + 1):
        for w in range(int(resource_bound * 100) + 1):
            if int(cost_values[i-1] * 100) <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - int(cost_values[i-1] * 100)] + payoff_values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    
    # Find the items to include in the knapsack
    res = dp[n][int(resource_bound * 100)]
    w = int(resource_bound * 100)
    selected_atoms = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i-1][w]:
            continue
        else:
            selected_atoms.append(atoms[i-1])
            res -= payoff_values[i-1]
            w -= int(cost_values[i-1] * 100)
    
    return [atom.replace('[', '').replace(']', '').replace('\'', '').split(',') for atom in selected_atoms]

@timeout(5)
def main(args):
    global metric
    ltl = args[1]
    ap = set(args[2].replace('[','').replace(']','').replace(' ', '').split(','))
    aux = args[3]
    sim = []
    i = aux.find('[')
    j = aux.find(']')
    while i != -1 and j != -1:
        sim.append(aux[i+1:j].replace(' ', '').split(','))
        i = aux.find('[', i+1)
        j = aux.find(']', j+1)
    costs = {}
    for c in args[4].split(';'):
        costs[c.split(':')[0].replace(' ', '')] = float(c.split(':')[1])
    resource_bound = float(args[5])
    filename = args[6]
    metric = importlib.import_module(args[7])
    print('ltl ' + str(ltl))
    print('ap ' + str(ap))
    print('sim ' + str(sim))
    print('costs ' + str(costs))
    print('resource bound ' + str(resource_bound))
    print(filename)
    monitor = RationalMonitor(ltl, ap, sim, costs, resource_bound)
    verdict = None
    with open(filename, 'r') as file:
        while True:
            event = file.readline()
            if not event:
                break
            verdict = monitor.next(set(event.replace('\n', '').replace(' ', '').split(',')))
    print('Verdict: ' + str(verdict))
    return str(verdict)

if __name__ == '__main__':
    main(sys.argv)

# main(["", "X a", "[a,b,c]", "[a,b]", "[a,b]:10", "10", "test.txt"])
