# Make this!

## Problem statement
How can I decide what to cook in the evening when my executive function is low? I have ingredients and I know how 
to cook but I need someone to give me some ideas about what to make. 

I also want to be able to customize recipes to my preferences and make subsitutions while retaining the flavor profile of 
my favorite food. Examples:
- Suppose I really don't like olives so any recipe that features olives is unlikely to make my list unless I can understand what they
    add to the flavor so I can substitute something else for their salty/briny-ness.
- Maybe I'm lactose intolerant but love pasta dishes and pizza. What can I do to give my lasange some creamy goodness without ricotta 
    or mozzarella?

I want an app where I can give it a short list of ingredients and choose from a list of recipes. Then in the recipe I've selected,
I want to use data science to suggest substitutions for specific ingredients.

## Top-level results
I used cosine similarity to create a recommender model based on 231,637 recipes with 8,023 unique ingredients. Users choose an ingredient
from a recipe on the *Make This!* app and the back-end of the app gets every variation of that ingredient in the data and the top-10 
recommended matches for each of those variations. It sorts those results by the highest cosine similarity value and returns the top three.


## Notebooks in this repo:
- [edamam api](/notebooks/edamam_recipe_api.ipynb): exploring the recipe api, looking at what are required parameters and how to dig into the json
response to get the information I want to display on the app
- [recipe database](/notebooks/recipe_database.ipynb): initial EDA on the Kaggle dataset<sup>1</sup> from Food.com.
- [model recipe database](/notebooks/model_recipe_database.ipynb): data exploration and initial pass on using the Kaggle/Food.com data with a clustering model. 
- [cluster model trials](/notebooks/cluster_model_trials.ipynb): trials of kmeans, dbscan, birch and agglomerative clustering models, using a few different
ways to subset the data. Ends with the cosine similarity recommender


## Data
The "Food.com Recipes and Interacations" dataset has several tables of recipes and user interactions. I used three of their recipe tables:
- "RAW_recipes.csv" which has human-readable details of 231,637 recipes
- "PP_recipes.csv" which has pre-processed versions of those recipes. Each ingredient has an id and the text in fields like ingredient labels and tags
has been encoded using the GPT subword tokenizer.
- "ingr_map.pkl" which has the mapping from the ingredient id in the processed recipes to the human-readable label in the raw recipes.


## Methodology
### Filter & process data
I filtered the recipes by the "tag" field to use only those that had been tagged as a main course. See the [tags.txt](/data/generated_data/tags.txt) for
the list of all the tags. That reduced the number of recipes from 231,637 to 96,201 and also eliminated some ingredients.

To run the clustering models, I wanted to get rid of ingredients that only appeared in a small number of of recipes. Initially, I got rid of any 
ingredient that occurred in fewer than 5 recipes (completely arbitrary threshold). Later, I used Principal Component Analysis to calculate which 
ingredients contributed the most to the variance in the data. Keeping only those that cumulatively accounted for 90% of the variance, I reduced the 
number of ingredients from 8,023 to 827.

### Clustering models
I tried four unsupervised clustering models: kmeans, dbscan, birch and agglomerative. In order to get a hint about how many clusters to set, I first 
ran scipy's `
![positive class word cloud](/images/pos_class_word_cloud.png)


## Running the app
Navigate to the "streamlit_app" folder and run `streamlit run home.py` in the terminal. The app
should automatically take you to a tab in your default browser.

## Technical notes
### Installing requirements
- From the root of this repo, run `conda deactivate` to get out of any of your existing conda environments
- Hopefully, you're running zsh with a theme that shows your active conda environment - yes?
- Run `conda env create -f env.yml`


## References
1. Food.com Recipes and Interacations. Kaggle dataset. [link](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data)
1. Neelansh Garg, Apuroop Sethupathy, Rudraksh Tuwani, Rakhi NK, Shubham Dokania, Arvind Iyer, Ayushi Gupta, Shubhra Agrawal, Navjot Singh, Shubham Shukla, Kriti Kathuria, Rahul Badhwar, Rakesh Kanji, Anupam Jain, Avneet Kaur, Rashmi Nagpal, Ganesh Bagler. (2018, 4 January) FlavorDB: a database of flavor molecules. Nucleic Acids Research [link](https://academic.oup.com/nar/article/46/D1/D1210/4559748#107188690)

## Source for external images
1. Flavor profile wheel image from [Culinart Kosher](https://cooking.marcgottlieb.com/2014/11/flavor-profile/)
2. Pressure cooker favicon for app from [here](https://www.flaticon.com/packs/cooking-178?word=cooking)
3. All external images in my presentation came from [Unsplash](https://unsplash.com/) and their specific artists' attribution is in the slides
