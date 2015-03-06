#DM 6 (Partie Python)
    
    #Question 0
    P=X+2X^2+3X^3
    #Question 1
    L=54*[0]
    L[53]=1
    L[0]=1
    L[2]=3
    P = Polynome(L)   
    
    #Question 2
    deg.P
    
    #Question 3
    P[0]
    #Question 4
    5X^42 + 3X+1 par 42 X^12 +3X-2
    L=43*[0]
    L[42]=5
    L[1]=3
    L[0]=1
    P1 = Polynome (L)
    l=13*[0]
    l[12]=42
    l[1]=3
    l[0]=-2
    P2 = Polynome(l)
    
    R=-5/2744*X**9 + 5/1372*X**8 - 5/2058*X**7 + 5/9261*X**6 + 3*X + 1
    #Question 5
    P = Polynome([0,0])
    P.deg=-1
    
    
    def binomial(k,n):
        P = Polynome([1,1])
        Q=P**n
        return Q[k]
    def eval_poly(P, x):
        Q=0
        d=P.deg
        for i in range (d+1):
            Q=Q+P[i]*x**i
        return Q
    
    def derivative(P):
        d=P.deg
        L=[]
        for i in range (0,d):
            L[i]=i*P[i+1]
        Q = Polynome (L)
        return Q
        
    def sturm_sequence(P):
        L=[P,derivative(P)]
        i=0
        while not L[i]%L[i+1]==0 :
            L.append(-L[i]%L[i+1])
            i=i+1
        return L
    def nb_sg_change_at(L, x):
        c=0
        i=1
        while i=<len(L):
            if eval_poly(L[i],x)*eval_poly(L[i-1],x)<0:
                c=c+1
                i=i+1
            else :
                i=i+1
        return c
               
            
    