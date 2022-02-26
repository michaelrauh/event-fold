import itertools

import ortho


def projections_work(left_locations, right_locations, left, right, session):
    for left_location, right_location in zip(left_locations, right_locations):
        if not (ortho.name_at_location(right, right_location) in session.project_forward(ortho.name_at_location(left, left_location))):
            return False
    return True


def find_axis_mappings(left, right, session):
    return [dict(zip(ortho.get_axes(right), permutation)) for permutation in
            itertools.permutations(ortho.get_axes(left)) if
            projections_work(permutation, ortho.get_axes(right), left, right, session)]


def diagonal_works(left, right):
    for set_left, set_right in zip(ortho.get_names_as_list_of_diagonal_sets(left)[1:], ortho.get_names_as_list_of_diagonal_sets(right)[:-1]):
        if not set_left.isdisjoint(set_right):
            print(f"filtering {left} + {right} due to diagonal rule")
            return False
    return True


def up(session, f, s):
    for left, right in itertools.product(session.ortho_with_name(f), session.ortho_with_name(s)):
        left_type = ortho.position(left, f)
        right_type = ortho.position(right, s)
        if left_type == right_type == ortho.Position.ORIGIN:
            for axis_mapping in find_axis_mappings(left, right, session):
                if diagonal_works(left, right):
                    print("attempting up insert")
                    session.add_ortho(ortho.zip_up(left, right, axis_mapping))


def new_pair(session, f, s):
    ex_nihilo(session, f, s)
    up(session, f, s)


def ex_nihilo(session, f, s):
    a_b_mapping(session, f, s)
    b_d_mapping(session, f, s)


def a_b_mapping(session, a, b):
    # a b
    # c d
    for d in session.project_forward(b):
        for c in session.project_backward(d):
            if b != c:
                if a in session.project_backward(c):
                    print("attempting a b insert")
                    session.add_ortho(ortho.create(a, b, c, d))


def b_d_mapping(session, b, d):
    for c in session.project_backward(d):
        if b != c:
            for a in session.project_backward(c):
                if b in session.project_forward(a):
                    print("attempting b d insert")
                    session.add_ortho(ortho.create(a, b, c, d))
