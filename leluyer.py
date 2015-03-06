# -*- coding: utf-8 -*-
"""
La classe Polynome sert à manipuler simplement des polynômes. Voici quelques
exemples d'utilisation (les ">>>" indiquent que la ligne est une commande 
passée à l'interpréteur Python, les autres lignes sont les réponses de
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

/!\ Un polynôme ressemble à une liste, mais n'est pas une liste ! En particulier
‾‾‾ les méthodes "append" et "len" ne s'appliquent pas à un polynôme.

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
#                                                                              #
#                       REPRENDRE LA LECTURE !                                 #
#                                                                              #
################################################################################

# Questions préliminaires, pour être sûr d'avoir bien compris comment utiliser
# les polynômes:
# 0. Quel polynôme est construit par l'instruction Polynome([0,1,2,3])
"0 + x + 2x^2 + 3x^3"

# 1. Construire le polynôme X^52 + 3X^2 +1 (plusieurs lignes peuvent 
#    être nécessaires).
def construirepolynomebizare(d,D):
    x=1
    p=Polynome([1]) #on ajoute le terme constant = 1
    while x<=d:     
        p[x]=0      #tout les termes de degré inférieur au degré du polynome ont
                    #des facteurs nuls
        x+=1
    p[d]=D          #on ajoute le coefficient dominant
    return p

"ici, p = X^52 + 3X^2 + 1 "
"p = construirepolynomebizare(52,1)"
"p[2]=3"


# 2. Donner 2 moyens de connaître le coefficient dominant d'un polynôme P
"utiliser la fonction lead"
"utiliser la fonction P.deg puis éxécuter P[P.deg]"
    
# 3. Comment accéder au terme constant d'un polynôme P?
"faire P[0]"

# 4. Calculer le reste de la division de 5X^42 + 3X+1 par 42X^12 +3X-2.
P,p=construirepolynomebizare(42,5),construirepolynomebizare(12,42)
P[1],P[0],p[1],p[0]=3,1,3,(-2)
P%p
"à executer ligne par ligne"

# 5. Si P est un polynôme, comment tester que P est le polynôme nul?
"utiliser dans un 1er temps la fonction deg puis vérifier P[0]=0"

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
def binomial(k, n):
    """ Renvoie le coefficient binomial "k parmi n"... en 1 seule ligne !
        (indication: (X+1)^n )
    """
    p=Polynome([1,1])**n
    return p[k]
    #ce programme fonctionne mais il renvoie le resultat sous forme de fraction..."
    

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
    #Methode Brutale:
    S=0
    for i in range(1,P.deg+1):
        S=S+P[i]*x**i
    return S+P[0]

p=Polynome([1,0,5])
eval_poly(p, 3)

def derivative(P):
    """ Renvoie le polynôme dérivé de P.
    
    Exemples:
        >>> X = Polynome([0,1])
        >>> derivative(X**2)
        2*X
        >>> derivative(5*X**3 - 6*X +3)
        15*X**2 - 6
    """
    p=Polynome([])                  #p sera la dérivé de P
    for i in range(1,P.deg+1):      #permet "d'isoler" chaque terme du polynome
        p[i-1]=P[i]*i               #un terme de degré i donne un terme de 
    return p                        #degré (i-1), son facteur est multiplié 
                                    #par ce degré

P=Polynome([3,(-6),0,5])
derivative(P)

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


    P_0=P
    P_1=derivative(P)    
    Sturm=[P_0,P_1]    
    while P_1.deg>=1:           #le programme s'arrête à l'optention de P_m=cste
        P_1=-(P_0%P_1)          #effectue l'opération de la suite de Sturm
        Sturm.append(P_1)       #ajoute ce calcul à la suite de Sturm
        P_0=Sturm[len(Sturm)-2] #on reprend l'avant dernier terme de la suite
        P_1=Sturm[len(Sturm)-1] #on reprend le dernier terme de la suite
    return Sturm
        
    
P = Polynome([-1, 9, -6, 1])
sturm_sequence(P)

       
def nb_change_sign_at(polys, x):
    """ Calcule le nombre de changements de signes lorsqu'on évalue les 
    polynomes dans polys en x. Un zéro n'est pas considéré comme un changement
    de signe.
    
    Entrées:
        polys: liste de polynômes
        x: un nombre.
    
    Exemple:
        >>> X = Polynome([0, 1])
        >>> nb_change_sign_at([X, X**2+1, X+2], -1)
        1  # on a "-1, 2, 1" soit la chaîne de signes "-++", donc 1 changement
        >>> nb_change_sign_at([X, X**2+1, X-2], -1)
        2 # on a "-1, 2, -3" soit la chaîne de signes "-+-", donc 2 changements
        >>> nb_change_sign_at([X**2+1,X-2,-X],2)
        1 # on a "3.0.-2" soit la chaîne de signes "+0-", donc 1 changement
    """  
    c=0                                 #nombre de changement de signe
    sign=[]                             #liste de "+","-"
    
    for i in range (len(polys)):
        if type(polys[i])==int or type(polys[i])==float: #on teste si le terme
                                                        # est constant
            if polys[i]>0:
                sign.append(1)
            elif polys[i]<0:
                sign.append(-1)
        else:
            if eval_poly(polys[i],x)>0:
                sign.append(1)              #le signe "+" sera représenté par 1
            elif eval_poly(polys[i],x)<0:
                sign.append(-1)             #le signe "-" sera représenté par -1
                                        #comme le 0 ne compte pas, on ne le 
                                        #teste pas
    for j in range (1,len(sign)):
        if sign[j-1]!=sign[j]:          #on parcours la liste sign en regardant
                                        #si le le signe du terme précédent est
                                        #le même ou non que le signe du terme
                                        #suivant
            c+=1                        #si oui, le compteur est incrémenté de 1
    return c

X=Polynome([0,1])
nb_change_sign_at([X, X**2+1, X+2], -1)
nb_change_sign_at([X, X**2+1, X-2], -1)
nb_change_sign_at([X**2+1,X-2,-X],2)
nb_change_sign_at([X**3 - 6*X**2 + 9*X - 1, 3*X**2 - 12*X + 9, 2*X - 5, 9/4],2)

def nb_roots_between(polys, a, b):
    """ Renvoie le nombre de racines du premier polynôme de polys sur le
    segment ]a,b[, quand polys est une suite de Sturm.
    
    Entrées:
        polys: une liste de polynômes, plus exactement, polys est la suite de
            Sturm de polys[0];
        a: un nombre;
        b: un nombre strictement plus grand que a.
    """
    Da=nb_change_sign_at(polys,a)
    Db=nb_change_sign_at(polys,b)
    c=Da-Db
    if c>=0:
        return c
    else:
        return "pas de racine dans ]a;b["

polys=[X**3 - 6*X**2 + 9*X - 1, 3*X**2 - 12*X + 9, 2*X - 5, 9/4]
nb_roots_between(polys,-1,1) #résultat attendu : 1

def roots_range(P):
    """ Renvoie un nombre M > 0 tel que toutes les racines de P soient dans 
    l'intervalle [-M, M].
    
    Indication: voir exercice 21 du chapitre sur les polynômes (attention,
    dans l'exercice 21, le polynôme est supposé unitaire).
    """
    S=0
    P=P//P.lead                 #pour obtenir un polynome unitaire
    for i in range (P.deg+1):   # on appilque ensuite le résultat de l'ex 21
        S=S+abs(P[i])
    if 1>S:
        M=1
    else :
        M=S
    return M
    
P=Polynome([-4,0,1])
roots_range(P)
    
def nb_roots(polys):
    """ Renvoie le nombre de racines réelles du premier polynôme de polys,
    quand polys est une suite de Sturm.
    
    Entrées:
        polys: une liste de polynômes, plus exactement, polys est la suite de
            Sturm de polys[0].
    """
    b=roots_range(polys[0])
    a=-b
    nb=nb_roots_between(polys,a,b)
    return nb
    
polys=[X**3 - 6*X**2 + 9*X - 1, 3*X**2 - 12*X + 9, 2*X - 5, 9/4]
nb_roots(polys)


def find_root(P, a, b, eps):
    """ Trouve une racine de p dans [a,b[, sachant que p(a) * p(b) <= 0.
    Renvoie une approximation de la racine à eps près.

    Algorithme : utiliser une dichotomie.
    """
    while (b-a)/2>=eps:     
        i=(a+b)/2                  
        if eval_poly(P,i)==0:
            return i
        elif eval_poly(P,a)>0:
            if eval_poly(P,i)>0:
                a=i 
            else:
                b=i 
        elif eval_poly(P,a)<0:
            if eval_poly(P,i)>0:
                b=i 
            else:
                a=i 
    return (a+b)/2 

    
P=Polynome([1,2])
find_root(P, -3, 2, 0.01)


def isolate_roots(P):
    """ Renvoie une liste de nombres [x_0, x_1, ..., x_n]
    rangés dans l'ordre croissant telle qu'il existe une unique racine de P 
    entre chaque x_i et x_{i+1}. 
    
    Cette fonction est déjà implémentée et fonctionnera
    correctement sous réserve que toutes les fonctions ci-dessus sont 
    correctement implémentées.
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
    """ Renvoie la liste des racines de P avec une précision eps.
    On pourra calculer le radical de P, qui a même racines que P mais qui n'a
    pas de facteurs carrés; pour cela, on peut tout simplement utiliser
    P.square_free().
    """
    return 0
