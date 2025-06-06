from pymongo import MongoClient
from typing import Any, Callable
import json, time
#pythhonApp/Thread logic
def initialize_rules() -> dict[str, dict[str, Callable]]:
    from transformations import Transformations  # Local import avoids circular import issues

    return {
        "data_validation": {
            "range_checks": Transformations.range_checks,
        },
        "data_cleaning": {
            "lower_case": Transformations.lower_case,
            "capitalization_rules": Transformations.capitalization_rules,
        },
        "data_transformation": {
            "str_to_float": Transformations.str_to_float,
            "increment_value": Transformations.increment_value,    
            "trimming": Transformations.trimming,
            "year_extraction": Transformations.year_extraction,
        },
        "data_aggregation": {
            "summarization": Transformations.summarization,
            "concatenation": Transformations.concatenation,        
        },
        "anonymization": {
            "data_masking": Transformations.data_masking,
        },
        "data_standardization": {
            "renaming_columns" : Transformations.renaming_columns
        }        
    }

def extract_id(input_data: dict) -> tuple[str, Any]:
    id_keys = [key for key in input_data.keys() if "id" in key.lower()]
    selected_key = min(id_keys, key=len) if id_keys else None
    if selected_key and selected_key in input_data:
        return selected_key, input_data[selected_key]
    return "id", hash(json.dumps(input_data, sort_keys=True))

def log_applied_rules(input_id: Any, applied_rules: list[str], transformation_times: list[str]) -> dict:
    return {
        "input_id": input_id,
        "applied_rules": applied_rules or ["None"],
        "transformation_times": transformation_times or ["N/A"],
        "logged_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def load_config(config_path: str) -> dict:
    """
    Loads configuration settings from a JSON file.
    
    Parameters:
        config_path (str): The file path to the configuration JSON file. Defaults to 'config.json'.
    
    Returns:
        dict: The configuration settings loaded from the JSON file.
    """
    with open(config_path, "r") as config_file:
        return json.load(config_file)

def log_message(verbose, message):
    """
    Prints a message if verbosity is enabled.
    """
    if verbose > 0:
        print(message)

def flatten_dict(d: dict[str, Any], parent_key: str = '', sep: str = '.') -> dict[str, Any]:
    """
    Flatten nested dictionaries into a single-level dict with dotted keys.
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            # Optional: flatten first element of list if it's a dict
            items.update(flatten_dict(v[0], new_key, sep=sep))
        else:
            items[new_key] = v
    return items