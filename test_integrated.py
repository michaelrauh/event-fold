import subprocess
import unittest
from time import sleep

import certifi
import pymongo

import ortho
from session import start_session


class MyTestCase(unittest.TestCase):
    def test_ex_nihilo(self):
        expected = ortho.create("a", "b", "c", "d")
        print("starting listener")
        p = subprocess.Popen(["python", "listener.py"])
        uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri,
                                     tls=True,
                                     tlsCertificateKeyFile='X509-cert-5204489386261822956.pem',
                                     tlsCAFile=certifi.where())
        session = start_session(client)

        session.collection.pairs.delete_one({"from": "a", "to": "b"})  # todo hide deletes behind session
        session.collection.pairs.delete_one({"from": "c", "to": "d"})
        session.collection.pairs.delete_one({"from": "a", "to": "c"})
        session.collection.pairs.delete_one({"from": "b", "to": "d"})
        session.collection.orthos.delete_one({"data": expected})

        session.ingest("A b.")
        session.ingest("C d.")
        session.ingest("A c.")
        session.ingest("B d.")
        sleep(5)  # todo: allow listener to notify when done
        p.terminate()
        p.communicate()
        print("stopped listener")

        found = session.collection.orthos.find_one()['data']
        self.assertEqual(expected, found)


if __name__ == '__main__':
    unittest.main()
