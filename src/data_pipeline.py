import pandas as pd
import util as utils
import joblib
import yaml
from sklearn.model_selection import train_test_split

def read_raw_data(config: dict) -> pd.DataFrame:
    # Return raw dataset
    return pd.read_csv(config["dataset_path"])

def handle_duplicates(input_data):
    # Drop duplicates
    input_data = input_data.drop_duplicates()

    return input_data

def check_data(input_data, config):
    # Measure the range of input data
    len_input_data = len(input_data)

    # Check data types
    assert input_data.select_dtypes("int").columns.to_list() == config["int_columns"], "an error occurs in int column(s)."
    assert input_data.select_dtypes("float").columns.to_list() == config["float_columns"], "an error occurs in float column(s)."

    # Check range of data
    assert input_data[config["float_columns"][0]].between(config["range_ph"][0], config["range_ph"][1]).sum() == len_input_data, "an error occurs in temperature range."
    assert input_data[config["float_columns"][1]].between(config["range_hardness"][0], config["range_hardness"][1]).sum() == len_input_data, "an error occurs in humidity range."
    assert input_data[config["float_columns"][2]].between(config["range_solids"][0], config["range_solids"][1]).sum() == len_input_data, "an error occurs in pressure range."
    assert input_data[config["float_columns"][3]].between(config["range_chloramines"][0], config["range_chloramines"][1]).sum() == len_input_data, "an error occurs in pm1 range."
    assert input_data[config["float_columns"][4]].between(config["range_sulfates"][0], config["range_sulfates"][1]).sum() == len_input_data, "an error occurs in pm25 range."
    assert input_data[config["float_columns"][5]].between(config["range_org_carbon"][0], config["range_org_carbon"][1]).sum() == len_input_data, "an error occurs in nc05 range."
    assert input_data[config["float_columns"][6]].between(config["range_trihalomethanes"][0], config["range_trihalomethanes"][1]).sum() == len_input_data, "an error occurs in nc1 range."
    assert input_data[config["float_columns"][7]].between(config["range_turbidity"][0], config["range_turbidity"][1]).sum() == len_input_data, "an error occurs in nc25 range."
    assert input_data[config["int_columns"][0]].between(config["range_potability"][0], config["range_potability"][1]).sum() == len_input_data, "an error occurs in tvoc range."
    
 def split_data(input_data: pd.DataFrame, config: dict):
    # Split predictor and label
    x = input_data[config["predictors"]].copy()
    y = input_data[config["label"]].copy()

    # 1st split train and test
    x_train, x_test, \
    y_train, y_test = train_test_split(
        x, y,
        test_size = config["test_size"],
        random_state = 42,
        stratify = y
    )

    # 2nd split test and valid
    x_valid, x_test, \
    y_valid, y_test = train_test_split(
        x_test, y_test,
        test_size = config["valid_size"],
        random_state = 42,
        stratify = y_test
    )

    return x_train, x_valid, x_test, y_train, y_valid, y_test

if __name__ == "__main__":
    # 1. Load configuration file
    config = utils.load_config()

    # 2. Read all raw dataset
    raw_dataset = read_raw_data(config)

    # 3. Drop duplicates
    raw_dataset = handle_duplicates(raw_dataset, config)

    # 4. Data defense for non API data
    check_data(raw_dataset, config)

    # 5. Splitting train, valid, and test set
    x_train, x_valid, x_test, \
        y_train, y_valid, y_test = split_data(raw_dataset, config)

    # 6. Save train, valid and test set
    utils.pickle_dump(x_train, config["train_set_path"][0])
    utils.pickle_dump(y_train, config["train_set_path"][1])

    utils.pickle_dump(x_valid, config["valid_set_path"][0])
    utils.pickle_dump(y_valid, config["valid_set_path"][1])

    utils.pickle_dump(x_test, config["test_set_path"][0])
    utils.pickle_dump(y_test, config["test_set_path"][1])

    utils.pickle_dump(raw_dataset, config["dataset_cleaned_path"])