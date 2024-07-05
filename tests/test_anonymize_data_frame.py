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
    data_actual = anonymize_data_frame(case['data'],case['anonymize'])
    
    for anonymized_column in case['anonymize']:
        assert not data_actual[anonymized_column].equals(case['data'][anonymized_column]), f'The data was not anonymized at column: {anonymized_column}.\n Given: {case['data'][column]}\nGot: {data_actual[column]}'
    
    for column in set(case['data'].columns) - set(case['anonymize']):
        assert data_actual[column].equals(case['data'][column]), f'The data was at column: {column}.\n Given: {case['data'][column]}\nGot: {data_actual[column]}'

def test_anonymize_data_frame_handles_missing_column_exception():
    anonymize = ['name', 'email', 'salary']
    data_given = pd.DataFrame({
                'name': ['Alice Smith','Bob Johnson'],
                'email': ['alice.smith@company.com','bob.johnson@company.com'],
                'age': [28,35],
            })

    with pytest.raises(ColumnNotFoundException) as excinfo:
        anonymize_data_frame(data_given, anonymize)
    assert str(excinfo.value) == "One or more columns set for anonymization do not exist"