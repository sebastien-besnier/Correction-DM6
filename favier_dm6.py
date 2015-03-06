# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 17:40:00 2015

@author: Laïta
"""
from numbers import Number
from fractions import Fraction
class Polynome:
    """ WARNING : this class is written for educational purpose; the algorithms
    used are unefficient with polynomials of high degree. Consider a real
    lib if you have to deal with big polynomials.
    """
    
    def __init__(self, coeffs):
        """ Construit un polynÃ´me Ã  partir d'une liste de coefficients.
        
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
            raise ValueError("l'indice doit Ãªtre positif")
        
        if i <= self.deg:
            return self._coeffs[i]
        else:
            return 0
    
    def __setitem__(self,i, coeff):
        """Modifie le coefficient devant x^i. Lance une erreur si i < 0.
        Met le degrÃ© Ã  jour si besoin."""
        if i < 0:
            raise ValueError("l'indice doit Ãªtre positif")

        n = len(self._coeffs)
        self._coeffs.extend([0] * (i-n +1))
        self._coeffs[i] = coeff
        if i > self._deg and coeff != 0:
            self._deg = i
        elif i == self.deg and coeff == 0:
            self._compute_deg(i-1)

    def _compute_deg(self, dmax):
        """ Met Ã  jour le veritable degrÃ© du polynÃ´me en ignorant les 0 en fin
        de liste, en supposant que tous les Ã©lÃ©ments de self._coeffs sont
        nuls aux indices supÃ©rieurs strictement Ã  dmax."""
        while dmax >= 0 and self._coeffs[dmax] == 0:
            dmax -= 1
        self._deg = dmax

    def __add__(self, p2):
        """ Renvoie la somme de self et p2. p2 peut Ãªtre un polynÃ´me ou un 
        nombre (hÃ©rite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut additionner un polynÃ´me"
                             "qu'avec un nombre ou un polynÃ´me")
                             
        deg = max(self.deg, p2.deg)
        coeffs = [0] * (deg +1)
        for i in range(deg + 1):
            coeffs[i] = self[i] + p2[i]
        return Polynome(coeffs)
    
    __radd__ = __add__
    
    def __sub__(self, p2):
        """ Renvoie la diffÃ©rence de self et p2. p2 peut Ãªtre un polynÃ´me ou un 
        nombre (hÃ©rite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut soustraire un polynÃ´me"
                             "qu'avec un nombre ou un polynÃ´me")
                             
        deg = max(self.deg, p2.deg)
        coeffs = [0] * (deg + 1)
        for i in range(deg + 1):
            coeffs[i] = self[i] - p2[i]
        return Polynome(coeffs)
    
    def __rsub__(self, p2) : 
        """ Renvoie la diffÃ©rence de p2 et self. p2 peut Ãªtre un polynÃ´me ou un 
        nombre (hÃ©rite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut soustraire un polynÃ´me"
                             "qu'avec un nombre ou un polynÃ´me")
                             
        deg = max(self.deg, p2.deg)
        coeffs = [0] * (deg +1)
        for i in range(deg + 1):
            coeffs[i] = p2[i] - self[i]
        return Polynome(coeffs)
        
    def __neg__(self):
        """Renvoie le polynÃ´me opposÃ© de self."""
        return Polynome([-c for c in self._coeffs])
    
    def __mul__(self, p2):
        """ Renvoie le produit de self et p2. p2 peut Ãªtre un polynÃ´me ou un 
        nombre (hÃ©rite de Number)."""
        if isinstance(p2, Number):
            p2 = Polynome([p2])
        elif not isinstance(p2, Polynome):
            raise ValueError("on ne peut multiplier un polynÃ´me"
                             "qu'avec un nombre ou un polynÃ´me")
        
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
                             "dÃ©finies")
                             
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
            raise ValueError("on ne peut diviser un polynÃ´me"
                             "qu'avec un nombre ou un polynÃ´me")
        
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
        """ Renvoie une reprÃ©sentation textuelle du monome de degrÃ© d de self.
            Si debut est Ã  True et le coefficient est positif, il n'y aura pas
            de signe "+" au dÃ©but de la chaÃ®ne de caractÃ¨res.
            Si debut est Ã  False, il y aura toujours un signe "+" ou "-" devant
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
        """ Renvoie une reprÃ©sentation textuelle de P."""
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
        
        Si self est un produit de polynomes irrÃ©ductibles P_i Ã  une certaine
        puissance, le radical de self est le produit des P_i Ã  la puissance
        1."""
        t = Polynome([i*c for i, c in enumerate(self._coeffs)])
        return self // self.gcd(t)

    __repr__ = __str__

P=Polynome([0,1])
O=P**42
O[42]=5
X=Polynome([0,1])
I=X**12
I[12]=42
(O+Polynome([1,3]))%(I+Polynome([-2,3]))




################################################################################
#                                                                              #
#                       REPRENDRE LA LECTURE !                                 #
#                                                                              #
################################################################################

# Questions prÃ©liminaires, pour Ãªtre sÃ»r d'avoir bien compris comment utiliser
# les polynÃ´mes:
# 0. Quel polynÃ´me est construit par l'instruction Polynome([0,1,2,3])
##3X^3+2X^2+X
# 1. Construire le polynÃ´me X^52 + 3X^2 +1 (plusieurs lignes peuvent 
#    Ãªtre nÃ©cessaires).
##P=Polynome([0,1])
##O=P**52
##O+Polynome([1,0,3])
# 2. Donner 2 moyens de connaÃ®tre le coefficient dominant d'un polynÃ´me P
##P.lead et P[P.deg]
# 3. Comment accÃ©der au terme constant d'un polynÃ´me P?
##P[0]
# 4. Calculer le reste de la division de 5X^42 + 3X+1 par 42 X^12 +3X-2.
##P=Polynome([0,1])
##O=P**42
##O[42]=5
##X=Polynome([0,1])
##I=X**12
##I[12]=42
##(O+Polynome([1,3]))%(I+Polynome([-2,3]))
# 5. Si P est un polynÃ´me, comment tester que P est le polynÃ´me nul?
##P est nul ssi: P.deg==0 et P[0]==0 => Non, si P.deg==0, alors P[0]!=0.

# Consigne: Ã©crire le corps des fonctions donnÃ©es. Laisser la docstring
# (la chaine de caractÃ¨res sous la fonction la documentant). TESTER ABONDAMMENT
# CHAQUE FONCTION APRÃˆS L'AVOIR Ã‰CRITE ! Exemple:

# AVANT votre passage:
def quarante_deux_fois(x):
    """Renvoie la multiplication de 42 par x."""
    return 0
    
# APRÃˆS votre passage:
def quarante_deux_fois(x):
    """Renvoie la multiplication de 42 par x."""
    res = 0
    for i in range(9):
        for j in range(5):
            res += x
    return res - x - x - x
# Ã‰videmment, il y a mieux pour Ã©crire cette fonction....

# Sauf mention explicite dans la documentation, les fonctions ne modifient pas
# leurs arguments. De plus, lorsque la documentation d'une fonction indique que 
# ses arguments sont d'un certain type, on fera confiance Ã  l'utilisateur et
# on ne vÃ©rifiera pas les types. 

# Les fonctions obligatoires pour le DM sont : bin, eval_poly, derivative et
# sturm_sequence. Vous m'enverrez le fichier Ã  l'adresse 
#                   monsieurbesnier@gmail.com
# avant mardi soir, 19h, cachet du mail faisant foi. Vous nommerez votre fichier
# "nom_prenom_dm6.py" (sans accent, ni espaces ni caractÃ¨res spÃ©ciaux). Par 
# exemple pour moi ce serait "sebastien_besnier_dm6.py"

# Avis aux Ã©lÃ¨ves tentÃ©s de faire un copier/coller sauvage Ã  partir du code du
# voisin, pour aprÃ¨s changer quelques noms de variables : cela se repÃ¨re 
# extrÃ¨mement facilement. Il y a mÃªme des outils qui font Ã§a automatiquement. Et 
# ils fonctionnent trÃ¨s bien.

# Just for fun, sans lien avec la suite
def binomial(k, n):
    """ Renvoie le coefficient binomial "k parmi n"... en 1 seule ligne !
        (indication: (X+1)^n )
    """
    P=Polynome([1,1])**n
    return P[k] #1ligne?
    

def eval_poly(P, x):
    """ Renvoie P(x).
    
    EntrÃ©es:
        P: polynÃ´me
        x: nombre
        
    Algorithme: si vous ne voulez pas vous embÃªter, utilisez la formule brutale,
    qui consiste Ã  faire la somme des a_i x^i.
    Si vous voulez Ãªtre un peu plus efficace, utilisez l'algorithme 
    "d'HÃ¶rner" pour rÃ©duire le nombre
    de multiplications pour avoir x**n. Par exemple, si P = aX^3 + bX^2 + cX +d,
    on calcule P(x) grÃ¢ce Ã :
        P(x) = d + x (c + x (b + a x)))
    (on commence donc le calcul par le terme de plus haut degrÃ©).
    
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
    s=0
    for i in range ((P.deg)+1):
        s=s+P[i]*x**i
    return s
    
