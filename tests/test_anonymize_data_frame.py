import pandas as pd
import pytest

from src.anonymize_data_frame import ColumnNotFoundException, anonymize_data_frame

test_cases = [
    {
        "data": pd.DataFrame({
            'name': ['John Doe'],
            'email': ['john.doe@example.com'],
            'age': [30]
        }),
        "anonymize": ['name','email'],
    },
    {
        "data": pd.DataFrame({
            'name': ['Alice Smith','Bob Johnson'],
            'email': ['alice.smith@company.com','bob.johnson@company.com'],
            'age': [28,35],
            'employee_id': [12345,67890]
        }),
        "anonymize": ['name','email','employee_id']
    },
    {
        "data": pd.DataFrame({
            'name': ['John Doe','Alice Smith','Bob Johnson'],
            'email': ['john.doe@company.com', 'alice.smith@company.com','bob.johnson@company.com'],
            'age': [41,28,35],
            'employee_id': [0,12345,67890]
        }),
        "anonymize": ['employee_id','name','email']
    },
    {
        "data": pd.DataFrame({
            'name': ['Alice Smith','Bob Johnson'],
            'email': ['alice.smith@company.com','bob.johnson@company.com'],
            'age': [28,35],
            'employee_id': [12345,67890]
        }),
        "anonymize": ['name','email']
    },
    {
        "data": pd.DataFrame({
            'client_name': ['John Doe', 'Jane Smith', 'John Doe', 'Alice Johnson', 'Bob Brown'],
            'quotation': [100.50, 200.75, 150.25, 300.00, 250.40]
        }),
        "anonymize": ['client_name'],
    }
]

@pytest.mark.parametrize("case", test_cases)
def test_anonymize_data_frame(case):
    df_actual = anonymize_data_frame(case['data'],case['anonymize'])
    
    for anonymized_column in case['anonymize']:
        assert not(case['data'][anonymized_column] == df_actual[anonymized_column]).any(), f'The data was not anonymized at column: {anonymized_column}.\n Given:\n{case['data'][anonymized_column]}\nGot:\n{df_actual[anonymized_column]}'
    
    for column in set(case['data'].columns) - set(case['anonymize']):
        assert (df_actual[column] == (case['data'][column])).all(), f'The data was at column: {column}.\n Given:\n{case['data'][column]}\nGot:\n{df_actual[column]}'

def test_anonymize_data_frame_handles_missing_column_exception():
    anonymize = ['name', 'email', 'salary']
    df_given = pd.DataFrame({
                'name': ['Alice Smith','Bob Johnson'],
                'email': ['alice.smith@company.com','bob.johnson@company.com'],
                'age': [28,35],
            })

    with pytest.raises(ColumnNotFoundException) as excinfo:
        anonymize_data_frame(df_given, anonymize)
    assert str(excinfo.value) == "One or more columns set for anonymization do not exist"

def test_anonymize_data_frame_keeps_fields_aggregatable():
    anonymize = ['client_name','quotation']
    df_given = pd.DataFrame({
            'client_name': ['John Doe', 'Jane Smith', 'John Doe', 'Alice Johnson', 'Bob Brown'],
            'quotation': [100.50, 200.75, 150.25, 300.00, 250.40]
        })
    
    df_actual = anonymize_data_frame(df_given, anonymize)

    for column in anonymize:
        assert df_actual[column][0] != df_actual[column][1] and \
            df_actual[column][0] != df_actual[column][3], f'All {column} fields have the same value'
        df_actual[column][0] == df_actual[column][2], f'{column} fields with the same input should yeald the same result'