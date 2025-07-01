# Import python packages 
import streamlit as st 
from snowflake.snowpark.functions import col, when_matched 

# Write directly to the app 
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:") 
st.write( """ Choose the fruits you want in your custom smoothie! """ ) 
name_on_order = st.text_input('Name on your smoothie:') 

st.write('The of your smoothie will be: ', name_on_order) 

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name')) 
#st.dataframe(data=my_dataframe, use_container_width=True) 
ingredients_list = st.multiselect( 'Select upto 5 fruits:', my_dataframe, max_selections= 5 ) 

if ingredients_list: 
    #st.write(ingredients_list) 
    #st.text(ingredients_list)
    ingredients_string = '' 
    for fruit_choosen in ingredients_list: 
        ingredients_string += fruit_choosen + ' ' 
    st.write(ingredients_string) 
    my_insert_stmt = """insert into smoothies.public.orders(INGREDIENTS, name_on_order) values ('"""+ ingredients_string + """', '""" +name_on_order+"""')""" 
    #st.write(my_insert_stmt) 
    time_to_submit = st.button("Submit Order")
    if time_to_submit: 
        session.sql(my_insert_stmt).collect() 
        st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")
