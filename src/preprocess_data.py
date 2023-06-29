'''
Dataframe cleaning and feature engineering
'''
import numpy as np
import pandas as pd
import click
from box import ConfigBox
from pathlib import Path

from utils.load_params import load_params
from utils.logger import create_logger


def preprocess_df(name: str, params: ConfigBox) -> pd.DataFrame:
    '''
    Clean dataframe + feature engineering
    '''
    # Read cleaning params from config
    TEMP_DATA_PATH = Path(params.base.temp_data_path)
    PROCESSED_DATA_PATH = Path(params.base.processed_data_path)

    MAX_TRIP_DISTANCE = params.preprocess.max_trip_distance
    MIN_TRIP_DURATION = params.preprocess.min_trip_duration
    MAX_TRIP_DURATION = params.preprocess.max_trip_duration
    MAX_AVG_TRIP_SPEED = params.preprocess.max_avg_trip_speed
    MIN_FARE_AMOUNT = params.preprocess.min_fare_amount

    filename = name + '.feather'
    df = pd.read_feather(TEMP_DATA_PATH / filename)

    # Create trip duration from timestamps and avg trip speed
    df['trip_duration'] = \
        (df.tpep_dropoff_datetime - df.tpep_pickup_datetime).dt.seconds / 60
    df['avg_trip_speed'] = \
        df.trip_distance / df.trip_duration * 60

    # Fill missing values
    df.passenger_count = df.passenger_count.fillna(1)

    # Replace NaN and inf values in avg_trip_speed columns with 0
    df.avg_trip_speed = df.avg_trip_speed.fillna(0)
    df.replace([np.inf, -np.inf], 0, inplace=True)

    # Clean dataframe with outlier thresholds
    if params.preprocess.drop_outliers:
        df = df[df.trip_duration.between(MIN_TRIP_DURATION, MAX_TRIP_DURATION)]
        df = df[df.trip_distance < MAX_TRIP_DISTANCE]
        df = df[df.avg_trip_speed < MAX_AVG_TRIP_SPEED]
        df = df[df.fare_amount > MIN_FARE_AMOUNT]

    # Create features from timestamp
    if params.preprocess.create_dt_features:
        df['pickup_day'] = df.tpep_pickup_datetime.dt.day_of_week
        df['pickup_hour'] = df.tpep_pickup_datetime.dt.hour
        df = df.drop(['tpep_pickup_datetime', 'tpep_dropoff_datetime'], axis=1)

    # Convert categorical features
    for col in ['PULocationID', 'DOLocationID', 'pickup_day', 'pickup_hour']:
        df[col] = df[col].astype('category')

    df = df.reset_index(drop=True)
    df.to_feather(PROCESSED_DATA_PATH / filename)

    return df


@click.command()
@click.option('--config', default='params.yaml')
def preprocess_data(config: str):

    params = load_params(config)

    logger = create_logger('PREPROCESS', params.base.log_level)

    # Process train dataset
    df_train_processed = preprocess_df('train', params)
    logger.info(f'Processed train dataframe with '
                f'{df_train_processed.shape[1]} columns'
                f' and {df_train_processed.shape[0]} records')

    # Process test dataset
    df_test_processed = preprocess_df('test', params)
    logger.info(f'Processed train dataframe with '
                f'{df_test_processed.shape[1]} columns'
                f' and {df_test_processed.shape[0]} records')


if __name__ == '__main__':
    preprocess_data()
