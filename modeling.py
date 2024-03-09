
import pickle

import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# functions for interacting with my model

def map_recipe_ingredients(response_ingr: pd.Series, map_df: pd.DataFrame) -> list[list[int]]:
    mapped_ingr = []
    # iterate through the response recipes   
    for ingr_list in response_ingr:
        codes = []
        # iterate through the list of ingredients
        for label in ingr_list:
            label = label.lower()
            # if label is generic enough, it'll match one or more rows in the "replaced" column
            replaced = map_df.loc[map_df["replaced"] == label]
            
            # if the label is more specific, it might be found in the longer description in the "raw" column
            raw = map_df.loc[map_df["raw_ingr"].str.find(label) != -1]
            if replaced.shape[0] > 0:
                code = replaced["id"].value_counts().idxmax()
            elif raw.shape[0] > 0:
                code = raw["id"].value_counts().idxmax()
            else:
                code=-1
            codes.append(code)
        mapped_ingr.append(codes)
    return mapped_ingr


def flag_ingredients(ingreds: list[list[int]], map_df: pd.DataFrame):
    flagged_recipes = []
    # iterate through the list of recipe ingredient ids
    for ing_list in ingreds:
        # iterate through the list of unique ids from mapper
        recipe_row = []
        for id_col in map_df["id"].unique():
            flag = 1 if id_col in ing_list else 0
            recipe_row.append(flag)
        flagged_recipes.append(recipe_row)
    
    return pd.DataFrame(flagged_recipes)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# functions for creating & comparing models

def train_save_best_model(pipe: Pipeline, pipe_params: dict[str, any], X_train: pd.DataFrame, y_train: pd.Series, file_path: str):
    gs = generate_gs(pipe, pipe_params)
    gs.fit(X_train, y_train)
    with open(file_path, "wb") as f:
        pickle.dump(gs.best_estimator_, f)
    print(f"saved model to {file_path}")
    return gs


def fetch_fitted_pipeline(file_path: str) -> Pipeline:
    with open(file_path, "rb") as f:
        pipeline = pickle.load(f)
    return pipeline
    

def generate_gs(pipe_tuples: list[tuple], pipe_params: dict[str, any]) -> GridSearchCV:
    print("again!")
    select_params = {}
    for stage in pipe_tuples:
        for key, value in pipe_params.items():
            if stage[0] in key:
                select_params[key] = value
    pipeline = Pipeline(pipe_tuples)
    return GridSearchCV(pipeline, param_grid=select_params, cv=5, verbose=1, scoring="balanced_accuracy", n_jobs=-1)

