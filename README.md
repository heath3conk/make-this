# Make This!

## Table of Contents
- [Problem statement](#problem-statement)
- [App description](#app-description)
- [Model summary & top-level results](#model-summary--top-level-results)
- [Navigating this repo](#navigating-this-repo)

## Problem statement
How can I decide what to cook in the evening when my executive function is low? I have ingredients and I'm an excellent 
cook but after a long work day I have no good ideas for food and nothing in my refrigerator looks appetizing.

Then, when I have some recipes in front of me, I may also want or need to be able to customize them to my preferences and make 
subsitutions while retaining the flavor profile of my favorite food. Examples:
- Suppose I really don't like olives so any recipe that features olives is unlikely to make my list unless I can understand what they
    add to the flavor so I can substitute something else for their salty/briny-ness.
- Maybe I'm lactose intolerant but love pasta dishes and pizza. What can I do to give my lasange some creamy goodness without ricotta 
    or mozzarella?

## App description
**Make This!** is an app where users enter some ingredients they have on hand and the app makes an [API call](#edamam-api) to fetch 
recipes that include those ingredients (no data science here, just an API call). The data science comes when the user chooses a 
recipe and then selects an ingredient in the recipe they don't have or don't want to include. At that point, the app recommends three
possible alternative ingredients to substitute for the one(s) the user identifies. **Make This!** is not hosted anywhere at the moment 
but you can fork this repo & [run it](#running-the-app) locally!


## Model summary & top-level results
I used cosine similarity to create a recommender model based on 231,637 recipes with 8,023 unique ingredients (see the [data](#data) 
section for more details). Users choose an ingredient from a recipe on the **Make This!** app and the back-end of the app gets every 
variation of that ingredient in the data and the top-10 recommended matches for each of those variations. It sorts those results by 
the highest cosine similarity value and returns the top three.

With an unsupervised model, there's no train-test split with data set aside to measure the model's effectiveness. Instead, you need
someone with domain knowledge (me) to evaluate the results. In its current iteration, the cosine similarity model is only somewhat
effective, offering reasonable substitution recommendations for some ingredients and outlandish recommendations for others.

See the [sample results](#sample-results) section for some good and bad recommendations.
See the [future work](#future-work) section for possible model improvements.

Jump to [table of contents](#table-of-contents)

## Navigating this repo
### Jupyter notebooks
At the top of each notebook, I've provided a brief summary of its purpose and a list of the sections in the notebook. You can't
use hyperlinks to move around in jupyter notebooks but you can search by the items in those lists to jump to the section you want.
- [edamam recipe api](/notebooks/edamam_recipe_api.ipynb): exploring the recipe api<sup>1</sup>, figuring out which parameters are 
required and how to dig into the json response to get the information I want to display on the app. Sample JSON response is 
[here](/sample_response.json); the ingredients I sent to the API were "cherry tomatoes, sourdough bread".
- [EDA recipe database](/notebooks/eda_recipe_database.ipynb): initial EDA on the Kaggle dataset<sup>2</sup> from Food.com. Includes
references to some articles about tokenizing the recipe data<sup>3,4</sup>.
- [model recipe database](/notebooks/model_recipe_database.ipynb): data exploration and initial pass on using the Kaggle/Food.com data 
with a KMeans model to cluster recipes. Also uses that model to predict which cluster a new recipe (from the Edamam API).
- [cluster model trials](/notebooks/cluster_model_trials.ipynb): trials of kmeans, dbscan, birch and agglomerative clustering models, 
using a few different ways to subset the data. Ends with the cosine similarity recommender


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

## Sample results


## Other potential approaches
### Clustering models
I tried four unsupervised clustering models: kmeans, dbscan, birch and agglomerative. At first, I was setting the number of clusters to try somewhat randomly, ranging from 3? to 100?. My very first attempt, with a kmeans model, set `n_clusters=12` which had a silhouette score of 0.17. 

In order to get a hint about how many clusters to set, I first 
ran scipy's `dendogram` function:

![dendrogram](/images/scipy_dendrogram.png)

### Future work


## Running the app
Navigate to the "streamlit_app" folder and run `streamlit run home.py` in the terminal. The app
should automatically take you to a tab in your default browser.

### Edamam API


## Technical notes
### Installing requirements
- From the root of this repo, run `conda deactivate` to get out of any of your existing conda environments
- Hopefully, you're running zsh with a theme that shows your active conda environment - yes?
- Run `conda env create -f env.yml`


## References
1. [Swagger docs](https://developer.edamam.com/edamam-docs-recipe-api) for Edamam recipe search API
2. Food.com Recipes and Interacations. Kaggle dataset. [link](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions/data)
3. Dash, Ajit. (May 21, 2023) Unlocking the Power of Tokens: Optimizing Token Usage in GPT for Efficient Text Processing. [link](https://techcommunity.microsoft.com/t5/healthcare-and-life-sciences/unlocking-the-power-of-tokens-optimizing-token-usage-in-gpt-for/ba-p/3826665)
4. Khanna, Chetna. (August 13, 2021) Byte-Pair Encoding: Subword-based tokenization algorithm. [link](https://towardsdatascience.com/byte-pair-encoding-subword-based-tokenization-algorithm-77828a70bee0)
1. Neelansh Garg, Apuroop Sethupathy, Rudraksh Tuwani, Rakhi NK, Shubham Dokania, Arvind Iyer, Ayushi Gupta, Shubhra Agrawal, Navjot Singh, Shubham Shukla, Kriti Kathuria, Rahul Badhwar, Rakesh Kanji, Anupam Jain, Avneet Kaur, Rashmi Nagpal, Ganesh Bagler. (2018, 4 January) FlavorDB: a database of flavor molecules. Nucleic Acids Research [link](https://academic.oup.com/nar/article/46/D1/D1210/4559748#107188690)

## Source for external images
1. Flavor profile wheel image from [Culinart Kosher](https://cooking.marcgottlieb.com/2014/11/flavor-profile/)
2. Pressure cooker favicon for app from [here](https://www.flaticon.com/packs/cooking-178?word=cooking)
3. All external images in my presentation came from [Unsplash](https://unsplash.com/) and their specific artists' attribution is in the slides
