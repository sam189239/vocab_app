import pymongo
import pandas as pd


def get_database():
    CONNECTION_STRING = "mongodb+srv://sam:1234239@vocab-app-cluster.ckp7m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client['dict_list']
    

if __name__ == "__main__":    
    db = get_database()
    coll = db["words"]
    item = {"word":"indefatigable"," definition":"(of a person or their efforts) persisting tirelessly."," examples":"an indefatigable defender of human rights"," synonyms":"unfaltering, indomitable, dogged, single-minded, dynamic, never-tiring, unflagging, assiduous, untiring, unswerving, persistent, tireless, industrious, unwearying, unwearied, unremitting, determined, tenacious, unshakeable, energetic, enthusiastic, relentless, unrelenting"}
    # coll.insert_one(item)
    df = pd.DataFrame(coll.find())
    df = df.drop('_id', 1)
    print(df.head())