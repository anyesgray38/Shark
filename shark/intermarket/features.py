from math import sqrt

def correlation(a: list[float], b: list[float]) -> float | None:
    n=min(len(a),len(b))
    if n < 2: return None
    a,b=a[-n:],b[-n:]
    ma=sum(a)/n; mb=sum(b)/n
    va=sum((x-ma)**2 for x in a); vb=sum((x-mb)**2 for x in b)
    if va == 0 or vb == 0: return None
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/sqrt(va*vb)

def alignment(primary: list[float], confirming: list[float]) -> float | None:
    return correlation(primary, confirming)
