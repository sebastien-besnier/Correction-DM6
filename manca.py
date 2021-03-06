# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 12:58:44 2015

@author: nicolas# Tu te foutterais pas un peu de ma gueule là par hasard ?
"""

La classe Polynome sert à manipuler simplement des polynômes. Voici quelques
exemples d utilisation (les ">>>" indiquent que la ligne est une commande 
passée à l interpréteur Python, les autres lignes sont les réponses de
Python):
 
Création: en donnant la liste des coefficients 
=========
    >>> P = Polynome([1, 0, 5])
    >>> P
    5*X**2 + 1
    >>> X = Polynome([0, 1])
    >>> X**n
    X**n
     
Accès et modification :
=======================
    >>> P = Polynome([1, 0, 5])
    >>> P[2] # le coefficient devant X^2
    5
    >>> P[3] # le coefficient devant X^3 (il n'y en a pas)
    0
    >>> P[0] # le terme constant
    1
    >>> P.lead # lead pour leader : le coefficient dominant de P
    5
    >>> P.deg # le degré de P
    2
    >>> P[2] = 4 # on change le coefficient devant X^2
    >>> P
    4X^2 + 1
    >>> P[5] = 3 # on rajoute un coefficient
    >>> P
    3*X**5 + 4X**2 + 1
    >>> P.deg # le degré est-il bien mis à jour ?
    5 # oui !
    >>> P.lead
    3
 
/!\ Un polynôme ressemble à une liste, mais n est pas une liste ! En particulier
‾‾‾ les méthodes "append" et "len" ne s appliquent pas à un polynôme.
 
Opérations algébriques : tout ce que vous révez de faire avec des polynômes
========================
 
    >>> P = Polynome([1, 0, 5])
    >>> P * P
    25*X**4 + 10*X**2 + 1
    >>> P + 5
    5*X**2 + 6
    >>> P ** 3 # puissance
    125*X**6 + 75*X**4 + 15*X**2 + 1
    >>> (P * P) // (P + 5) # quotient de la division euclidienne
    5*X**2 - 4
    >>> (P * P) % (P + 5) # reste de la division euclidienne
    25
    >>> X = Polynome([0,1])
    >>> (5*X**2 - 4) * (P + 5) + 25 - (P* P) # vérification
    0 # youpi !
"""
 
