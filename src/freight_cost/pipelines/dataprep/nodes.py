"""
This is a boilerplate pipeline 'dataprep'
generated using Kedro 0.18.14
"""
from pandas import merge, DataFrame, get_dummies, concat
from sklearn.model_selection import train_test_split

def preprocess_prices(prices: DataFrame) -> DataFrame:
    prices = prices[['Flow', 'Origem', 'Destino', 'Veículo', 'Tarifa por Embarque']].copy()
    prices['id'] = prices[['Flow', 'Origem', 'Destino']].apply(lambda x: '_'.join(x), axis=1)
    prices['capacity'] = prices['Veículo'].str.extract('(\d+)', expand=False)
    prices.drop(columns = ['Flow', 'Origem', 'Destino', 'Veículo'], inplace=True)
    return prices

def preprocess_distances(distances: DataFrame) -> DataFrame:
    distances = distances[['Fluxo', 'Estado de Origem', 'Estado de Destino', 
                           'Distância em Km', 'Origem', 'Destino']].copy()
    distances['Origem'] = distances[['Origem', 'Estado de Origem']].apply(lambda x: ', '.join(x), axis=1)
    distances['Destino'] = distances[['Destino', 'Estado de Destino']].apply(lambda x: ', '.join(x), axis=1)
    distances['id'] = distances[['Fluxo', 'Origem', 'Destino']].apply(lambda x: '_'.join(x), axis=1)
    distances['category'] = distances[['Estado de Origem', 'Estado de Destino']].apply(lambda x: '_'.join(x), axis=1)
    distances.drop(columns=['Fluxo', 'Origem',
                            'Destino', 'Estado de Origem', 
                            'Estado de Destino'], inplace=True)
    return distances

def preprocess_regression_table(pre_processed_prices: DataFrame, 
                               pre_processed_distances: DataFrame) -> DataFrame:    
    def remove_outliers_using_iqr_and_std(df: DataFrame, column: str = 'Tarifa por Embarque') -> DataFrame:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        std = df[column].std()
        return df[(df[column] >= q1 - 1.5 * iqr) & 
                  (df[column] <= q3 + 1.5 * iqr) & 
                  (df[column] >= df[column].mean() - 2 * std) & 
                  (df[column] <= df[column].mean() + 2 * std)]
    
    regression_table = merge(pre_processed_prices, 
                             pre_processed_distances, 
                             on='id', how='left', 
                             validate="many_to_many")
    regression_table = regression_table.groupby('id').apply(remove_outliers_using_iqr_and_std).reset_index(drop=True)
    regression_table.dropna(inplace=True)
    regression_table.drop(columns=['id'], inplace=True)
    return regression_table

def feature_engineer_regression_table(regression_table: DataFrame) -> DataFrame:
    regression_table = concat(
        [regression_table, get_dummies(regression_table['category'], prefix='category_')],
        axis=1
        )
    regression_table.drop(columns=['category'], inplace=True)    
    regression_table['tarif'] = regression_table['Tarifa por Embarque'].astype(float)
    del regression_table['Tarifa por Embarque']
    return regression_table

def split_data(regression_table: DataFrame, 
               test_size: float = 0.2, 
               random_state: int = 42) -> tuple:
    X = regression_table.drop(columns=['tarif'])
    y = regression_table['tarif']
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
