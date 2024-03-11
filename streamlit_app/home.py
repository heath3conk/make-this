from PIL import Image
import json
import requests

import streamlit as st
from streamlit_extras.switch_page_button import switch_page


fav = Image.open("../images/pressure-cooker.ico")
st.set_page_config(
    page_title="Make This!",
    page_icon=fav,
)

st.title("Make this!")

# initializing ingredients to empty list
st.session_state.ingredients = []

def gather_ingredients():
    st.subheader("Let's find some recipes you can make.")
    st.write("Enter some ingredients you have on hand:")
    ingredients = st.text_area("enter ingredients, separated by commas").split(",")
    st.session_state.ingredients = [ i.strip() for i in ingredients ]
    st.session_state.recipes = []
    fetch_recipes = st.button("fetch recipes")
    # nice to have: capture cmd+enter with same behavior as button
    if fetch_recipes:
        print("switching to recipe list")
        switch_page("recipe_list")
    


gather_ingredients()
    


