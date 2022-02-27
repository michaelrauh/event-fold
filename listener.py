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

# todo add missing unit tests - this was integration tested up front and so is missing them
# todo implement a sweeper that replays all events. There can be a max of one of these per DB.


if __name__ == '__main__':
    while True:
        Session(MongoClient.client).listen_on_change(listen)
