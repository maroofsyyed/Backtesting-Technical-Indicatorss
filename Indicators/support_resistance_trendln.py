"""
This file contains functions to find support and resistances with help of finding local maxima and minima as pivot points.
"""

import trendln
import matplotlib.pyplot as plt


def get_support_resistance(data, plot_fig=True, numbest=2, return_all=False):
    """
    Calculating Support and resistances from the given data, using just close prices.
    Plotting is also feasible.
    :param close_data: The Dataframe object with market data
    :param plot_fig: Whether to plot the figure with numbest number of best describing supports and resistances
    :param numbest: Number of supports and  resisances to take into account from the top performing ones
    :param return_all: Whether to return all the the supports and resistances found
    :return: returns list of all supports, list of all resistances, each of size numbest if return_all is False, else
             will return all of them found.
    """
    close_data = data['close'].values
    mins, maxs = trendln.calc_support_resistance(close_data, accuracy=8)
    all_minimas, all_minimas_line, supports, window_supports = mins
    all_maximas, all_maximas_line, resistances, window_resistances = mins
    print(f'Total supports lines found: {len(supports)}')
    print(f'Total resistances lines found: {len(supports)}')
    if plot_fig:
        fig = trendln.plot_support_resistance(close_data, accuracy=8, numbest=numbest)
        plt.show()

    if return_all:
        return supports, resistances

    return supports[:numbest], resistances[:numbest]
