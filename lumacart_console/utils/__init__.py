def safe_get(sequence, default = None):
    return sequence[0] if sequence else default