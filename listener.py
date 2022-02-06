import pymongo

if __name__ == '__main__':
    cursor = pymongo.MongoClient("mongodb://127.0.0.1:27017").watch()
    document = next(cursor)
    print(document)