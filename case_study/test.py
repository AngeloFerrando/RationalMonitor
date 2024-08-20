import rational_monitor

phi1 = 'F(c && Xw)'

phi2 = 'F(gamma && (b1 || b2 || b3) && Xmb)'

phi3 = 'F((!c && b1 && Xb2) || (!c && b2 && Xb3))'

psi1 = 'G((b1 || b2 || b3) -> X!c)'

psi2 = 'G(gamma -> !(b1 || b2 || b3))'

psi3 = 'G(!gamma -> !mb)'

psi1orpsi2 = '(' + psi1 + ' || ' + psi2 + ')'

properties = [('phi1', phi1), ('phi2', phi2), ('phi3', phi3), ('psi1', psi1), ('psi2', psi2), ('psi3', psi3), ('psi1orpsi2', psi1orpsi2)]

for (name, prop) in properties:
    print(f'\n{name}\n')
    print('Standard')
    rational_monitor.main(["", prop, "[b1,b2,b3,c,s,alpha,beta,gamma,mb,w]", "", "", "0", "100", "case_study/trace_standard.txt", "metrics.metric_2"])
    print('Passive')
    rational_monitor.main(["", prop, "[b1,b2,b3,c,s,alpha,beta,gamma,mb,w]", "[c,s];[alpha,beta,gamma]", "[c,s]:2;[alpha,beta,gamma]:3", "0", "100", "case_study/trace.txt", "metrics.metric_2"])
    print('Active')
    rational_monitor.main(["", prop, "[b1,b2,b3,c,s,alpha,beta,gamma,mb,w]", "[c,s];[alpha,beta,gamma]", "[c,s]:2;[alpha,beta,gamma]:3", "3", "100", "case_study/trace.txt", "metrics.metric_2"])
    print('Reactive')
    rational_monitor.main(["", prop, "[b1,b2,b3,c,s,alpha,beta,gamma,mb,w]", "[c,s];[alpha,beta,gamma]", "[c,s]:2;[alpha,beta,gamma]:3", "3", "2", "case_study/trace.txt", "metrics.metric_2"])
