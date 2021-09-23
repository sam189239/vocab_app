# from altair.vegalite.v4.schema.core import FlattenTransform
from numpy.core.fromnumeric import mean
from freedictionaryapi.clients.sync_client import DictionaryApiClient
import pandas as pd
import streamlit as st
from csv import writer
import random
import pymongo
import regex as re


def get_database():
    CONNECTION_STRING = "mongodb+srv://sam:1234239@vocab-app-cluster.ckp7m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client['dict_list']


def meaning(input_word):
  with DictionaryApiClient() as client:
    parser = client.fetch_parser(input_word)
  word = parser.word
  defn = []
  for meaning in word.meanings:
      for definition in meaning.definitions:
              defn.append(meaning.part_of_speech + ": " + str(definition))
  # defn = str(defn)
  link = parser.get_link_on_audio_with_pronunciation()
  all_def = ", ".join(parser.get_all_definitions())
  syns = ", ".join(parser.get_all_synonyms())
  exs = ", ".join(parser.get_all_examples())
  return defn, link, all_def, syns, exs


def display_word(df, r):
  st.header(df.loc[r].iat[0])
  st.markdown(df.loc[r].iat[1])
  st.markdown("Examples: "+df.loc[r].iat[2])
  st.markdown("Synonyms: "+df.loc[r].iat[3])
  
def search():
  search_txt = st.text_input("")
  search_btn = st.button("Search")
  if search_btn or search_txt:
    my_regex = r"\b(?=\w)" + re.escape(search_txt) + r"\w*"
    myquery = { "word": { "$regex": my_regex } }
    mydoc = pd.DataFrame(coll.find(myquery))
    len = mydoc.shape[0]
    if(len>=1):
      mydoc = mydoc.drop('_id', 1)
      if(len==1):
        display_word(mydoc, 0)
      else:
        st.dataframe(mydoc)
    else:
      st.write("No results found")


if __name__ == "__main__":    
  db = get_database()
  coll = db["words"]
  df = pd.DataFrame(coll.find())
  df = df.drop('_id', 1)
  
  fl_button = st.sidebar.button("Full List")
  word = st.sidebar.text_input("Add words to the database here")
  add_button = st.sidebar.button("Add")
  

  if fl_button:
    st.title('Full word list: ')
    search()
    st.table(df)
    button = st.button('Go Back')
    if button:
      fl_button = False


  else:

    st.title("Vocabulary app")
    
    # Display random word
    rand_button = st.button("Random")
    if rand_button:
      len = df.shape[0] - 1
      r = random.randint(0,len)
      display_word(df, r)

    # Display new word added
    if add_button or word:
      defn, link, all_def, syns, exs  = meaning(word)
      row_contents = [word, all_def, exs, syns]
      item = {"word":word," definition":all_def," examples":exs," synonyms":syns}
      coll.insert_one(item)
      st.header("Added Word: ")
      st.header(word)
      st.markdown(all_def)
      st.markdown("Examples: " + exs)
      st.markdown("Synonyms: " + syns)

    # Display word list
    st.header("Word list")  
    search()

    st.dataframe(df)





  #clickable lists
  #duplicate removal