def parse_args(args, expected=0):
    """
    Simple parser: ensures at least `expected` args; returns list or None.
    """
    if len(args) < expected:
        return None
    return args
