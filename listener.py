import certifi
import pymongo

import ortho
import pair
from session import Session


def listen():
    type_ = change['ns']['coll']
    document = change['fullDocument']
    if type_ == 'pairs':  # todo hide this behind session
        pair.new_pair(Session(client), document['from'], document['to'])
    elif type_ == 'orthos':
        ortho.new_ortho(Session(client), document['data'])

# todo add missing unit tests - this was integration tested up front and so is missing them
# todo: dedup DB connection and read details from env.
# todo: implement a sweeper that is like a regular listener, except it puts all events into a queue and does them in order,
# and then starts over when it is done. It should write somewhere special if it finds something.
# todo: change to the callback api
if __name__ == '__main__':
    print("listening")
    uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile='X509-cert-5204489386261822956.pem', tlsCAFile=certifi.where())
    while True:
        # listener_watcher.idle()
        with client.watch() as stream:
            for change in stream:
                #listener_watcher.busy()
                listen()
