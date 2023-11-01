'''
 Function is calculating the differences between consecutive rows in the specified data DataFrame for a given period.
'''


def delta(data=None, period=1):             # Working Fine
    """
    Function to calculate  difference between each row and the row behind it by n=period number of days.
    :param data: Stock Data. pd.Dataframe is applicable
    :param period: The period for which difference in features is to be obtained.
    :return: Dataframe with delta calculated for each numerical feature and initial n=period number of rows will be filled with np.nan
    """
    if data is None:
        return "You have not given data, please provide data in form of pandas dataframe"
    # elif str(type(data)) is not "<class 'pandas.core.frame.DataFrame'>":
    #     return "The input given is not of type pandas dataframe"

    return data - data.shift(period)
