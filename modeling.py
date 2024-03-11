
import pickle

import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

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

def try_kmeans_models(cluster_range: list[int], name_modifier: str, data_df: pd.DataFrame, models_df: pd.DataFrame) -> pd.DataFrame:
    models_details = []
    
    for cluster in cluster_range:
        trial_details = {}
        trial_details["model_type"] = "kmeans"
        trial_details["clusters"] = cluster
        km = KMeans(n_clusters=cluster, n_init="auto", random_state=42)
        km.fit(data_df)
        
        sil_score = silhouette_score(data_df, km.labels_)
        trial_details["score"] = sil_score
        trial_details["inertia"] = km.inertia_
        
        modifier = "" if len(name_modifier) == 0 else f"_{name_modifier}"
        model_name = f"kmeans_{cluster}c_mains{modifier}"
        print(f"{model_name} score = {sil_score}")
        
        trial_details["name"] = model_name
        models_details.append(trial_details)
        
        with open(f"models/main_course_recipes_models/{model_name}.pkl", "wb") as f:
            pickle.dump(km, f)
    
    new_models = pd.DataFrame.from_dict(models_details)
    return pd.concat([models_df, new_models])


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

