#Libraries 
import util as utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from datetime import datetime
from tqdm import tqdm
import yaml
import json
import pandas as pd
import seaborn as sns
import copy
import hashlib

def load_train_feng(params: dict) -> pd.DataFrame:
    # Load train set
    x_train = utils.pickle_load(params["train_feng_set_path"][0])
    y_train = utils.pickle_load(params["train_feng_set_path"][1])

    return x_train, y_train

def load_valid(params: dict) -> pd.DataFrame:
    # Load valid set
    x_valid = utils.pickle_load(params["valid_feng_set_path"][0])
    y_valid = utils.pickle_load(params["valid_feng_set_path"][1])

    return x_valid, y_valid

def load_test(params: dict) -> pd.DataFrame:
    # Load tets set
    x_test = utils.pickle_load(params["test_feng_set_path"][0])
    y_test = utils.pickle_load(params["test_feng_set_path"][1])

    return x_test, y_test

def time_stamp():
    return datetime.now()

def create_log_template():
    # Column name
    logger = {
        "model_name" : [],
        "model_uid" : [],
        "training_time" : [],
        "training_date" : [],
        "performance" : [],
        "f1_avg" : [],
        "data_configurations" : [],
    }

    return logger

def training_log_updater(current_log, log_path):
    current_log = current_log.copy()

    # Log path
    log_path = config["training_log_path"]

    # Open existing log file
    try:
        with open(log_path, "r") as file:
            last_log = json.load(file)
        file.close()

    # Make a new log file if there's no log file/file not found
    except FileNotFoundError as ffe:
        with open(log_path, "w") as file:
            file.write("[]")
        file.close()
        with open(log_path, "r") as file:
            last_log = json.load(file)
        file.close()
    
    # Append current log entry to existing log file
    last_log.append(current_log)

    # Dump log file to designated path
    with open(log_path, "w") as file:
        json.dump(last_log, file)
        file.close()

    return last_log

def create_model_object():

    # Create model object
    svm_baseline = SVC()
    rf_baseline = RandomForestClassifier()
    knn_baseline = KNeighborsClassifier()

    # Store model in a dictionary
    list_of_model = {
    "smote" : [
        { "model_name": svm_baseline.__class__.__name__, "model_object": svm_baseline, "model_uid": ""},
        { "model_name": rf_baseline.__class__.__name__, "model_object": rf_baseline, "model_uid": ""},
        { "model_name": knn_baseline.__class__.__name__, "model_object": knn_baseline, "model_uid": ""}
        ]
    }

    return list_of_model

def train_eval_model(list_of_model, prefix_model_name, x_train, y_train, data_configuration_name, x_valid, y_valid, log_path):

    list_of_model = copy.deepcopy(list_of_model)
    # Make log file column name
    logger = create_log_template()

    # Train all models stored in the list of model
    for model in tqdm(list_of_model):    
        model_name = prefix_model_name + "-" + model["model_name"]

        # Train
        start_time = time_stamp()
        model["model_object"].fit(x_train, y_train)
        finished_time = time_stamp()

        # Measure the training time
        elapsed_time = finished_time - start_time
        elapsed_time = elapsed_time.total_seconds()

        # Predict
        y_pred = model["model_object"].predict(x_valid)
        performance = classification_report(y_valid, y_pred, output_dict = True)

        # Create Unique ID
        plain_id = str(start_time) + str(finished_time)
        chiper_id = hashlib.md5(plain_id.encode()).hexdigest()

        model["model_uid"] = chiper_id

        # Add information to logfile
        logger["model_name"].append(model_name)
        logger["model_uid"].append(chiper_id)
        logger["training_time"].append(elapsed_time)
        logger["training_date"].append(str(start_time))
        logger["performance"].append(performance)
        logger["f1_avg"].append(performance['macro avg']["f1-score"])
        logger["data_configurations"].append(data_configuration_name)

    training_log = training_log_updater(logger, log_path)

    return training_log, list_of_model

def training_log_to_df(training_log):
    training_res = pd.DataFrame()

    for log in tqdm(training_log):
        training_res = pd.concat([training_res, pd.DataFrame(log)])
    
    training_res.sort_values(["f1_avg", "training_time"], ascending = [False, True], inplace = True)
    training_res.reset_index(inplace = True, drop = True)
    
    return training_res

def get_best_model(training_log_df, list_of_model):
    model_object = None

    # sort model with highest f1 score
    best_model_info = training_log_df.sort_values(["f1_avg", "training_time"], ascending = [False, True]).iloc[0]
    
    for configuration_data in list_of_model:
        for model_data in list_of_model[configuration_data]:
            if model_data["model_uid"] == best_model_info["model_uid"]:
                model_object = model_data["model_object"]
                break
    
    if model_object == None:
        raise RuntimeError("The best model not found in your list of model.")
    
    return model_object

def make_params_for_rf():

    # Make parameter list for random forest
    dist_params_rf = {
            "criterion" : ["gini", "entropy"],
            "n_estimators" : [10, 20, 30, 50, 100, 500],
            "min_samples_split" : [2, 4, 6, 10, 15, 20, 25],
            "min_samples_leaf" : np.arange(2, 31),
            "max_features": ['sqrt', 'log2'],
            "max_depth": range(1,20)}
    
    return dist_params_rf

def hyperparameter_tuning():

    # call function to get parameter list
    parameter = make_params_for_rf()

    # Tuning with randomized search
    rf_enh = RandomizedSearchCV(rf_baseline,
                          param_distributions = parameter,
                          cv = 3,
                          n_jobs = -1,
                          scoring = 'f1_macro',
                          verbose = 3
                          )
    
    return rf_enh

def append_tuned_to_list():
    list_of_model["smote"].append({"model_name": rf_enh.__class__.__name__ + "-" + rf_enh.estimator.__class__.__name__, "model_object": copy.deepcopy(rf_enh), "model_uid": ""})

    return

def fit_tuning_to_model(input_x, input_y):
    # fit best parameter to model
    fitted_model = rf_enh.fit(input_x, input_y)

    return fitted_model


# Run tasks
if __name__ == "__main__" :
    # 1. Load config file
    config = utils.load_config()

    # 2. Load set data
    x_train, y_train = load_train_feng(config)
    x_valid, y_valid = load_valid(config)
    x_test, y_test = load_test(config)

    # 3. Train baseline
    list_of_model = create_model_object()

    training_log, list_of_model_sm = train_eval_model(
    list_of_model["smote"],
    "baseline_model",
    x_train,
    y_train,
    "smote",
    x_valid,
    y_valid,
    "log/training_log.json")

    list_of_model["smote"] = copy.deepcopy(list_of_model_sm)

    # 4. Select best performing model from baseline
    training_res = training_log_to_df(training_log)

    model = get_best_model(training_res, list_of_model)
    
    #. 5. Hyperparameter tuning
    rf_enh = hyperparameter_tuning()
    
    training_log, list_of_model_smote_hyp = train_eval_model(
    [list_of_model["smote"][-1]],
    "hyperparams",
    x_train,
    y_train,
    "smote",
    x_valid,
    y_valid,
    "log/training_log.json")

    # 6. Get final model
    training_res = training_log_to_df(training_log)

    final_model = get_best_model(training_res, list_of_model)

    # 4. Dump model
    utils.pickle_dump(final_model, config["production_model_path"])