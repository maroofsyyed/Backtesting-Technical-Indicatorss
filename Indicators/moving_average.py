'''
Function to calculate average between each row and all the rows behind it by n=period number of days or less
'''


def moving_average(data=None, period=2):
    """
    Function to calculate average between each row and all the rows behind it by n=period number of days or less.
    :param data: Stock Data. pd.Dataframe is applicable
    :param period: The period for which average in features is to be obtained.
    :return: Dataframe with moving_average calculated for each numerical feature and initial n=period number of rows will be filled with np.nan
    """
    if data is None:
        return "You have not given data, please provide data in form of pandas dataframe"
    # elif str(type(data)) is not "<class 'pandas.core.frame.DataFrame'>":
    #     return "The input given is not of type pandas dataframe"

    return data.rolling(period).mean()
