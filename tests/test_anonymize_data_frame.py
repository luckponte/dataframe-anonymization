import hashlib
import pandas as pd
import pytest

from src.anonymize_data_frame import ColumnNotFoundException, anonymize_data_frame

def hash_string(original_list):
    return [hashlib.sha256(value.encode()).hexdigest() for value in original_list]

test_cases = [
    {
        "given": {
            "data": pd.DataFrame({
                'name': ['John Doe'],
                'email': ['john.doe@example.com'],
                'age': [30]
            }),
            "anonymize": ['name','email'],
        },
        "expect":pd.DataFrame({
            'name': hash_string(['John Doe']),
            'email': hash_string(['john.doe@example.com']),
            'age': [30]
        }),
    },
    {
        "given": {
            "data": pd.DataFrame({
                'name': ['Alice Smith','Bob Johnson'],
                'email': ['alice.smith@company.com','bob.johnson@company.com'],
                'age': [28,35],
                'employee_id': [12345,67890]
            }),
            "anonymize": ['name','email','employee_id']
        },
        "expect":pd.DataFrame({
            'name': hash_string(['Alice Smith','Bob Johnson']),
            'email': hash_string(['alice.smith@company.com','bob.johnson@company.com']),
            'age': [28,35],
            'employee_id': [0,0]
        }),
    },
    {
        "given": {
            "data": pd.DataFrame({
                'name': ['Alice Smith','Bob Johnson'],
                'email': ['alice.smith@company.com','bob.johnson@company.com'],
                'age': [28,35],
                'employee_id': [12345,67890]
            }),
            "anonymize": ['name','email']
        },
        "expect":pd.DataFrame({
            'name': hash_string(['Alice Smith','Bob Johnson']),
            'email': hash_string(['alice.smith@company.com','bob.johnson@company.com']),
            'age': [28,35],
            'employee_id': [12345,67890]
        }),
    },
    {
        "given": {
            "data": pd.DataFrame({
                'client_name': ['John Doe', 'Jane Smith', 'John Doe', 'Alice Johnson', 'Bob Brown'],
                'quotation': [100.50, 200.75, 150.25, 300.00, 250.40]
            }),
            "anonymize": ['client_name'],
        },
        "expect": pd.DataFrame({
            'client_name': hash_string(['John Doe', 'Jane Smith', 'John Doe', 'Alice Johnson', 'Bob Brown']),
            'quotation': [100.50, 200.75, 150.25, 300.00, 250.40]
        }),
    }
]

@pytest.mark.parametrize("case", test_cases)
def test_anonymize_data_frame(case):
    data_actual = anonymize_data_frame(case['given']['data'],case['given']['anonymize'])
    assert case['expect'].equals(data_actual), 'The anonymized data does not match the expected values'

def test_anonymize_data_frame_handles_missing_column_exception():
    anonymize = ['name', 'email', 'salary']
    data_given = pd.DataFrame({
                'name': ['Alice Smith','Bob Johnson'],
                'email': ['alice.smith@company.com','bob.johnson@company.com'],
                'age': [28,35],
            })
    expected = pd.DataFrame({
            'name': hash_string(['Alice Smith','Bob Johnson']),
            'email': hash_string(['alice.smith@company.com','bob.johnson@company.com']),
            'age': [28,35],
        })

    with pytest.raises(ColumnNotFoundException) as excinfo:
        actual = anonymize_data_frame(data_given, anonymize)
        
        assert str(excinfo.value) == "One or more columns set for anonymization do not exist"
        assert expected.equals(actual)