# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 21:27:27 2015

@author: amy
"""
#DM6 "Les Polynomes"

#Q0:

#P = Polynome([0, 1, 2, 3]) affiche:
#3*X**3 + 2*x**2 + 1

#Q1:

def Polynome(X):
    P = Polynome([1, 3, 1])
    while P.deg==52:
        P = X**52 + 3*X**2 + 1
    return P

#Q2:

#Soit P un polynome
#1er moyen:
#faire P.lead
#2e moyen: faire
def coeff(P, X, i):     # coeff=coefficient dominant
    while P.deg==i:
        coeff=P[i]      # le coefficient devant X**i
    return coeff

#Q3:

#Pour accéder au terme constant d'un polynome P,
#c'est àdire le coefficient devant X**0 il faut
#faire P[0] ou faire:
def term(P, X, i):        # terme constant
    while P.deg==0:
        term=P[0]
    return term

#Q4:

def Reste (P, Q, X):   #Reste=polynome restant de la division euclidienne de P par Q
    P = 5*X**42 + 3*X + 1
    Q = 42*X**12 + 3*X - 2
    while Reste.deg<Q.deg:
        R=P % Q
    return R

#Q5:

def Polynome_nul(P, n, X):
    while P[n]==0:     #coefficients devant X**n
        P = 0
    return Polynome_nul


