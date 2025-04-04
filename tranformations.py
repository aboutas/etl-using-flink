# data_cleaning
def standardize_format(data, fields):
    transformed = {k: (v.lower().strip() if k in fields and isinstance(v, str) else v) for k, v in data.items()}
    return transformed, False  # Never filters out

#data_transformation
def type_conversion(data, fields):
    transformed =  {k: float(v) if k in fields and isinstance(v, str) and v.replace('.', '', 1).isdigit() else v for k, v in data.items()}
    return transformed, False                

# anonymization
def tokenization(data, fields): 
    transformed = {k: hash(v) if k in fields and isinstance(v, (str, int)) else v for k, v in data.items()}
    return transformed, False

# data_filtering | Disable for now (not in initalize_rules), creates issue on order execution.
def row_filtering(data, fields):
    """Filters out rows where none of the given fields have a value > 100."""
    keep_row = any(k in data and isinstance(data[k], (int, float)) and data[k] > 100 for k in fields)
    return (data, not keep_row)  # If `keep_row` is False, mark for filtering

def column_filtering(data, fields):
    """Keeps only specified fields."""
    transformed = {k: v for k, v in data.items() if k in fields}
    return transformed, False  # Never filters out
