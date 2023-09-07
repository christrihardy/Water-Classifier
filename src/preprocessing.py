import util as utils
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

def load_dataset(config_data: dict) -> pd.DataFrame:
    # Load every set of data
    x_train = utils.pickle_load(config_data["train_set_path"][0])
    y_train = utils.pickle_load(config_data["train_set_path"][1])

    x_valid = utils.pickle_load(config_data["valid_set_path"][0])
    y_valid = utils.pickle_load(config_data["valid_set_path"][1])

    x_test = utils.pickle_load(config_data["test_set_path"][0])
    y_test = utils.pickle_load(config_data["test_set_path"][1])

    # Return 6 set of data
    return x_train, y_train, x_valid, y_valid, x_test, y_test

def smote_fit_resample(x_data, y_data):
    

    # Balance with smote
    x_train_smote, y_train_smote = SMOTE(sampling_strategy = "minority",
            random_state = 123).fit_resample(x_data, y_data)


    return x_train_smote, y_train_smote


def imputationMedian(input_data):

    input_data = input_data.copy()
    missing_column = ["ph", "Sulfate", "Trihalomethanes"]

    # Impute train set with median
    for columns in missing_column:
        median_value = input_data[columns].median()
        input_data[columns].fillna(median_value, inplace = True)

    return input_data

# Standard scaler function
def scaler_transform(X, scaler = None):
    
    if scaler != None:
        pass
    else:
        # Buat & fit encoder
        scaler = StandardScaler()
        scaler.fit(X)

    # Tranform data
    X_scaled = scaler.transform(X)
    X_scaled = pd.DataFrame(X_scaled,
                            columns = X.columns,
                            index = X.index)
    
    return X_scaled, scaler


# Run tasks
if __name__ == "__main__":
    # 1. Load configuration file
    config = utils.load_config()

    # 2. Load dataset
    x_train, y_train, x_valid, y_valid, x_test, y_test = load_dataset(config)

    # 3. Impute Missing values
    x_train_imp = imputationMedian(x_train)
    x_valid_imp = imputationMedian(x_valid)
    x_test_imp = imputationMedian(x_test)

    # 4. Balance data
    x_train_smote, y_train_smote = smote_fit_resample(x_train_imp, y_train)

    # Standardizing with scaler
    x_train_clean, scaler = scaler_transform(X = x_train_smote)
    x_test_clean, scaler = scaler_transform(X = x_test_imp)
    x_valid_clean, scaler = scaler_transform(X = x_valid_imp)

    # 5. Dump set data
    utils.pickle_dump(x_train_clean, config["train_feng_set_path"][0])
    utils.pickle_dump(y_train_smote, config["train_feng_set_path"][1])

    utils.pickle_dump(x_valid_clean, config["valid_feng_set_path"][0])
    utils.pickle_dump(y_valid, config["valid_feng_set_path"][1])

    utils.pickle_dump(x_test_clean, config["test_feng_set_path"][0])
    utils.pickle_dump(y_test, config["test_feng_set_path"][1])