"""
This is a boilerplate pipeline 'datascience'
generated using Kedro 0.18.14
"""
from pandas import DataFrame
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from logging import getLogger

def train_model(regression_table_train: DataFrame, regression_table_train_target: DataFrame) -> LinearRegression:
    poly = PolynomialFeatures(degree=1, include_bias=True)
    regression_table_train = poly.fit_transform(regression_table_train)
    regression_table_train_target = regression_table_train_target['tarif']
    model = LinearRegression().fit(regression_table_train, regression_table_train_target)
    return model

def evaluate_model(model: LinearRegression, regression_table_test: DataFrame, regression_table_test_target: DataFrame) -> DataFrame:
    poly = PolynomialFeatures(degree=1, include_bias=True)
    regression_table_test = poly.fit_transform(regression_table_test)
    y_pred = model.predict(regression_table_test)
    score = r2_score(regression_table_test_target, y_pred)
    logger = getLogger(__name__)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score)