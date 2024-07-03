import pandas as pd

from src.data_anon import anonymize_data

def test_data_anon():
    data_identifiable = pd.DataFrame({
    'name': ['John Doe'],
    'email': ['john.doe@example.com'],
    'age': [30]
})

    data_expected_anonimized = pd.DataFrame({
    'name': ['Anonymous'],
    'email': ['anonymous@example.com'],
    'age': [30]
})
    
    data_actual_anonimized = anonymize_data(data_identifiable)
    assert data_expected_anonimized.equals(data_actual_anonimized)

    data_identifiable = pd.DataFrame({
    'name': ['Alice Smith','Bob Johnson'],
    'email': ['alice.smith@company.com','bob.johnson@company.com'],
    'age': [28,35],
    'employee_id': [12345,67890]
})
    
    data_expected_anonimized = pd.DataFrame({
    'name': ['Anonymous','Anonymous'],
    'email': ['anonymous@example.com','anonymous@example.com'],
    'age': [28,35],
    'employee_id': [0,0]
})
    data_actual_anonimized = anonymize_data(data_identifiable)
    assert data_expected_anonimized.equals(data_actual_anonimized)