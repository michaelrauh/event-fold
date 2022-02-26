from enum import Enum, auto


class Position(Enum):
    ORIGIN = auto()
    HOP = auto()
    OTHER = auto()


def create(x11, x12, x21, x22):
    return sorted([[x11, []], [x12, [x12]], [x21, [x21]], [x22, (sorted([x12, x21]))]])


def new_ortho(session, ortho):
    print(ortho)
    return None


def origin(ortho):
    return next(node[0] for node in ortho if len(node[1]) == 0)


def translate_coordinates(ortho, axis_mapping):
    return [[node[0], [axis_mapping[name] for name in node[1]]] for node in ortho]


def augment_coordinates(ortho, augmenting_axis): # todo: there is a missing test here that coordinates end up sorted during augmentation
    return [[node[0], node[1] + [augmenting_axis]] for node in ortho]


def zip_up(left, right, axis_mapping):
    return sorted(left + augment_coordinates(translate_coordinates(right, axis_mapping), origin(left)))


def get_axes(ortho):
    return sorted([node[0] for node in ortho if len(node[1]) == 1])


def name_at_location(ortho, location):
    length = len(location)
    if length == 0:
        return origin(ortho)
    elif length == 1:
        return location[0]
    else:
        return next(node[0] for node in ortho if node[1] == location)


def length_of_bottom_right_coordinates(ortho):
    return max(len(node[1]) for node in ortho)


def get_names_at_distance(ortho, dist):
    return {node[0] for node in ortho if len(node[1]) == dist}


def get_names_as_list_of_diagonal_sets(ortho):
    return [get_names_at_distance(ortho, dist) for dist in range(1 + length_of_bottom_right_coordinates(ortho))]


def position(ortho, name):
    buckets = get_names_as_list_of_diagonal_sets(ortho)
    if name in buckets[0]:
        return Position.ORIGIN
    elif name in buckets[1]:
        return Position.HOP
    else:
        return Position.OTHER
