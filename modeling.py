
import pickle

import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import balanced_accuracy_score, recall_score, precision_score, f1_score, roc_auc_score



def store_metrics(X_test: pd.DataFrame, y_test: pd.Series, scores_df: pd.DataFrame, model, label: str) -> pd.DataFrame:
    """
    took this from lesson 2.14

    Args:
        y_test: actual values for test data
        preds: predictions for test data

    Returns:
        dict with metrics on the given set of predictions & actual data
    """
    preds = model.predict(X_test)
    
    scoring_functions = [("balanced_accuracy", balanced_accuracy_score(y_test, preds)), 
                         ("f1_score", f1_score(y_test, preds)),
                         ("recall", recall_score(y_test, preds)),
                         ("precision", precision_score(y_test, preds))]
    metrics = []
    
    for pair in scoring_functions: 
        score = {
            "model_name": label,
            "score_type": pair[0],
            "score": pair[1]
        }
        metrics.append(score)
    new_scores_df = pd.DataFrame.from_dict(metrics)
    
    return pd.concat([scores_df, new_scores_df])


def store_params(model, pipe_params, label, params_dict):
    model_params = model.get_params()
    params_selected = { key: model_params[key] for key in list(model_params.keys()) if key in list(pipe_params.keys())}
    params_dict[label] = params_selected
    return params_dict


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
    select_params = {}
    for stage in pipe_tuples:
        for key, value in pipe_params.items():
            if stage[0] in key:
                select_params[key] = value
    pipeline = Pipeline(pipe_tuples)
    return GridSearchCV(pipeline, param_grid=select_params, cv=5, verbose=1, scoring="balanced_accuracy", n_jobs=-1)