eval_poly(5*X**2+1,3)

def derivative(P):
    """ Renvoie le polynÃ´me dÃ©rivÃ© de P.
    
    Exemples:
        >>> X = Polynome([0,1])
        >>> derivative(X**2)
        2*X
        >>> derivative(5*X**3 - 6*X +3)
        15*X**2 - 6
    """
    s=Polynome([0])
    X=Polynome([0,1])
    for i in range (1,(P.deg) +1):
        s=s+P[i]*i*X**(i-1)
    return s

derivative(X**2)    
derivative(5*X**3 - 6*X +3)

def sturm_sequence(P):
    """ Renvoie la suite de Sturm de P sous forme de liste [P_0, P_1, ..., P_m].
    
    La suite de Sturm est dÃ©finie par (l'expression "A%B" dÃ©signe le reste de la
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
    P_0=P
    P_1=derivative(P)
    L=[P,derivative(P)]
    if ((P_0%P_1))!=0:
        P_0,P_1=P_1,-(P_0%P_1)
        L.append(P_1)
    else: return L
    return L
sturm_sequence(Polynome([-1, 9, -6, 1]))  
        
# Conclusion : bien.
def nb_change_sign_at(polys, x):
    """ Calcule le nombre de changements de signes lorsqu'on Ã©value les 
    polynomes dans polys en x. Un zÃ©ro n'est pas considÃ©rÃ© comme un changement
    de signe.
    
    EntrÃ©es:
        polys: liste de polynÃ´mes
        x: un nombre.
    
    Exemple:
        >>> X = Polynome([0, 1])
        >>> nb_change_sign_at([X, X**2+1, X+2], -1)
        1  # on a "-1, 2, 1" soit la chaÃ®ne de signes "-++", donc 1 changement
        >>> nb_change_sign_at([X, X**2+1, X-2], -1)
        2 # on a "-1, 2, -3" soit la chaÃ®ne de signes "-+-", donc 2 changements
        >>> nb_change_sign_at([X**2 + 1, X - 2, -X], 2)
        1 # on a "3, 0, -2" soit la chaÃ®ne de signes "+0-", donc 1 changement
    """
    return 0


def nb_roots_between(polys, a, b):
    """ Renvoie le nombre de racines du premier polynÃ´me de polys sur le
    segment ]a,b[, quand polys est une suite de Sturm.
    
    EntrÃ©es:
        polys: une liste de polynÃ´mes, plus exactement, polys est la suite de
            Sturm de polys[0];
        a: un nombre;
        b: un nombre strictement plus grand que a.
    """
    return 0


def roots_range(P):
    """ Renvoie un nombre M > 0 tel que toutes les racines de P soient dans 
    l'intervalle [-M, M].
    
    Indication: voir exercice 21 du chapitre sur les polynÃ´mes (attention,
    dans l'exercice 21, le polynÃ´me est supposÃ© unitaire).
    """
    return 0
    
def nb_roots(polys):
    """ Renvoie le nombre de racines rÃ©elles du premier polynÃ´me de polys,
    quand polys est une suite de Sturm.
    
    EntrÃ©es:
        polys: une liste de polynÃ´mes, plus exactement, polys est la suite de
            Sturm de polys[0].
    """
    return 0

def find_root(P, a, b, eps):
    """ Trouve une racine de p dans [a,b[, sachant que p(a) * p(b) <= 0.
    Renvoie une approximation de la racine Ã  eps prÃ¨s.

    Algorithme : utiliser une dichotomie.
    """
    return 0


def isolate_roots(P):
    """ Renvoie une liste de nombres [x_0, x_1, ..., x_n]
    rangÃ©s dans l'ordre croissant telle qu'il existe une unique racine de P 
    entre chaque x_i et x_{i+1}. 
    
    Cette fonction est dÃ©jÃ  implÃ©mentÃ©e et fonctionnera
    correctement sous rÃ©serve que toutes les fonctions ci-dessus sont 
    correctement implÃ©mentÃ©es.
    """
    polys = sturm_sequence(P)
    M = 2*roots_range(P)
    
    def loop(a, b, n_prev):
        """Renvoie une liste [c_0, c_1, ..., c_m] telle que chaque intervalle de
        la liste [a, c_0, c_1, ..., c_m, b] contienne exactement une racine de
        P. n_prev contient le nombre de racines de P entre a et b."""
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
    """ Renvoie la liste des racines de P avec une prÃ©cision eps.
    On pourra calculer le radical de P, qui a mÃªme racines que P mais qui n'a
    pas de facteurs carrÃ©s; pour cela, on peut tout simplement utiliser
    P.square_free().
    """
    return 0
