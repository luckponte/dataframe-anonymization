import hashlib
from pandas import DataFrame


class ColumnNotFoundException(Exception):    
    pass

def _anonymize(value):
    if isinstance(value,str):
        return hashlib.sha256(value.encode()).hexdigest()
    return 0

def anonymize_data_frame(df_identifiable: DataFrame, anonymize_columns: list) -> DataFrame:
    df_anonymized = df_identifiable.copy()
    for column in anonymize_columns:
        if not column in df_identifiable.columns:
            raise ColumnNotFoundException("One or more columns set for anonymization do not exist")
        else:
            df_anonymized[column] = df_anonymized[column].apply(_anonymize)

    return df_anonymized