from math import sqrt

def summary(r_values: list[float]) -> dict:
    if not r_values:
        return {"trades":0,"win_rate":0.0,"expectancy":0.0,"profit_factor":0.0,"max_drawdown":0.0,"sharpe":0.0}
    wins=[r for r in r_values if r>0]; losses=[r for r in r_values if r<0]
    equity=[]; x=0.0; peak=0.0; dd=0.0
    for r in r_values:
        x+=r; peak=max(peak,x); dd=max(dd,peak-x)
        equity.append(x)
    mean=sum(r_values)/len(r_values)
    var=sum((r-mean)**2 for r in r_values)/max(1,len(r_values)-1)
    pf=sum(wins)/abs(sum(losses)) if losses else float('inf')
    return {"trades":len(r_values),"win_rate":len(wins)/len(r_values),"expectancy":mean,"profit_factor":pf,"max_drawdown":dd,"sharpe":mean/sqrt(var) if var else 0.0,"net_r":x}
