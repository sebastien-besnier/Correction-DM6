# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 16:58:42 2015

@author: Sophie
"""

"Blondeau Damien"    "DM6"

################################################################################
#        Programmation des fonctions intervenant sur lespolynomes              #
################################################################################

from numbers import Number
from fractions import Fraction
class Polynome:
    """ WARNING : this class is written for educational purpose; the algorithms
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
#                           Réponses au questions                              #
################################################################################
    
    
" 0. Quel polynôme est construit par l'instruction Polynome([0,1,2,3])?"
#Le polynome construit construit par l'instruction Polynome([0,1,2,3]) est 
#3*X**3+2*X**2+X


""" 1. Construire le polynôme X^52 + 3X^2 +1 (plusieurs lignes peuvent 
       être nécessaires)."""
P=Polynome([1,0,3])
P[52]=1
print P      

 
" 2. Donner 2 moyens de connaître le coefficient dominant d'un polynôme P"
#On peut utiliser la fonction P.lead ou alors P[P.deg] pour afficher le 
#coefficient dominant

"3. Comment accéder au terme constant d'un polynôme P?"
# Il sufit de rentrer P[0] dans la console

" 4. Calculer le reste de la division de 5X^42 + 3X+1 par 42 X^12 +3X-2."
P=Polynome([1,3])
P[42]=5
D=Polynome([-2,3])
D[12]=42
reste=P%D
print reste
#le reste est -5/2744*X**9 + 5/1372*X**8 - 5/2058*X**7 + 5/9261*X**6 + 3*X + 1

" 5. Si P est un polynôme, comment tester que P est le polynôme nul?"  
#Pour tester que P est le Polynome nul il suffit de demanderle degré de P
#Si ce dégré est égaleà -1, alors il s'agit du polynome nul


################################################################################
#                        Programmation des fonctions                           #
################################################################################  

def binomial(k, n):
    """ Renvoie le coefficient binomial "k parmi n"... en 1 seule ligne !
        (indication: (X+1)^n )
            """
    P=Polynome([1,1])**n
    return int(P[k]) 
    

def eval_poly(P, x):
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
    i=1
    n=int(P.deg)
    s=P[n]
    while n-i>=0:
     s=s*x+P[n-i]
     i=i+1
    return int(s)    

def derivative(P):
    """ Renvoie le polynôme dérivé de P.
    
    Exemples:
        >>> X = Polynome([0,1])
        >>> derivative(X**2)
        2*X
        >>> derivative(5*X**3 - 6*X +3)
        15*X**2 - 6
    """
    for i in range (P.deg):
        P[i]=P[i+1]*(i+1)
    P[P.deg]=0
    return P  

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
        [X**3 - 6*X**2 + 9*X - 1, 3*X**2 - 12*X + 9, 2*X - 5, 9/4]"""
    import copy
    A=copy.deepcopy(P)
    l=[1]*(int(P.deg)+2)
    l[0]=A
    l[1]=derivative(P) 
    for i in range(A.deg): # On choisit d'effectuer une boucle for, en effet a 
     l[i+2]=-l[i]%l[i+1] # chaque itération de la suite de sturm le dégré 
     if l[i+2]==0:         # diminue ainsi il y aura au maximum un nombre 
      return l[0:i+2]      # d'itération égal au degré du polynome initial
    return l     

P = Polynome([-1, 9, -6, 1])
sturm_sequence(P)

   



    
    
