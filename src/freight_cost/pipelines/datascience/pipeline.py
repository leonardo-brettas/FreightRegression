"""
This is a boilerplate pipeline 'datascience'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node 
from .nodes import train_model, evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_model,
            inputs=['regression_table_train', 'regression_table_train_target'],
            outputs='linear_regression_model',
            name='train_model_node'
        ),
        node(
            func=evaluate_model,
            inputs=['linear_regression_model', 'regression_table_test', 'regression_table_test_target'],
            outputs=None,
            name='evaluate_model_node'
        )
    ])
