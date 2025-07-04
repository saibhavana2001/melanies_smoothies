# Import python packages 
import streamlit as st 
import snowflake.connector
import requests
import pandas as pd

# Write directly to the app 
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:") 
st.write( """ Choose the fruits you want in your custom smoothie! """ ) 
name_on_order = st.text_input('Name on your smoothie:') 

st.write('The of your smoothie will be: ', name_on_order) 

cnx = snowflake.connector.connect(
    user = 'SAIBHAVANA',
    password = '9014Bh@vana632',
    account = 'RDPZUWB-VMB49907'
)
cur = cnx.cursor()

cur.execute("Select fruit_name, search_on from smoothies.public.fruit_options")
fruit_options = cur.fetchall()

my_dataframe = pd.DataFrame(fruit_options, columns = ['fruit_name', 'search_on'])
#st.dataframe(data=my_dataframe, use_container_width=True) 
#st.stop()

pd_df = my_dataframe

#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect( 'Select upto 5 fruits:', my_dataframe, max_selections= 5 ) 

if ingredients_list: 
    #st.write(ingredients_list) 
    #st.text(ingredients_list)
    ingredients_string = '' 

    for fruit_choosen in ingredients_list: 
        ingredients_string += fruit_choosen + ' ' 

        search_on = pd_df.loc[pd_df['fruit_name'] == fruit_choosen, 'search_on'].iloc[0]
        #st.write('the serach value of the fruit choosen is '+search_on)

        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefruit_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        #st.text(smoothiefruit_response.json())
        sf_df = st.dataframe(data=smoothiefruit_response.json(), use_container_width=True) 


    st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(INGREDIENTS, name_on_order) values ('"""+ ingredients_string + """', '""" +name_on_order+"""')""" 
    
    #st.write(my_insert_stmt)    
    
    time_to_submit = st.button("Submit Order")
    
    if name_on_order:
        if time_to_submit: 
            cur.execute(my_insert_stmt)
            cnx.commit()
            st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")
    else:
        st.write('Please enter a name on your order')




cur.close()
cnx.close()
