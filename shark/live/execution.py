class LiveExecutionDisabled(RuntimeError):
    pass


def submit_order(*args, **kwargs):
    raise LiveExecutionDisabled(
        "Live execution is disabled. Complete research, out-of-sample, walk-forward, "
        "paper-trading and explicit risk review before enabling an execution adapter."
    )
