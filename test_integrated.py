import subprocess
from time import sleep

import MongoClient
import ortho
from session import start_session


class TestIntegration:
    def test_ex_nihilo(self):
        expected = ortho.create("a", "b", "c", "d")
        print("starting listener")
        p = subprocess.Popen(["python", "listener.py"])
        client = MongoClient.client
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
        sleep(5)
        p.terminate()
        p.communicate()
        print("stopped listener")

        found = session.get_one_ortho()
        assert expected == found
