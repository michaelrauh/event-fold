def create(a, b, c, d):
    return sorted([[a, []], [b, [b]], [c, [c]], [d, (sorted([b, c]))]])


def new_ortho(session, ortho):
    print(ortho)
    return None