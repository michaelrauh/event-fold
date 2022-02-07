def new_pair(session, f, s):
    ex_nihil(session, f, s)


def ex_nihil(session, f, s):
    a_b_mapping(session, f, s)
    b_d_mapping(session, f, s)


def a_b_mapping(session, a, b):
    for d in session.project_forward(b):
        for c in session.project_backward(d):
            if b != c:
                if a in session.project_backward(c):
                    print("attempting a b insert")
                    session.ex_nihilo(a, b, c, d)


def b_d_mapping(session, b, d):
    for c in session.project_backward(d):
        if b != c:
            for a in session.project_backward(c):
                if b in session.project_forward(a):
                    print("attempting b d insert")
                    session.ex_nihilo(a, b, c, d)
