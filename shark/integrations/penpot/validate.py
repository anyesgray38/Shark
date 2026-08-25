# Penpot Task Validation

def validate_task(task: dict) -> None:
    required = {"operation", "requirement"}
    missing = required.difference(task)
    if missing:
        raise ValueError(f"Missing Penpot task fields: {sorted(missing)}")
