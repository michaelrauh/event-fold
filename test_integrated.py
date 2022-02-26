import subprocess
from time import sleep

import certifi
import pymongo

import ortho
from session import start_session


class TestIntegration:
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

        session.delete_pair("a", "b")
        session.delete_pair("c", "d")
        session.delete_pair("a", "c")
        session.delete_pair("b", "d")
        session.delete_ortho(expected)

        session.ingest("A b.")
        session.ingest("C d.")
        session.ingest("A c.")
        session.ingest("B d.")
        sleep(5)  # todo: allow listener to notify when done
        p.terminate()
        p.communicate()
        print("stopped listener")

        found = session.collection.orthos.find_one()['data'] #  TODO: remove all data, to, from subscripting as it leaks DB details
        assert expected == found
