import pytest
from freight_cost.pipelines.dataprep.nodes import (
    preprocess_prices, 
    preprocess_distances, 
    preprocess_regression_table, 
    feature_engineer_regression_table, 
    split_data
)
from pandas.testing import assert_frame_equal
from pandas import DataFrame

def test_preprocess_prices():
    prices = DataFrame({
        'Flow': ['Flow1', 'Flow2'],
        'Origem': ['Origem1', 'Origem2'],
        'Destino': ['Destino1', 'Destino2'],
        'Veículo': ['Veículo1', 'Veículo2'],
        'Tarifa por Embarque': [10, 20]
    })
    processed_prices = preprocess_prices(prices)
    expected_output = DataFrame({
        'Tarifa por Embarque': [10, 20],
        'id': ['Flow1_Origem1_Destino1', 'Flow2_Origem2_Destino2'],
        'capacity': ['1', '2']
    })
    assert_frame_equal(processed_prices, expected_output)


def test_preprocess_distances():
    distances = DataFrame({
        'Fluxo': ['Flow1', 'Flow2'],
        'Estado de Origem': ['MG', 'SP'],
        'Estado de Destino': ['SP', 'MG'],
        'Distância em Km': [100, 200],
        'Origem': ['Origem1', 'Origem2'],
        'Destino': ['Destino1', 'Destino2']
    })
    processed_distances = preprocess_distances(distances)
    expected_output = DataFrame({
        'Distância em Km': [100, 200],
        'id': ['Flow1_Origem1, MG_Destino1, SP', 'Flow2_Origem2, SP_Destino2, MG'],
        'category': ['MG_SP', 'SP_MG']
    })
    assert_frame_equal(processed_distances, expected_output)
    
