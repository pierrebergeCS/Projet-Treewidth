def priv(X,Y):
    L=[]
    for a in X:
        if a not in Y:
            L.append(a)
    return L

def aux1(X,Y):
    X0=X
    A=priv(X,Y)
    B=priv(Y,X)
    L=[]
    while len(A)>0:
        a=A.pop()
        X.delete(a)
        L.append(X)
    while len(B)>0:
        b=B.pop()
        X.append(b)
        L.append(X)
    return L

def nicepath(P):
    P=[[]]+P+[[]]
    N=[]
    for i in range(len(P)-1):
        N.append(P[i])
        N+=aux1(P[i],P[i+1])
    N+=P[-1]
    return N

def peigne(p,L):
    if len(L)<=1:
        return (p,L)
    else:
        return (p,[(p,[L[0]]),(peigne(p,L[1:]))])

def aux2(X,Y):
    X0=X
    A=priv(X,Y)
    B=priv(Y,X)
    L=[]
    while len(A)>0:
        a=A.pop()
        X.delete(a)
        L.append(X)
    while len(B)>0:
        b=B.pop()
        X.append(b)
        L.append(X)
    return chaine(L)

def chaine(L):
    if L=[]:
        return L
    else:
        return (L[0],[chaine(L[1:])])
