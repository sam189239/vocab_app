from freedictionaryapi.clients.sync_client import DictionaryApiClient
import pandas as pd
import streamlit as st
from csv import writer
import random
import pymongo
import regex as re
import os



  def get_table_download_link(df):
      """Generates a link allowing the data in a given panda dataframe to be downloaded
      in:  dataframe
      out: href string
      """
      csv = df.to_csv(index=False)
      b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
      href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
def download_as_pdf(df):
  

  return

def get_database():
    CONNECTION_STRING = os.getenv('CONNECTION_STRING') # MongoDB connection string - Config variable set on Heroku
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
  
  home_button = st.sidebar.button("Home")
  fl_button = st.sidebar.button("Full List")
  word = st.sidebar.text_input("Add words to the database here")
  add_button = st.sidebar.button("Add")
  
  if home_button:
    fl_button = False
    
  # Full list page
  if fl_button:
    st.title('Full word list: ')
    search()
    download_button = st.button('Download as PDF')
    fl_button = True
    df.sort_values(by=['word'], inplace=True)
    if download_button:
      st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    st.table(df)
    back_button = st.button('Go Back')
    if back_button:
      fl_button = False      


  # Home page
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
  #sort list
  #search in df
  #handle errors for syn or ex not found
