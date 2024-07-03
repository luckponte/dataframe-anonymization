from pandas import DataFrame


def anonymize_data(data_identifiable: DataFrame) -> DataFrame:
    data_identifiable['name'] = 'Anonymous'
    data_identifiable['email'] = 'anonymous@example.com'

    data_identifiable['employee_id'] = 0
    return data_identifiable