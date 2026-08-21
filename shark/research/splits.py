from dataclasses import dataclass

@dataclass(frozen=True)
class Split:
    train: tuple
    test: tuple

def holdout(items: list, train_fraction: float = 0.7) -> Split:
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")
    cut=int(len(items)*train_fraction)
    return Split(tuple(items[:cut]), tuple(items[cut:]))

def walk_forward(items: list, train_size: int, test_size: int, step: int | None = None):
    if train_size <= 0 or test_size <= 0:
        raise ValueError("window sizes must be positive")
    step=step or test_size
    if step <= 0:
        raise ValueError("step must be positive")
    i=0
    while i+train_size+test_size <= len(items):
        yield Split(tuple(items[i:i+train_size]), tuple(items[i+train_size:i+train_size+test_size]))
        i += step