################################################################################
#           IGNOREZ LES LIGNES SUIVANTES JUSQU'AU PROCHAIN                     #
#                   ENCART VOUS INVITANT À LIRE                                #
################################################################################
"""
from numbers import Number
from fractions import Fraction
class Polynome:
    """
    WARNING : this class is written for educational purpose; the algorithms
    used are unefficient with polynomials of high degree. Consider a real
    lib if you have to deal with big polynomials.
    """
     
    def __init__(self, coeffs):
        """ Construit un polynôme à partir d'une liste de coefficients.
         
        coeffs: liste des coefficients, le terme constant est dans coeffs[0],
            le terme en X est dans coeffs[1], ...
        """
        self._coeffs = [Fraction(c) for c in coeffs]
        self._compute_deg(len(coeffs)-1)
     
    @property
    def deg(self):
        return self._deg
 
    @property
    def lead(self):
        "Renvoie le coefficient dominant de self (0 si self.deg < 0)"
        if self.deg < 0:
            return 0
        return self[self.deg]
 
    def __getitem__(self, i):
        """Renvoie le coefficient devant x^i. Lance une erreur si i < 0, renvoie
         0 si i > deg."""
        if i < 0:
            raise ValueError("l'indice doit être positif")
         
        if i <= self.deg:
            return self._coeffs[i]
        else:
            return 0
     
    def __setitem__(self,i, coeff):
        """Modifie le coefficient devant x^i. Lance une erreur si i < 0.
        Met le degré à jour si besoin."""
        if i < 0:
            raise ValueError("l'indice doit être positif")
 
        n = len(self._coeffs)
        self._coeffs.extend([0] * (i-n +1))
        self._coeffs[i] = coeff
        if i > self._deg and coeff != 0:
            self._deg = i
        elif i == self.deg and coeff == 0:
            self._compute_deg(i-1)
 
    def _compute_deg(self, dmax):
        """ Met à jour le veritable degré du polynôme en ignorant les 0 en fin
        de liste, en supposant que tous les éléments de self._coeffs sont
        nuls aux indices supérieurs strictement à dmax."""
        while dmax >= 0 and self._coeffs[dmax] == 0:
            dmax -= 1
        self._deg = dmax
 
    def __add__(self, p2):
        """ Renvoie la somme de self et p2. p2 peut être un polynôme ou un 
        nombre (hérite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut additionner un polynôme"
                             "qu'avec un nombre ou un polynôme")
                              
        deg = max(self.deg, p2.deg)
        coeffs = [0] * (deg +1)
        for i in range(deg + 1):
            coeffs[i] = self[i] + p2[i]
        return Polynome(coeffs)
     
    __radd__ = __add__
     
    def __sub__(self, p2):
        """ Renvoie la différence de self et p2. p2 peut être un polynôme ou un 
        nombre (hérite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut soustraire un polynôme"
                             "qu'avec un nombre ou un polynôme")
                              
        deg = max(self.deg, p2.deg)
        coeffs = [0] * (deg + 1)
        for i in range(deg + 1):
            coeffs[i] = self[i] - p2[i]
        return Polynome(coeffs)
     
    def __rsub__(self, p2) : 
        """ Renvoie la différence de p2 et self. p2 peut être un polynôme ou un 
        nombre (hérite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut soustraire un polynôme"
                             "qu'avec un nombre ou un polynôme")
                              
        deg = max(self.deg, p2.deg)
        coeffs = [0] * (deg +1)
        for i in range(deg + 1):
            coeffs[i] = p2[i] - self[i]
        return Polynome(coeffs)
         
    def __neg__(self):
        """Renvoie le polynôme opposé de self."""
        return Polynome([-c for c in self._coeffs])
     
    def __mul__(self, p2):
        """ Renvoie le produit de self et p2. p2 peut être un polynôme ou un 
        nombre (hérite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut multiplier un polynôme"
                             "qu'avec un nombre ou un polynôme")
         
        deg = self.deg + p2.deg
        coeffs = [0] * (deg + 1)
        for i in range(self.deg + 1):
            for j in range(p2.deg + 1):
                coeffs[i+j] += self._coeffs[i] * p2._coeffs[j]
        return Polynome(coeffs)
     
    __rmul__ = __mul__
     
    def __pow__(self, n):
        """ Renvoie self**n. """
        if n < 0:
            raise ValueError("seule les puissances entieres positives sont"
                             "définies")
                              
        res = Polynome([1])
        for i in range(n):
            res *= self
        return res
     
    def __eq__(self, p2):
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            return False
        if self.deg < 0 and p2.deg < 0:
            return True
         
        return ( self.deg == p2.deg and
                 self._coeffs[:p2.deg + 1] == p2._coeffs[:p2.deg + 1])
             
    def quo_rem(self, p2):
        """Renvoie le quotient et le reste de la division euclidienne de
        self par p2."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut diviser un polynôme"
                             "qu'avec un nombre ou un polynôme")
         
        if p2.deg < 0:
            raise ValueError("impossible de diviser par 0")
 
        x = Polynome([0,1])
        q = Polynome([0] * (self.deg - p2.deg))
        r = Polynome(self._coeffs[:self.deg + 1])
        while r.deg >= p2.deg:
            coeff = r.lead / p2.lead
            deg = r.deg - p2.deg
            xd = x**deg
            q += coeff * xd
            r -= coeff * xd * p2
        return q, r
         
    def __mod__(self, p2):
        return self.quo_rem(p2)[1]
     
    def __floordiv__(self, p2):
        return self.quo_rem(p2)[0]
         
     
    def _monome_to_str(self, d, debut):
        """ Renvoie une représentation textuelle du monome de degré d de self.
            Si debut est à True et le coefficient est positif, il n'y aura pas
            de signe "+" au début de la chaîne de caractères.
            Si debut est à False, il y aura toujours un signe "+" ou "-" devant
            le monome.
            Si le coefficient est nul, renvoie la chaine vide.
        """
        coeff = self[d]
        if coeff == 0:
            return ""
                     
        if coeff > 0:
            if debut:
                signe =""
            else:
                signe = " + "
        else:
            coeff *= -1
            if debut:
                signe = "-"
            else:
                signe = " - "
         
        if d == 0:
            res = signe + str(coeff)
        else:
            if coeff == 1:
                res = signe + "X"
            else:
                res = signe + str(coeff) + "*X"
             
            if d > 1:
                res += "**" + str(d)
        return res    
     
    def __str__(self):
        """ Renvoie une représentation textuelle de P."""
        if self.deg < 0:
            return "0"
     
        s = self._monome_to_str(self.deg, True)
        for i in range(self.deg - 1, -1, -1):
            s += self._monome_to_str(i, False)
        return s
       
    def gcd(self, p2):
        """ Renvoie le pgcd de self et p2."""
        if p2.deg < 0:
            return self
        if self.deg < p2.deg:
            return p2.gcd(self)
         
        return p2.gcd(self % p2)
         
    def square_free(self):
        """ Renvoie le radical de self.
         
        Si self est un produit de polynomes irréductibles P_i à une certaine
        puissance, le radical de self est le produit des P_i à la puissance
        1."""
        t = Polynome([i*c for i, c in enumerate(self._coeffs)])
        return self // self.gcd(t)
 
    __repr__ = __str__
 
 
