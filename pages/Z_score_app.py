# Bulid Streamlit app
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas_datareader
import yfinance as yf
from pandas_datareader import data as pdr
from numpy.core.fromnumeric import sort
import datetime
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
# Set the app title 
st.title('Welcone to my anomaly detection app')
st.title('based on Z score') 
# Add a welcome message 
st.write('Sell call options strategy') 
st.image("G:/My Drive/Colab Notebooks/Streamlit_app/pages/skewness.png")
st.markdown(
    """
    - Highly positively skewed: Skewness > 1
    - Moderately positively skewed: 0.5 < Skewness ≤ 1
    - Approximately symmetric: -0.5 ≤ Skewness ≤ 0.5
    - Moderately negatively skewed: -1 ≤ Skewness < -0.5
    - Highly negatively skewed: Skewness < -1        


    """
            )

#
#     Skewness = Mean – Mode
#     Positive Skewness (Right Skew) : Mean > Median > Mode
#     Negative Skewness (Left Skew)  : Mean < Median < Mode          
#     Skewness=0 : perfectly symmetric distribution where the data is evenly balanced on both sides of the mean
#     Skewness>0 : it suggests a positively skewed distribution where the tail on the right side is longer or fatter, and the majority of data points are concentrated on the left side of the mean.  
#     Skewness<0 : it indicates a negatively skewed distribution where the tail on the left side is longer or fatter, and the majority of data points are concentrated on the right side of the mean.
#     we prefer negative skewness
#
#
#

import yfinance as yf
import pandas as pd
from scipy.stats import skew, kurtosis

etfs = ["CNDX.L","CSPX.L", "IUIT.L","IUFS.L","IWRD.L","ISEU.L","LSEG.L","IBIT","SOXX","IVW","IETC","IXN"]
z_score_list = []
current_price_list = []
skewness_list = []
kurtosis_list = []

for etf in etfs:
    # Get historical data for the last month
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(months=1)  # Last month's data
    data = yf.download(etf, start=start_date, end=end_date)["Adj Close"]

    # Calculate mean and standard deviation for the last month
    mean_last_month = data.mean()
    std_last_month = data.std()

    # Calculate skewness and kurtosis for the last month
    skewness_last_month = skew(data)
    kurtosis_last_month = kurtosis(data)
    skewness_list.append(round(skewness_last_month, 2))
    kurtosis_list.append(round(kurtosis_last_month, 2))

    # Get the most recent data point (current price)
    current_price = data.iloc[-1]
    current_price_list.append(round(current_price, 2))

    # Calculate Z score for the current price
    z_score_current_price = round((current_price - mean_last_month) / std_last_month, 2)
    z_score_list.append(z_score_current_price)

df = pd.DataFrame({
    "ETF Symbol": etfs,
    "current_price": current_price_list,
    "Z Score": z_score_list,
    "Skewness": skewness_list,
    "Kurtosis": kurtosis_list
})


st.table(df.sort_values(by='Z Score', ascending=True))