import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Using Value of Fruit column as index instead of row index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # take the json verson of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# Adding heading for new section
streamlit.header('Fruityvice Fruit Advice')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    # output data to the screen as a table
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
    
except URLError as e:
  streamlit.error()
                    
# nothing will run past this point while we troubleshoot
streamlit.stop()

# connecting with snoflake and executing a query.
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")    # Testing connection
my_cur.execute('SELECT * FROM fruit_load_list')
my_data_row = my_cur.fetchall()
streamlit.text("The fruit_load_list contains:")
streamlit.dataframe(my_data_row)

add_fruit = streamlit.text_input('What fruit would you like to add?', 'Kiwi')
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")   # Modified test query to avoid error
streamlit.write('Thanks for adding', add_fruit)
