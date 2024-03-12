from PIL import Image

import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


fav = Image.open("../images/pressure-cooker.ico")
st.set_page_config(
    page_title="model prediction",
    page_icon=fav,
)


def map_ingredients(ingr: list[str]) -> list[int]:
    """ 
    fetches pickle file with mapping of ingredient labels to the ints used in the model
    Arg:
        ingr: list of ingredient labels for an individual recipe
    Returns:
        list of integers from the mapper that correspond to the labels
        if the label isn't found, we add -1 to indicate that
    """
    map_df = pd.read_pickle("../data/kaggle_food_dot_com/ingr_map.pkl")
    codes = []

    for label in ingr:
    # for label in ["plum tomatoes"]:
        replaced = map_df.loc[map_df["replaced"] == label.lower()]
        raw = map_df.loc[map_df["raw_ingr"].str.find(label.lower()) != -1]
        if replaced.shape[0] > 0:
            print(f"found {label} in replaced")
            code = replaced["id"].value_counts().idxmax()
            
        elif raw.shape[0] > 0:
            print(f"found {label} in raw")
            code = raw["id"].value_counts().idxmax()
            
        else:
            print(f"couldn't find {label}")
            code=-1
        
        codes.append(code)
    return codes
    
    
def display_model_prediction():
    recipe = st.session_state.selected_recipe
    st.header(recipe["title"])
    mapped_ingreds = map_ingredients(recipe["ingredients"])
    
        

if len(st.session_state.selected_recipe) > 0:
    display_model_prediction()
else:
    st.write("No recipe selected!")
    back_to_form = st.button("input form")
    if back_to_form:
        switch_page("home")
    
    back = st.button("recipe list")
    if back:
        switch_page("recipe_list")
        
    