################################################################################
#                                                                              #
#                       REPRENDRE LA LECTURE !                                 #
#                                                                              #
################################################################################
 
# Questions préliminaires, pour être sûr d'avoir bien compris comment utiliser
# les polynômes:
# 0. Quel polynôme est construit par l'instruction Polynome([0,1,2,3])
# 1. Construire le polynôme X^52 + 3X^2 +1 (plusieurs lignes peuvent 
#    être nécessaires).
# 2. Donner 2 moyens de connaître le coefficient dominant d'un polynôme P
# 3. Comment accéder au terme constant d'un polynôme P?
# 4. Calculer le reste de la division de 5X^42 + 3X+1 par 42 X^12 +3X-2.
# 5. Si P est un polynôme, comment tester que P est le polynôme nul?
 
# Consigne: écrire le corps des fonctions données. Laisser la docstring
# (la chaine de caractères sous la fonction la documentant). TESTER ABONDAMMENT
# CHAQUE FONCTION APRÈS L'AVOIR ÉCRITE ! Exemple:
 
# AVANT votre passage:
def quarante_deux_fois(x):
    """Renvoie la multiplication de 42 par x."""
    return 0
     
# APRÈS votre passage:
def quarante_deux_fois(x):
    """Renvoie la multiplication de 42 par x."""
    res = 0
    for i in range(9):
        for j in range(5):
            res += x
    return res - x - x - x
# Évidemment, il y a mieux pour écrire cette fonction....
 
# Sauf mention explicite dans la documentation, les fonctions ne modifient pas
# leurs arguments. De plus, lorsque la documentation d'une fonction indique que 
# ses arguments sont d'un certain type, on fera confiance à l'utilisateur et
# on ne vérifiera pas les types. 
 
# Les fonctions obligatoires pour le DM sont : bin, eval_poly, derivative et
# sturm_sequence. Vous m'enverrez le fichier à l'adresse 
#                   monsieurbesnier@gmail.com
# avant mardi soir, 19h, cachet du mail faisant foi. Vous nommerez votre fichier
# "nom_prenom_dm6.py" (sans accent, ni espaces ni caractères spéciaux). Par 
# exemple pour moi ce serait "sebastien_besnier_dm6.py"
 
# Avis aux élèves tentés de faire un copier/coller sauvage à partir du code du
# voisin, pour après changer quelques noms de variables : cela se repère 
# extrèmement facilement. Il y a même des outils qui font ça automatiquement. Et 
# ils fonctionnent très bien.
 
# Just for fun, sans lien avec la suite
def binomial(k,n):
    P=(Polynome([1,1]))**n
    return P[k]

def eval_poly(P,x):
    r=P.lead
    for i in range(P.deg-1,-1,-1):
        r=r*x+P[i]
    return r
 
def derivative(P):
    r=0
    for i in range ((P.deg)+1):
        r+=P[i]*x**i
    return r
    
 
def sturm_sequence(P):
    P1=P
    P2=derivative(P)
    L=[P1,P2]
    while P2.deg!=0:
        P1=P2
        P2=-(P1%P2)
        L.append(P2)
    return L
     
         
