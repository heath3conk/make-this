from PIL import Image

import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


fav = Image.open("../images/pressure-cooker.ico")
st.set_page_config(
    page_title="Selected recipe",
    page_icon=fav,
)



map_df = pd.read_pickle("../data/kaggle_food_dot_com/ingr_map.pkl")
recommender = pd.read_parquet("../data/generated_data/recommender_all.parquet")


def find_ingredient_id(ingred: str) -> set[str]:
    """ 
    finds ids in "ingr_map" data that matches selected ingredient, searching in the
    "replaced" and "raw_ingr" columns
    Args:
        ingred: the ingredient to search for
    Returns: int id that seems like the closest match for the ingredient
    """
    codes = []
    replaced = map_df.loc[map_df["replaced"] == ingred.lower()]
    raw = map_df.loc[map_df["raw_ingr"].str.find(ingred.lower()) != -1]
    
    # returning all the possible matches to pass to recommender
    if replaced.shape[0] > 0:
        codes.extend(replaced["id"])
        
    if raw.shape[0] > 0:
        codes.extend(raw["id"])
        
    else:
        print(f"couldn't find {ingred}")
        # return empty set
        return set(codes)
    
    return set([ str(code) for code in codes ])


def recommend_subs(codes: list[str]) -> list[tuple[str, float]]:
    if len(codes) == 0:
        print("no codes to get recommendations for")
        return []
    
    # build dict of ingredient labels & their values from the recommender
    hits = {}
    for code in codes:
        # just in case the ingredient is one those we removed because of its infrequency
        if code in list(recommender.columns):
            # get top 10 values from the recommender
            top_hits = recommender[code].sort_values(ascending = False)[1:11]
            for i in top_hits:
                # get str index where the search ingredient matches the value in top_hits
                #  that index = the ingredient id
                ingr_id = recommender.index[recommender[code]==i].array[0]
                mapped = map_df.loc[map_df["id"] == int(ingr_id), "raw_ingr"]
                ing_label = list(mapped)[0]
                # if that label is already in the dict, keep it set to the highest value from recommender
                if ing_label in hits.keys():
                    prev_value = hits[ing_label]
                    value = i if i > prev_value else prev_value
                    hits[ing_label] = value
                else:
                    hits[ing_label] = i
    
    if len(hits) > 0:
        return sorted(hits.items(), key=lambda x: x[1], reverse=True)
    else:
        return []
    


def get_substitute(ingred:str) -> None:
    """ 
    streamlit opereations
    calls "find_ingredient_id" and "recommend_subs" and displays suggested substitutes
    includes some error handling, probably not enough of that
    """
    codes = find_ingredient_id(ingred)
    if len(codes) > 0:
        subs = recommend_subs(list(codes))
        if len(subs) > 0:
            st.subheader(f"Here are a few options to use in place of {ingred}:")
            
            # subs is a list of tuples: ({ingredient label}, {recommender value}), sorted by recommender value
            if subs[0][1] < 0.1:
                st.write("low confidence in these suggestions")
            
            max_show = min(3, len(subs))
            # found this here: https://discuss.streamlit.io/t/python-list-output-as-markdown-lists-beautify-lists/23303/3
            md_list = ""
            for i in subs[:max_show]:
                md_list += f"- {i[0]}, recommender value: {round(i[1], 4)}\n"
            st.markdown(md_list)
        else: 
            st.write(f"Oops! Couldn't find any substitutions for {ingred}.")
    else: 
        st.write(f"Oops! Couldn't find {ingred} in the recommender.")


def display_recipe() -> None:
    """ 
    streamlit operations
    displays the image and ingredient list for the selected recipe, 
    buttons for: 
      - go to the URL for the recipe (link from the recipe API)
      - go back to the list of recipes
    
    """
    recipe = st.session_state.selected_recipe
    st.header(recipe["title"])

    col1, col2 = st.columns(2)
    col1.image(recipe["image"])
    col2.subheader("ingredients list")
    for i in recipe["ingredients"]:
        col2.checkbox(i, value=False, key=i, on_change=get_substitute, args=(i,))
        
    st.link_button("recipe source", recipe["link"])
    st.write("(original source may or may not still be available)")

    # predict = st.button("get model prediction")
    # if predict:
    #     switch_page("model_prediction")

    back = st.button("back to list of recipes")
    if back:
        st.session_state.selected_recipe = {}
        switch_page("recipe_list")
        

if len(st.session_state.selected_recipe) > 0:
    display_recipe()
else:
    st.write("No recipe selected!")
    back_to_form = st.button("input form")
    if back_to_form:
        switch_page("home")
    
    back = st.button("recipe list")
    if back:
        switch_page("recipe_list")
        
    