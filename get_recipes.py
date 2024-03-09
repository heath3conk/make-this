import json
import requests

import pandas as pd


def get_recipes(ingr: list[str], num_ingr: tuple[int, int], app_id: str, app_key: str, dish: str="Main course", meal: str="Dinner"):
    recipes_endpoint = "https://api.edamam.com/api/recipes/v2?type=public"
    ingredients = f"q={'%2C%20'.join(ingr)}"  # TODO: handle empty `ingr` list
    min_max_ingr = f"ingr={min(num_ingr)}-{max(num_ingr)}"  # TODO: handle empty or single-element `num_ingr`
    dish_type=f"dishType={dish}"
    meal_type = f"mealType={meal}"  # TODO: set default `meal`?
    full_url = f"{recipes_endpoint}&{ingredients}&{min_max_ingr}&{dish_type}&{meal_type}&app_id={app_id}&app_key={app_key}"
    # print(full_url)
    response = requests.get(full_url)
    data = response.json()
    print(response.status_code)
    
    if response.status_code == 200 and data["count"] > 0:
        items = []
        for item in data["hits"]:
            recipe_dict = {}
            recipe_dict["title"] = item["recipe"]["label"]
            recipe_dict["link"] = item["recipe"]["url"]
            recipe_dict["servings"] = item["recipe"]["yield"]
            recipe_dict["cuisine"] = item["recipe"]["cuisineType"]
            recipe_dict["diet_labels"] = item["recipe"]["dietLabels"]
            recipe_dict["healh_labels"] = item["recipe"]["healthLabels"]
            recipe_dict["cautions"] = item["recipe"]["cautions"]
            recipe_dict["ingredient_lines"] = item["recipe"]["ingredientLines"]
            
            ingred_labels =[]    
            ingreds = []
            for ingr in item["recipe"]["ingredients"]:
                ingredient_details = {}
                ingredient_details["text"] = ingr["text"]
                ingredient_details["quantity"] = ingr["quantity"]
                ingredient_details["measure"] = ingr["measure"]
                ingredient_details["weight"] = ingr["weight"]
                ingredient_details["food"] = ingr["food"]  # adds "food" label to the "ingredient details" dict
                ingredient_details["food_category"] = ingr["foodCategory"]
                ingreds.append(ingredient_details)
                recipe_dict["ingredient_details"] = ingreds
                
                ingred_labels.append(ingr["food"])  # adds "food" label to list of ingredients
                recipe_dict["ingredient_labels"] = ingred_labels
            items.append(recipe_dict)
    return pd.DataFrame.from_dict(items)

    