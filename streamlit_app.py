import streamlit
import pandas
import snowflake.connector
from urllib.error import URLError
import requests

streamlit.title('hello welcome to the page')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 🥗 🍞Omega 3 & Blueberry Oatmeal')
streamlit.text('🥣  🥑🍞Kale, Spinach & Rocket Smoothie')
streamlit.text('🥣 🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(my_fruit_list)
#create a repeatable code called function

def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized
     
streamlit.header('FruityVice fruit Advice')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice: 
          streamlit.error("please select a fruit to get information")
    else:
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
        streamlit.error()


streamlit.header("the fruit load list contains:")
#snowflake-related functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * from fruit_load_list")
            return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      streamlit.dataframe(my_data_rows)
      streamlit.stop()



fruit_choice = streamlit.text_input('What fruit you like to add?','Kiwi')
streamlit.write('Thank you for adding', fruit_choice)

my_cur.execute("insert into fruit_load_list values('from streamlit')");












