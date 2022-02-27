import MongoClient
import ortho
import pair
from session import Session, ChangeType


def listen(session, change):
    print("busy")
    type_ = session.change_type(change)
    if type_ == ChangeType.PAIRS:
        pair.new_pair(session, session.get_from(change), session.get_to(change))
    elif type_ == ChangeType.ORTHOS:
        ortho.new_ortho(session, session.get_data(change))
    print("idle")


if __name__ == '__main__':
    while True:
        Session(MongoClient.client).listen_on_change(listen)
