import time
from PIL import Image
import json
import requests

import pandas as pd
import streamlit as st


fav = Image.open("../images/pressure-cooker.ico")
st.set_page_config(
    page_title="Make This!",
    page_icon=fav,
)

st.title("Make this!")

st.subheader("Let's find some recipes you can make.")
st.write("Enter some ingredients you have on hand:")
ingredients = st.text_area("enter ingredients, separated by commas")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('fetch recipes', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    st.write("Searching for recipes")
    with st.spinner(text='In progress'):
        time.sleep(3)
        st.success('Done')


for i in ingredients:  # this prints each character on its own
    print(i)


with open("../secrets.json", "rb") as f:
    key_file = json.loads(f.read())

APP_ID = key_file["app_id"]
APP_KEY = key_file["key"]


def get_recipes(ingr: list[str], time: int, dish: str="Main course", meal: str="Dinner"):
    recipes_endpoint = "https://api.edamam.com/api/recipes/v2?type=public"
    ingredients = f"q={'%2C%20'.join(ingr)}"  # TODO: handle empty `ingr` list
    
    num_ingr = (len(ingr), 10)
    min_max_ingr = f"ingr={min(num_ingr)}-{max(num_ingr)}"
    time_spent = f"time=0-{time}" # TODO: handle empty `time` value
    dish_type=f"dishType={dish}"
    meal_type = f"mealType={meal}"
    full_url = f"{recipes_endpoint}&{ingredients}&{min_max_ingr}&{dish_type}&{meal_type}&{time_spent}&app_id={APP_ID}&app_key={APP_KEY}"
    response = requests.get(full_url)
    data = response.json()
    # print(response.status_code)
    
    if response.status_code == 200 and data["count"] > 0:
        items = []
        for item in data["hits"]:
            recipe_dict = {}
            recipe_dict["title"] = item["recipe"]["label"]
            recipe_dict["link"] = item["recipe"]["url"]
            recipe_dict["image"] = item["recipe"]["images"]["REGULAR"]["url"]
            recipe_dict["servings"] = item["recipe"]["yield"]
            # recipe_dict["cuisine"] = item["recipe"]["cuisineType"]
            # recipe_dict["diet_labels"] = item["recipe"]["dietLabels"]
            # recipe_dict["healh_labels"] = item["recipe"]["healthLabels"]
            # recipe_dict["cautions"] = item["recipe"]["cautions"]
            # recipe_dict["ingredient_lines"] = item["recipe"]["ingredientLines"]
            
            ingreds = []
            for ingr in item["recipe"]["ingredients"]:
                ingreds.append(ingr["food"])
                recipe_dict["ingredients"] = list(set(ingreds))
            
            recipe_dict["num_ingredients"] = len(recipe_dict["ingredients"])
            items.append(recipe_dict)
            
        return pd.DataFrame.from_dict(items), 200
    
    elif response.status_code != 200:
        return pd.DataFrame(), response.status_code
    
    else:
        return pd.DataFrame(), 200