from altair.vegalite.v4.schema.core import FlattenTransform
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


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


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
  



if __name__ == "__main__":    
  db = get_database()
  coll = db["words"]
  df = pd.DataFrame(coll.find())
  df = df.drop('_id', 1)
  # print(df.head())
  # df = pd.read_csv("dict.csv")
  
  fl_button = st.sidebar.button("Full List")
  word = st.sidebar.text_input("Add words to the database here")
  add_button = st.sidebar.button("Add")
  

  if fl_button:
    st.title('here is a page')
    button = st.button('Go Back')
    if button:
      fl_button = False


  else:

    st.title("Vocabulary app")
    
    rand_button = st.button("Random")
    if rand_button:
      len = df.shape[0] - 1
      # print(len)
      r = random.randint(0,len)
      display_word(df, r)

    if add_button or word:
      defn, link, all_def, syns, exs  = meaning(word)
      row_contents = [word, all_def, exs, syns]
      # append_list_as_row('dict.csv', row_contents)
      item = {"word":word," definition":all_def," examples":exs," synonyms":syns}
      coll.insert_one(item)
      st.header("Added Word: ")
      st.header(word)
      st.markdown(all_def)
      st.markdown("Examples: " + exs)
      st.markdown("Synonyms: " + syns)
      # display_word(df, df.shape[0]-1)

    st.header("Word list")  
    search_text = st.text_input("")
    search_button = st.button("Search")
    # if search_text:
    #   search_button = True
    if search_button or search_text:
      my_regex = r"\b(?=\w)" + re.escape(search_text) + r"\w*"
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

    st.dataframe(df)


  
  # st.markdown(df.head())
  # cols = ["word", "definition", "examples", "synonyms"]
  # st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)

  









  #clickable lists
  #duplicate removal