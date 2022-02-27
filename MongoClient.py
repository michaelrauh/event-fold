import certifi
import pymongo

uri = "mongodb+srv://cluster0.t0zld.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = pymongo.MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile='X509-cert-5204489386261822956.pem', tlsCAFile=certifi.where())