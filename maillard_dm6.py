from math import factorial
def binomial2(k, n):
    if k == 0:
        return 1
    if k > n:
        return 0
    else:
        return factorial(n) // factorial(k) // factorial(n-k)

def binomial(k, n):
    if k == 0:
        return 1
    if k > n:
        return 0
    else:
        return binomial(k,n-1) + binomial(k-1, n-1)


def eval_poly(P, x):
    res = 0
    for i in range (0, P.deg+1):
        res = res + (P[i] * x**i)
    return res
 
def derivative(P):
    coef = []
    for i in range (1, P.deg+1):
        coef.append(P[i]*i)
    return Polynome(coef)
     
 

def sturm_sequence(P):
    X = Polynome([0,1])
    sturm = [P]
    sturm.append(derivative(P))
    i=1
    while ((sturm[i-1] % sturm[i]) != X[0]):
        sturm.append(-(sturm[i-1] % sturm[i]))
        i = i + 1

    return sturm
         
def nb_change_sign_at(polys, x):
    eval = []
    for i in polys:
        r = eval_poly(i, x)
        if r != 0:
            eval.append(r)

    nb = 0
    for i in range(1,len(eval)) :
        if (eval[i-1] * eval[i]) < 0:
            nb = nb + 1
        
    return nb
 
 
def nb_roots_between(polys, a, b):
    return nb_change_sign_at(polys, a) - nb_change_sign_at(polys, b)
 
 
def roots_range(P):
    somme=0
    for i in range (0, P.deg+1):
        somme = somme + abs(P[i])

    return somme
     
def nb_roots(polys):
    return nb_roots_between(polys, -roots_range(polys[0]), roots_range(polys[0]))
 
def find_root(P, a, b, eps):
    deb = a * 1.0
    fin = b * 1.0
    milieu = 0.0
    while (fin-deb) > eps:
        milieu = deb + ((fin-deb) / 2)
        if eval_poly(P, milieu) * eval_poly(P, fin) <= 0:
            deb = milieu
        else:
            fin = milieu
    return deb
 
 
def isolate_roots(P):
    polys = sturm_sequence(P)
    M = 2*roots_range(P)
     
    def loop(a, b, n_prev):
        if n_prev == 1 or n_prev == 0:
            return []
         
        c = (a + b) / 2.
        n = nb_roots_between(polys, a, c)
         
        if n == n_prev:
            return loop(a, c, n)
        if n == 0:
            return loop(c, b, n_prev)
        return loop(a, c, n) + [c] + loop(c, b, n_prev -n)
     
    return [-M] + loop(-M, M, nb_roots_between(polys, -M, M)) + [M]
 
def roots(P, eps):
    S = []
    L = isolate_roots(P)
    for i in range(0,len(L)-1) :
        S.append(find_root(P, L[i], L[i+1], eps))
    return S