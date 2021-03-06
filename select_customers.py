from geopy.distance import great_circle
import pandas as pd

def check_columns(customers):
    expected_columns = {'latitude', 'longitude', 'user_id', 'name'}
    if not expected_columns.issubset(customers.columns):
        raise Exception("Invalid file, columns missing")

def select_customers(customers, office, distance):
    """
    :param customers: DataFrame containing the customers, should have the following columns: 'latitude', 'longitude', 'user_id', 'name'
    :param office: latitude and longitude of the office
    :param distance: max distance to the office in km
    :return: DataFrame with user id and name of the selected customers.
    """
    if customers.empty:
        return pd.DataFrame(columns=["user_id", "name"])

    check_columns(customers)

    customers['distance_to_office'] = customers.apply(
        lambda row: great_circle((row['latitude'], row['longitude']), office).kilometers, axis=1)

    customers_within_distance = customers.loc[customers['distance_to_office'] < distance]

    customers_id_name = customers_within_distance.loc[:, ["user_id", "name"]]

    sorted_customers = customers_id_name.sort_values(by='user_id')

    return sorted_customers
