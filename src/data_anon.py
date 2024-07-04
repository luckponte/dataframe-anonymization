import hashlib
from pandas import DataFrame


def anonymize(value):
    if isinstance(value,str):
        return hashlib.sha256(value.encode()).hexdigest()
    return 0

def anonymize_data(data_identifiable: DataFrame, anonymize_columns: list) -> DataFrame:
    for column in anonymize_columns:
        data_identifiable[column] = data_identifiable[column].apply(anonymize)

    return data_identifiable