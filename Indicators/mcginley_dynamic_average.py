'''
The McGinley Dynamic indicator is a type of moving average built to improve traditional moving averages’
functionalities. It solves the problem of varying market speeds by automatically adjusting its speed
concerning the prevailing market conditions — it speeds up when the market is trending and slows down
when the market is ranging. Imagine the McGinley Dynamic Indicator as a moving average with a filter
for smoothening price data to avoid whipsaws.
'''

import numpy as np

def mcginley_dynamic_average(data=None, lookback=20, feature=None, return_list=False):
    """
    Function to calculate the McGinley Dynamic Average for each row in the data based on the specified feature.
    :param data: Stock data. pd.DataFrame is applicable.
    :param lookback: The lookback period.
    :param feature: The feature on which the McGinley Dynamic Average is calculated. It should be numerical.
    :param return_list: Boolean value indicating whether to return the entire DataFrame or just the calculated column.
    :return: DataFrame with the McGinley Dynamic Average calculated for the specified feature.
    """
    if data is None:
        raise ValueError("You have not provided data. Please provide data in the form of a pandas DataFrame.")

    if feature is None:
        raise ValueError("You have not specified the feature. Please provide the feature name as a string.")

    data1 = data.copy().reset_index()
    data1['mcginley_avg'] = np.zeros(data1.shape[0])
    data1.loc[0, 'mcginley_avg'] = data1.loc[0, feature]

    for idx in range(1, data1.shape[0]):
        if data1.loc[idx - 1, 'mcginley_avg'] == 0:
            data1.loc[idx, 'mcginley_avg'] = data1.loc[idx, feature]
        elif data1.loc[idx - 1, 'mcginley_avg'] > 0:
            data1.loc[idx, 'mcginley_avg'] = data1.loc[idx - 1, 'mcginley_avg'] + \
                ((data1.loc[idx, feature] - data1.loc[idx - 1, 'mcginley_avg']) /
                 (0.6 * lookback * (data1.loc[idx, feature] / data1.loc[idx - 1, feature]) ** 4))

    if return_list:
        return data1['mcginley_avg'].values
    else:
        return data1

