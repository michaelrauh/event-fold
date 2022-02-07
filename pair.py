def new_pair(session, f, s):
    a_b_mapping(session, f, s)
    b_d_mapping(session, f, s)
    c_d_mapping(session, f, s)
    a_c_mapping(session, f, s)

    b_a_mapping(session, s, f)
    d_b_mapping(session, s, f)
    d_c_mapping(session, s, f)
    c_a_mapping(session, s, f)


def a_b_mapping(session, a, b):
    pass


def b_d_mapping(session, b, d):
    for c in session.project_backward(d):
        if b != c:
            for a in session.project_backward(c):
                if session.project_forward(a) == b:
                    session.ex_nihilo(a, b, c, d)


def c_a_mapping(session, d, c):
    pass


def d_c_mapping(session, d, c):
    pass


def b_a_mapping(session, b, a):
    pass


def d_b_mapping(session, d, b):
    pass


def c_d_mapping(session, c, d):
    pass


def a_c_mapping(session, a, c):
    pass
