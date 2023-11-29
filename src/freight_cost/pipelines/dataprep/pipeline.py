"""
This is a boilerplate pipeline 'dataprep'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import preprocess_prices, preprocess_distances, preprocess_regression_table, feature_engineer_regression_table, split_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=preprocess_prices,
            inputs='prices',
            outputs='pre_processed_prices',
            name='preprocess_prices_node'
        ),
        node(
            func=preprocess_distances,
            inputs='distances',
            outputs='pre_processed_distances',
            name='preprocess_distances_node'
        ),
        node(
            func=preprocess_regression_table,
            inputs=['pre_processed_prices', 'pre_processed_distances'],
            outputs='pre_processed_regresssion_table',
            name='preprocess_regression_table_node'
        ),
        node(
            func=feature_engineer_regression_table,
            inputs='pre_processed_regresssion_table',
            outputs='regresssion_table',
            name='feature_engineer_regression_table_node'
        ),
        node(
            func=split_data,
            inputs='regresssion_table',
            outputs=['regression_table_train', 'regression_table_test', 'regression_table_train_target', 'regression_table_test_target'],
            name='split_data_node'
        )
    ])
