# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 09:43:42 2015

@author: Guillaume
"""
# 0. Quel polynôme est construit par l'instruction Polynome([0,1,2,3])
# 1. Construire le polynôme X^52 + 3X^2 +1 (plusieurs lignes peuvent
#    être nécessaires).
# 2. Donner 2 moyens de connaître le coefficient dominant d'un polynôme P
# 3. Comment accéder au terme constant d'un polynôme P?
# 4. Calculer le reste de la division de 5X^42 + 3X+1 par 42 X^12 +3X-2.
# 5. Si P est un polynôme, comment tester que P est le polynôme nul?



#1) on a le polynome 3X**3+2X**2+X
#2) on peut utiliser P.deg (=> bof) ou ???
#3) on tape P([0])
#P=Polynome([0])
#P[42]=5
#P[1]=3
#P[0]=1
#R=Polynome([0])
#R[12]=42
#R[1]=3
#R[0]=-2
#P%R
#-5/2744*X**9 + 5/1372*X**8 - 5/2058*X**7 + 5/9261*X**6 + 3*X + 1
#5) on utilise P.deg si on a - alors on a le polynome nul ou si P.lead=0



def binomial(k,n):
    P=Polynome([1,1])
    P=P**n
    return P[k] # 1 ligne ?
binomial(2,5)
#10

P=Polynome([1,1,1,1,1])
def derivative(P):
    Q=Polynome([])
    for i in range(P.deg+1): 
        Q[i]=P[i+1]*(i+1)
        Q.deg=i-1 # Ce n'est pas à toi de t'occuper de ça.
    return Q
derivative(P)
   #4*X**3 + 3*X**2 + 2*X + 1
 
 P=Polynome([7,-3,1,0,1])   
def eval_polynome(P,x):
    c=0
    for i in range (P.deg+1):
        c+=P[i]*x**i
    return c
eval_polynome(P,2)
#21

def sturm_sequence(Q):
    R=derivative(Q)
    l=[Q,R]
    i=1
    while not (l[i-1]%l[i])==0 :
        l.append(-l[i-1]%l[i])
        i=i+1
    return l
    
# Travail correct, dommage que tu ne respectes pas le format (docstrings manquantes).
P=Polynome([2,-3,-1,0,1]) 
sturm_sequence(P)
#[X**4 - X**2 - 3*X + 2, 4*X**3 - 2*X - 3, 1/2*X**2 + 9/4*X - 2, -95*X + 75, -127/1444]
P = Polynome([-1, 9, -6, 1])
sturm_sequence(P)
#[X**3 - 6*X**2 + 9*X - 1, 3*X**2 - 12*X + 9, 2*X - 5, 9/4]
