# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 14:07:59 2015

@author: Alice
"""

#Q0.
Polynome([0,1,2,3])
# 3*X**3 + 2*X**2 + X

#Q1. 
P = Polynome([1,0,3])
P[52]=1
P
# X**52 + 3*X**2 + 1

#Q2. 2 moyens pour connaitre le coefficient dominant :
P.lead
#1

#ou

P[P.deg]
#1.

#Q3.
P[0]

#Q4. 
M=Polynome([1,3])
M[42]=5
N=Polynome([-2,3,0,0,0,0,0,0,0,0,0,0,42])

M%N
#-5/2744*X**9 + 5/1372*X**8 - 5/2058*X**7 + 5/9261*X**6 + 3*X + 1

#Q5. P est le polynome nul si P.lead renvoie 0.

def binomial(k, n):
    """ Renvoie le coefficient binomial "k parmi n"... en 1 seule ligne !
        (indication: (X+1)^n )
    """
    P = (Polynome ([1,1]))**n  #on utilise le binome de Newton
    return P[k]
    
binomial (10,15)



def eval_poly(P,x):
    """ Renvoie P(x).
     
    Entrées:
        P: polynôme
        x: nombre
         
    Algorithme: si vous ne voulez pas vous embêter, utilisez la formule brutale,
    qui consiste à faire la somme des a_i x^i.
    Si vous voulez être un peu plus efficace, utilisez l'algorithme 
    "d'Hörner" pour réduire le nombre
    de multiplications pour avoir x**n. Par exemple, si P = aX^3 + bX^2 + cX +d,
    on calcule P(x) grâce à:
        P(x) = d + x (c + x (b + a x)))
    (on commence donc le calcul par le terme de plus haut degré).
     
    Exemples:
        >>> X = Polynome([0,1])
        >>> eval_poly(5*X**2 + 1, 0)
        1
        >>> eval_poly(5*X**2 + 1, 1)
        6
        >>> eval_poly(5*X**2 + 1, 2)
        21
        >>> eval_poly(5*X**2 + 1, 3)
        46
    """
    S=0
    n=P.deg
    for i in range (n+1):
        S=S+P[i]*(x**i)
    return S
    
P = Polynome([1,0,5])    
eval_poly(P,0)
eval_poly(P,1)
eval_poly(P,2)
eval_poly(P,3)



def derivative(P):
    """ Renvoie le polynôme dérivé de P.
     
    Exemples:
        >>> X = Polynome([0,1])
        >>> derivative(X**2)
        2*X
        >>> derivative(5*X**3 - 6*X +3)
        15*X**2 - 6
    """
    P_derive=Polynome([0])
    n=P.deg
    for i in range (n,0,-1):
        P_derive[i-1]=i*P[i]
    return P_derive
     
X=Polynome([0,1])
derivative(X**2)
derivative(5*X**3 - 6*X +3)




def sturm_sequence(P):
    """ Renvoie la suite de Sturm de P sous forme de liste [P_0, P_1, ..., P_m].
     
    La suite de Sturm est définie par (l'expression "A%B" désigne le reste de la
    division euclidienne de A par B):
    P_0 = P
    P_1 = P'
    P_{k+2} = - P_{k} % P_{k+1}, pour k entier naturel.
    Le dernier terme P_m est tel que P_{m-1} % P_m = 0.
     
    Exemple:
        >>> P = Polynome([-1, 9, -6, 1])
        >>> sturm_sequence(P)
        [X**3 - 6*X**2 + 9*X - 1, 3*X**2 - 12*X + 9, 2*X - 5, 9/4]
    """
    a=P
    b=derivative(P)
    l=[a,b]
    while b.deg!=0:
        a,b=b,-(a%b)
        l.append(b)
    return l
    
P=Polynome([-1,9,-6,1])
sturm_sequence(P)
        
     
         


