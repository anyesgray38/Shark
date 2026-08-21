import random
from statistics import mean

def monte_carlo_drawdown(returns: list[float], iterations: int = 2000, seed: int = 42) -> dict:
    if not returns: return {"p95_drawdown": 0.0, "drawdowns": []}
    rng=random.Random(seed); dds=[]
    for _ in range(iterations):
        sample=[rng.choice(returns) for _ in returns]
        equity=peak=1.0; dd=0.0
        for r in sample:
            equity *= 1+r
            peak=max(peak,equity)
            dd=max(dd,(peak-equity)/peak)
        dds.append(dd)
    dds.sort(); idx=min(len(dds)-1,int(.95*len(dds)))
    return {"p95_drawdown": dds[idx], "drawdowns": dds}

def permutation_test(returns: list[float], iterations: int = 2000, seed: int = 42) -> dict:
    if not returns: return {"observed": 0.0, "p_value": 1.0}
    rng=random.Random(seed); observed=mean(returns); exceed=0
    for _ in range(iterations):
        signs=[1 if rng.random() >= .5 else -1 for _ in returns]
        null=mean(r*s for r,s in zip(returns,signs))
        if null >= observed: exceed += 1
    return {"observed": observed, "p_value": (exceed+1)/(iterations+1)}
