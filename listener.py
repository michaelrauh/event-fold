import certifi
import pymongo

import ortho
import pair
from session import Session

if __name__ == '__main__':
    uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile='X509-cert-5204489386261822956.pem', tlsCAFile=certifi.where())
    while True:
        with client.watch() as stream:
            for change in stream:
                t = change['ns']['coll']
                if t == 'pairs':
                    doc = change['fullDocument']
                    pair.new_pair(Session(client), doc['from'], doc['to'])
                elif t == 'orthos':
                    doc = change['fullDocument']
                    ortho.new_ortho(Session(client), doc['data'])
