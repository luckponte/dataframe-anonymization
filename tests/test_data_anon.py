import hashlib
import pandas as pd
import pytest

from src.data_anon import anonymize_data

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
def test_data_anon(case):
    data_actual_anonimized = anonymize_data(case['given']['data'],case['given']['anonymize'])
    assert case['expect'].equals(data_actual_anonimized), 'The anonymized data does not match the expected values'