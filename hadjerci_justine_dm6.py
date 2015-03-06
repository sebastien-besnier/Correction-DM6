@author: Justine Hadjerci
"""

0) X+2*X**2+3*X**3
1) P=Polynome([1,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
2) 1ère méthode: P.lead
2ème méthode:
    n=P.deg
    P[n]
3) P[0]
4)
P= Polynome([1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5]) 
Q= Polynome([-2,3,0,0,0,0,0,0,0,0,0,0,42])
P%Q
Q[9]

5)
def polynome_nul(P):
    res=True
    for i in range (0,(P.deg)+1):
        if not P[i]==0:
            res=False 
    return res


def binomial(k,n):
     P=(X+1)**n
     F=P[X]
     return F
    
        
def eval_poly(P,x):
    S=0
    for i in range (0,((P.deg)+1):
        S= S+P[i]*x**i
    return S


def derivative (P):
    for i in range ((P.deg)+1):
        P[i]=P[i]*i
        i=i-1
    return P

def sturm_sequence(P):
    l=[]
    P_0=P
    P_1=derivative(P)
    l.append(P_0)
    l.append(P_1)
    while P_(i-1)%P_(i)!=0:
        P_(i+2)=-(P_i%P_(i+1))
        l.append(P_(i+2))
    return l
    

def nb_change_sign_at(polys,x):
    c=0
    L=[]
    for i in range(len(polys)+1):
        L.append(eval_poly(P_i,x))
    for j in range (len(L)+1):
        if L[i]>=0 and L[i+1]<0:
            c=c+1
        if L[i]<0 and L[i+1]>=0:
            c=c+1
    return c
    

def nb_roots_between(polys, a, b):
    Ra=nb_change_sign_at(polys,a)
    Rb=nb_change_sign_at(polys,b)
    R=Ra-Rb
    return R
    
    
def roots_range(P):
    for i in range ((P.deg)+1):
        S=S+P[i]
        M=1
        if S>M:
            M=S
        return M
        
    
