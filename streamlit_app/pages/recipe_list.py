import time
from PIL import Image
import json
import requests

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

fav = Image.open("../images/pressure-cooker.ico")
st.set_page_config(
    page_title="Found recipes",
    page_icon=fav,
)

# initializing selected_recipe to empty dict
st.session_state.selected_recipe = {}

with open("../secrets.json", "rb") as f:
    key_file = json.loads(f.read())

APP_ID = key_file["app_id"]
APP_KEY = key_file["key"]


def get_recipes(ingr: list[str], dish: str="Main course", meal: str="Dinner") -> list[dict[str: any]]:
    """ 
    Calls external API to get recipes with the given ingredients
    Args:
        ingr: list of ingredients the user entered in the previous page
        dish: type of recipe to search for, defaults to "Main course" for v1
        meal: defaults to "Dinner" for v1
    Returns:
        list of dicts where each dict represents a recipe with a title, link & image & other data
    """
    recipes_endpoint = "https://api.edamam.com/api/recipes/v2?type=public"
    ingredients = f"q={'%2C%20'.join(ingr)}"  # TODO: handle empty `ingr` list
    
    num_ingr = (len(ingr), 10)
    min_max_ingr = f"ingr={min(num_ingr)}-{max(num_ingr)}"
    dish_type=f"dishType={dish}"
    meal_type = f"mealType={meal}"
    full_url = f"{recipes_endpoint}&{ingredients}&{min_max_ingr}&{dish_type}&{meal_type}&app_id={APP_ID}&app_key={APP_KEY}"
    response = requests.get(full_url)
    data = response.json()
    
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
            
        return items, 200
    
    elif response.status_code != 200:
        return items, response.status_code
    
    else:
        return items, 200


def individual_recipe_display(recipe: dict[str: any]) -> None:
    """ 
    streamlit operations
    Args: 
        recipe: dict for an individual recipe
        i: index of that recipe in the sorted_recipes list
    """
    col1, col2 = st.columns(2)
    select_recipe = col1.button(recipe["title"])
    col2.image(recipe["image"])
    if select_recipe:
        print(f"clicked {recipe["title"]}")
        st.session_state.selected_recipe = recipe
        switch_page("individual_recipe")
    
        
def display_recipes(recipes: dict[str: any]) -> None:
    """ 
    streamlit operations
    - sorts recipes by number of ingredients
    - displays top 5 with title, image, link & radio button
    """
    sorted_recipes = sorted(recipes, key=lambda x: x["num_ingredients"])
    max_display = min(len(sorted_recipes), 5)
    for i in range(max_display):
        individual_recipe_display(sorted_recipes[i])


def fetch_recipes() -> None:
    """
    streamlit operations
    - runs `get_recipes` function with user-entered ingredients
    - displays top 5 recipes, sorted by fewest number of ingredients
    """
    if len(st.session_state.ingredients) > 0:
        results = get_recipes(st.session_state.ingredients)
        if len(results[0]) > 0:
            st.session_state.recipes = results[0]
            display_recipes(results[0])
        print(f"fetched {len(results[0])} recipes")
        print(f"status code = {results[1]}")
        
    else:
        switch_page("home")
        st.write("Please enter some ingredients")


for _ in st.session_state.ingredients:
    print(_)

fetch_recipes()







