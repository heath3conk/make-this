from PIL import Image
import json
import requests

import streamlit as st
from streamlit_extras.switch_page_button import switch_page


fav = Image.open("../images/pressure-cooker.ico")
st.set_page_config(
    page_title="Selected recipe",
    page_icon=fav,
)

recipe = st.session_state.selected_recipe
st.header(recipe["title"])

# found this here: https://discuss.streamlit.io/t/python-list-output-as-markdown-lists-beautify-lists/23303/3
md_list = ""
for i in recipe["ingredients"]:
    md_list += "- " + i + "\n"

col1, col2 = st.columns(2)
col1.image(recipe["image"])
col2.subheader("ingredients list")
col2.markdown(md_list)

st.link_button("Go recipe source", recipe["link"])
st.write("(original source may or may not still be available)")

back = st.button("Back to list of recipes")
if back:
    st.session_state.selected_recipe = {}
    switch_page("recipe_list")