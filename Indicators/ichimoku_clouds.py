"""
This file contains the function to calculate ichimoku clouds indicator, specially used for trend following purposes.
"""


def ichimoku_clouds(data, conversion_line_period=9, base_line_period=26, leading_span_b_period=52, displacement=26):
    """
    Ichimoku Clouds Indicator. Helpful in following trend features.
    :param data: Dataframe containing market data  features
    :param conversion_line_period: period setting for conversion line
    :param base_line_period: Base-line period window setting
    :param leading_span_b_period: Leading line periof window setting
    :param displacement: Displacement parameter
    :return: data with indicator values feature added
    """
    conversion_line = (data['high'].rolling(window=conversion_line_period).max() + data['low'].rolling(window=conversion_line_period).min()) / 2
    base_line = (data['high'].rolling(window=base_line_period).max() + data['low'].rolling(window=base_line_period).min()) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (data['high'].rolling(window=leading_span_b_period).max() + data['low'].rolling(window=leading_span_b_period).min()) / 2
    leading_span_b = leading_span_b.shift(displacement)
    data['conversion_line'] = conversion_line
    data['base_line'] = base_line
    data['leading_span_a'] = leading_span_a
    data['leading_span_b'] = leading_span_b
    return data