'''
Load dataset from parquet files as Pandas DataFrame with selected columns
and save to feather format.
'''

import pandas as pd
import click
from pathlib import Path

from utils.load_params import load_params
from utils.logger import create_logger


@click.command()
@click.option('--config', default='params.yaml')
def load_data(config: str):
    # Create ConfigBox from params.yaml
    params = load_params(config)

    RAW_DATA_PATH = Path(params.base.raw_data_path)
    TRAIN_DATASET = RAW_DATA_PATH / params.load_data.train
    TEST_DATASET = RAW_DATA_PATH / params.load_data.test
    TEMP_DATA_PATH = Path(params.base.temp_data_path)
    COLUMNS = params.load_data.columns

    logger = create_logger('DATA_LOAD', params.base.log_level)

    # Load train dataframe with selected data columns
    df_train = pd.read_parquet(TRAIN_DATASET, columns=COLUMNS)
    df_train.to_feather(TEMP_DATA_PATH/'train.feather')
    logger.info(f'Saved train dataframe with {df_train.shape[1]} columns'
                f' and {df_train.shape[0]} records')

    # Load test dataframe with selected data columns
    df_test = pd.read_parquet(TEST_DATASET, columns=COLUMNS)
    df_test.to_feather(TEMP_DATA_PATH/'test.feather')
    logger.info(f'Saved test dataframe with {df_test.shape[1]} columns'
                f' and {df_test.shape[0]} records')


if __name__ == '__main__':
    load_data()
