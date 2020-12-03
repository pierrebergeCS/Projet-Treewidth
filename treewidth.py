def priv(X,Y):
    '''renvoie X privé de Y'''
    L=[]
    for a in X:
        if a not in Y:
            L.append(a)
    return L

def aux1(X,Y):
    '''canonise le passage entre 2 sacs'''
    X0=X
    A=priv(X,Y)
    B=priv(Y,X)
    L=[]
    while len(A)>0:
        #ajout des sacs forget un à un
        a=A.pop()
        X.delete(a)
        L.append(X)
    while len(B)>0:
        #ajout des sacs introduce un à un
        b=B.pop()
        X.append(b)
        L.append(X)
    return L #liste des forget et introduce à ajouter entre X et Y

def nicepath(P):
    '''transforme une décomposition linéaire en une canonique de même largeur'''
    P=[[]]+P+[[]]
    N=[]
    for i in range(len(P)-1):
        #canonise les passages entre sacs
        N.append(P[i])
        N+=aux1(P[i],P[i+1])
    N+=P[-1]
    return N #la nice path-decomposition

def peigne(p,L):
    '''prend en entrée un couple père,liste de fils 
    et renvoie un arbre binaire en peigne où chaque fils est le fils de p'''
    if len(L)<=1:
        return (p,L)
    else:
        return (p,[(p,[L[0]]),(peigne(p,L[1:]))])

def chaine(L):
    '''transforme une liste en arbre chaîne'''
    if L=[]:
        return L
    else:
        return (L[0],[chaine(L[1:])])
