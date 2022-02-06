import certifi
import pymongo

def handle_new_forward(f, s):
    print(f, s)

if __name__ == '__main__':
    while True:
        uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri,
                                     tls=True,
                                     tlsCertificateKeyFile='X509-cert-5204489386261822956.pem', tlsCAFile=certifi.where())
        cursor = client.watch()  # todo use resume
        document = next(cursor)
        print(document)
        handle_new_forward(document['fullDocument']['from'], document['fullDocument']['to'])



