"""
This is a boilerplate test file for pipeline 'dataprep'
generated using Kedro 0.18.14.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
import pytest
from freight_cost.pipelines.dataprep.nodes import preprocess_prices, preprocess_distances, preprocess_regression_table, feature_engineer_regression_table, split_data
from kedro.pipeline import Pipeline
import pandas as pd


def test_preprocess_prices():
    # Create a sample DataFrame for testing
    prices = pd.DataFrame({
        'Flow': ['Flow1', 'Flow2'],
        'Origem': ['Origem1', 'Origem2'],
        'Destino': ['Destino1', 'Destino2'],
        'Veículo': ['Veículo1', 'Veículo2'],
        'Tarifa por Embarque': [10, 20]
    })
    # Call the function to preprocess the prices DataFrame
    processed_prices = preprocess_prices(prices)

    # Assert the expected output
    expected_output = pd.DataFrame({
        'Tarifa por Embarque': [10, 20],
        'id': ['Flow1_Origem1_Destino1', 'Flow2_Origem2_Destino2'],
        'capacity': ['1', '2']
    })
    pd.testing.assert_frame_equal(processed_prices, expected_output)

def test_preprocess_distances():
    # Create a sample DataFrame for testing
    distances = pd.DataFrame({
        'Fluxo': ['Flow1', 'Flow2'],
        'Estado de Origem': ['MG', 'SP'],
        'Estado de Destino': ['SP', 'MG'],
        'Distância em Km': [100, 200],
        'Origem': ['Origem1', 'Origem2'],
        'Destino': ['Destino1', 'Destino2']
    })
    # Call the function to preprocess the distances DataFrame
    processed_distances = preprocess_distances(distances)

    # Assert the expected output
    expected_output = pd.DataFrame({
        'Distância em Km': [100, 200],
        'id': ['Flow1_Origem1, MG_Destino1, SP', 'Flow2_Origem2, SP_Destino2, MG'],
        'category': ['MG_SP', 'SP_MG']
    })
    pd.testing.assert_frame_equal(processed_distances, expected_output)
    
