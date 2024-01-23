import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Load language files
with open('en.json') as json_file:
    en = json.load(json_file)
with open('zh_Hant.json', 'r', encoding='utf-8') as json_file:
    zh_Hant = json.load(json_file)
with open('sh_Hans.json', 'r', encoding='utf-8') as json_file:
    sh_Hans = json.load(json_file)

# Create a selectbox for language selection
languages = {
    "English": en,
    "繁體": zh_Hant,
    "簡體": sh_Hans
}

# Replace your strings in the application with the multilingual strings
st.set_page_config(
    page_title="Multipage Volatility Dashboard",
    page_icon="📈",
)
st.sidebar.image('1.png', width=100)

selected_lang = st.sidebar.selectbox("Language", options=list(languages.keys()))

# Select the texts based on the language
texts = languages[selected_lang]


st.title(texts["title"])


# User input for stock code and period

stock_code = st.sidebar.text_input(texts["enter_stock_code"], value="AAPL") 
period = st.sidebar.number_input(texts["enter_period"], value=50, step=1)
x_days = st.sidebar.number_input(texts["enter_volatility_days"], value=1, step=1)
v_alert = (st.sidebar.number_input(texts["avg_volatility_higher_or_lower"], value=0, step=1)/100)

if st.sidebar.button(texts["refresh"]):


    st.experimental_rerun()



# Set the end date as today and the start date as 180 days before today
end_date = datetime.today()
start_date = end_date - timedelta(days=1800)
# Download historical data as dataframe
def download_data(stock_code, start_date, end_date):
    data = yf.download(stock_code, start=start_date, end=end_date)
    return data

def download_data_current(stock_code):
    data_c = yf.download(stock_code, period="1d", interval="1m")
    return data_c   

data = download_data(stock_code, start_date, end_date)
data_pct = data.copy()
if data.empty:
    raise ValueError(f"{texts['no_data_error']}: {stock_code}")

#### By actual point

# Calculate the daily high and low prices
data["daily_volatility"] = data["High"] - data["Low"]
data["std_daily_volatility"] = data["daily_volatility"].rolling(period).std()
data["avg_daily_volatility"] = data["daily_volatility"].rolling(period).mean()

# Calculate the x-day high and low prices
data["x_day_high"] = data["High"].rolling(window=x_days).max()
data["x_day_low"] = data["Low"].rolling(window=x_days).min()
data["x_day_volatility"] = data["x_day_high"] - data["x_day_low"]
data["std_x_day_volatility"] = data["x_day_volatility"].rolling(period).std()
data["avg_x_day_volatility"] = data["x_day_volatility"].rolling(period).mean()

# Calculate the weekly high and low prices
start_date_wk = end_date - timedelta(days=900)
data_wk = yf.download(stock_code, start=start_date_wk, end=end_date, interval="1wk")
data_wk["weekly_volatility"] = data_wk["High"] - data_wk["Low"]
data_wk["std_weekly_volatility"] = data_wk["weekly_volatility"].rolling(period).std()
data_wk["avg_weekly_volatility"] = data_wk["weekly_volatility"].rolling(period).mean()

#### By percentage 

# Calculate the daily volatility as a percentage
data_pct["daily_volatility"] = (data_pct["High"] - data_pct["Low"]) / data_pct["Open"] * 100
data_pct["std_daily_volatility"] = data_pct["daily_volatility"].rolling(period).std()
data_pct["avg_daily_volatility"] = data_pct["daily_volatility"].rolling(period).mean()

# # Calculate the x-day volatility as a percentage
data_pct["x_day_high"] = data_pct["High"].rolling(window=x_days).max()
data_pct["x_day_low"] = data_pct["Low"].rolling(window=x_days).min()
data_pct["x_day_volatility"] = (data_pct["x_day_high"] - data_pct["x_day_low"]) / data_pct["x_day_low"] * 100
data_pct["std_x_day_volatility"] = data_pct["x_day_volatility"].rolling(period).std()
data_pct["avg_x_day_volatility"] = data_pct["x_day_volatility"].rolling(period).mean()

# Calculate the weekly volatility as a percentage in a new DataFrame
data_wk_pct = data_wk.copy()
data_wk_pct["weekly_volatility"] = (data_wk["High"] - data_wk["Low"]) / data_wk["Low"] * 100
data_wk_pct["std_weekly_volatility"] = data_wk_pct["weekly_volatility"].rolling(period).std()
data_wk_pct["avg_weekly_volatility"] = data_wk_pct["weekly_volatility"].rolling(period).mean()


data_c = download_data_current(stock_code)
current_price = data_c["Close"].iloc[-1]
update_time = data_c.index[-1]  
st.markdown(f"""
<span style="font-size: 34px; color: green;">
{texts["price"]}: {round(current_price,2)}
</span>
""", unsafe_allow_html=True)
st.write(f"{texts['last_update_time']}: ", update_time)

tab1, tab2, tab3 = st.tabs([texts["today_volatility"], texts["x_day_volatility"].format(x_days), texts["weekly_volatility"]])
with tab1:
    col1, col2 = st.columns(2)
    day_volatility = round(data["daily_volatility"].iloc[-2], 2)
    day_average_volatility = round(data["avg_daily_volatility"].iloc[-2], 2)
    day_std_volatility = round(data["std_daily_volatility"].iloc[-2], 2)
    day_high = round(data["High"].iloc[-1], 2)
    day_low = round(data["Low"].iloc[-1], 2)

    # PCT
    day_pct_volatility = round(data_pct["daily_volatility"].iloc[-2], 2)
    day_pct_average_volatility = round(data_pct["avg_daily_volatility"].iloc[-2], 2)
    day_pct_std_volatility = round(data_pct["std_daily_volatility"].iloc[-2], 2)
    daily_range_pct = round((day_high - day_low) / day_low * 100, 2)
    with col1:
        #show daily high and low different
        st.markdown(f"""
            <span style="font-size: 24px">
            {texts['today_range']}: {round(day_high - day_low,2)}
            </span>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <span style="font-size: 24px; color: green;">
            {texts['today_range']}%: {daily_range_pct}%
            </span>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <span style="font-size: 24px">
        {texts['day_high']}: {day_high}<br>
        {texts['day_low']}: {day_low}
        </span>
    """, unsafe_allow_html=True)
        
    st.write("_________________________")
    col1, col2, col3 = st.columns(3)
    with col1:
        # 1 Std Deviation
        upper_std_v_1 = day_average_volatility + (day_std_volatility * 1)
        lower_std_v_1 = day_average_volatility - (day_std_volatility * 1)
        upper_std_v_1_pct = day_pct_average_volatility + (day_pct_std_volatility * 1)
        lower_std_v_1_pct = day_pct_average_volatility - (day_pct_std_volatility * 1)
        if lower_std_v_1 < 0:
            lower_std_v_1 = 0.0   
        if lower_std_v_1_pct < 0:
            lower_std_v_1_pct = 0.0
        st.metric(label=texts["std_deviation_1"], value=f"{lower_std_v_1:.5} - {upper_std_v_1:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{lower_std_v_1_pct:.2f}% - {upper_std_v_1_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["previous_day_volatility"]}: </span>'
            f'<span style="color: blue;">{day_volatility},</span><br>'
            f'<center><span style="color: green;">{day_pct_volatility}%</span>', 
            unsafe_allow_html=True)
        

    with col2:
        # 2 Std Deviation
        upper_std_v_2 = day_average_volatility + (day_std_volatility * 2)
        lower_std_v_2 = day_average_volatility - (day_std_volatility * 2)
        upper_std_v_2_pct = day_pct_average_volatility + (day_pct_std_volatility * 2)
        lower_std_v_2_pct = day_pct_average_volatility - (day_pct_std_volatility * 2)
        if lower_std_v_2 < 0:
            lower_std_v_2 = 0.0
        if lower_std_v_2_pct < 0:
            lower_std_v_2_pct = 0.0 
        st.metric(label=texts["std_deviation_2"], value=f"{lower_std_v_2:.5} - {upper_std_v_2:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{lower_std_v_2_pct:.2f}% - {upper_std_v_2_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["average_volatility"]}: {day_average_volatility},</span><br>'f'<center><span style="color: green;">{day_pct_average_volatility}%</span>', unsafe_allow_html=True)

    with col3:
        # 3 Std Deviation
        upper_std_v_3 = day_average_volatility + (day_std_volatility * 3)
        lower_std_v_3 = day_average_volatility - (day_std_volatility * 3)
        upper_std_v_3_pct = day_pct_average_volatility + (day_pct_std_volatility * 3)
        lower_std_v_3_pct = day_pct_average_volatility - (day_pct_std_volatility * 3)
        if lower_std_v_3 < 0:
            lower_std_v_3 = 0.0
        if lower_std_v_3_pct < 0:
            lower_std_v_3_pct = 0.0
        st.metric(label=texts["std_deviation_3"], value=f"{lower_std_v_3:.5} - {upper_std_v_3:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{lower_std_v_3_pct:.2f}% - {upper_std_v_3_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["std_deviation_of_volatility"]} {day_std_volatility:.5},</span><br>'f'<center><span style="color: green;">{day_pct_std_volatility:.2f}%</span>', unsafe_allow_html=True)
        
    st.write(f"{texts['previous_day']}: ", data.index[-2])

    


with tab2:
    day_x_volatility = round(data["x_day_volatility"].iloc[-2], 2)
    day_x_average_volatility = round(data["avg_x_day_volatility"].iloc[-1], 2)
    day_x_std_volatility = round(data["std_x_day_volatility"].iloc[-1], 2)
    day_x_pct_volatility = round(data_pct["x_day_volatility"].iloc[-2], 2)
    day_x_pct_average_volatility = round(data_pct["avg_x_day_volatility"].iloc[-1], 2)
    day_x_pct_std_volatility = round(data_pct["std_x_day_volatility"].iloc[-1], 2)

    day_x_high = round(data["x_day_high"].iloc[-1], 2)
    day_x_low = round(data["x_day_low"].iloc[-1], 2)
    x_daily_range_pct = round((day_x_high - day_x_low) / day_x_low * 100, 2)
    
    col1, col2 = st.columns(2)
    with col1:
        #show daily high and low different
        st.markdown(f"""
            <span style="font-size: 24px">
            {texts['x_day'].format(x_days)}: {round(day_x_high - day_x_low,2)}
            </span>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <span style="font-size: 24px; color: green;">
            {texts['x_day'].format(x_days)}%: {x_daily_range_pct}%
            </span>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <span style="font-size: 24px">
        {texts['x_day_high'].format(x_days)}: {day_x_high}<br>
        {texts['x_day_low'].format(x_days)}: {day_x_low}
        </span>
    """, unsafe_allow_html=True)

    st.write("_________________________")


    col1, col2, col3 = st.columns(3)
    with col1:
        # 1 Std Deviation
        upper_x_std_v_1 = day_x_average_volatility + (day_x_std_volatility * 1)
        lower_x_std_v_1 = day_x_average_volatility - (day_x_std_volatility * 1)
        upper_x_std_v_1_pct = day_x_pct_average_volatility + (day_x_pct_std_volatility * 1)
        lower_x_std_v_1_pct = day_x_pct_average_volatility - (day_x_pct_std_volatility * 1)

        if lower_x_std_v_1 < 0:
            lower_x_std_v_1 = 0.0   
        if lower_x_std_v_1_pct < 0:
            lower_x_std_v_1_pct = 0.0
        st.metric(label=texts["std_deviation_1"], value=f"{lower_x_std_v_1:.5} - {upper_x_std_v_1:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{lower_x_std_v_1_pct:.2f}% - {upper_x_std_v_1_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["x_day_volatility"].format(x_days)}: </span>'
            f'<span style="color: blue;">{day_x_volatility},</span><br>'
            f'<center><span style="color: green;">{day_x_pct_volatility}%</span>', 
            unsafe_allow_html=True)
        

    with col2:
        # 2 Std Deviation
        upper_x_std_v_2 = day_x_average_volatility + (day_x_std_volatility * 2)
        lower_x_std_v_2 = day_x_average_volatility - (day_x_std_volatility * 2)
        upper_x_std_v_2_pct = day_x_pct_average_volatility + (day_x_pct_std_volatility * 2)
        lower_x_std_v_2_pct = day_x_pct_average_volatility - (day_x_pct_std_volatility * 2)
        if lower_x_std_v_2 < 0:
            lower_x_std_v_2 = 0.0
        if lower_x_std_v_2_pct < 0:
            lower_x_std_v_2_pct = 0.0
        st.metric(label=texts["std_deviation_2"], value=f"{lower_x_std_v_2:.5} - {upper_x_std_v_2:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{lower_x_std_v_2_pct:.2f}% - {upper_x_std_v_2_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["average_volatility"]}: {day_x_average_volatility},</span><br>'f'<center><span style="color: green;">{day_x_pct_average_volatility}%</span>', unsafe_allow_html=True)

    with col3:
        # 3 Std Deviation
        upper_x_std_v_3 = day_x_average_volatility + (day_x_std_volatility * 3)
        lower_x_std_v_3 = day_x_average_volatility - (day_x_std_volatility * 3)
        upper_x_std_v_3_pct = day_x_pct_average_volatility + (day_x_pct_std_volatility * 3)
        lower_x_std_v_3_pct = day_x_pct_average_volatility - (day_x_pct_std_volatility * 3)
        if lower_x_std_v_3 < 0:
            lower_x_std_v_3 = 0.0
        if lower_x_std_v_3_pct < 0:
            lower_x_std_v_3_pct = 0.0
        st.metric(label=texts["std_deviation_3"], value=f"{lower_x_std_v_3:.5} - {upper_x_std_v_3:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{lower_x_std_v_3_pct:.2f}% - {upper_x_std_v_3_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["std_deviation_of_volatility"]} {day_x_std_volatility:.5},</span><br>'f'<center><span style="color: green;">{day_x_pct_std_volatility:.2f}%</span>', unsafe_allow_html=True)
        
    st.write(f"{texts['previous_x_day'].format(x_days)}: ", data.index[-2])

    st.write("_________________________")


        
    csv = data.to_csv().encode('utf-8')
    st.download_button(
        label=texts["download_csv"],
        data=csv,
        file_name='daily_volatility.csv',
        mime='text/csv',)
    
    csv_pct = data_pct.to_csv().encode('utf-8')
    st.download_button(
        label=texts["download_csv_pct"],
        data=csv_pct,
        file_name='daily_volatility.csv',
        mime='text/csv',)
with tab3:
    week_volatility = round(data_wk["weekly_volatility"].iloc[-2], 2)
    week_average_volatility = round(data_wk["avg_weekly_volatility"].iloc[-2], 2)
    week_std_volatility = round(data_wk["std_weekly_volatility"].iloc[-2], 2)
    week_pct_volatility = round(data_wk_pct["weekly_volatility"].iloc[-2], 2)
    week_pct_average_volatility = round(data_wk_pct["avg_weekly_volatility"].iloc[-2], 2)
    week_pct_std_volatility = round(data_wk_pct["std_weekly_volatility"].iloc[-2], 2)
    week_high = round(data_wk["High"].iloc[-1], 2)
    week_low = round(data_wk["Low"].iloc[-1], 2)
    week_range_pct = round((week_high - week_low) / week_low * 100, 2)

    col1, col2 = st.columns(2)
    with col1:
        #show weekly high and low different
        st.markdown(f"""
            <span style="font-size: 24px">
            {texts['week_range']}: {round(week_high - week_low,2)}
            </span>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <span style="font-size: 24px; color: green;">
            {texts['week_range']}%: {week_range_pct}%
            </span>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <span style="font-size: 24px">
        {texts['week_high']}: {week_high}<br>
        {texts['week_low']}: {week_low}
        </span>
    """, unsafe_allow_html=True)

    st.write("_________________________")
    col1, col2, col3 = st.columns(3)
    with col1:
        # 1 Std Deviation
        week_upper_std_v_1 = week_average_volatility + week_std_volatility
        week_lower_std_v_1 = week_average_volatility - week_std_volatility
        week_upper_std_v_1_pct = week_pct_average_volatility + week_pct_std_volatility
        week_lower_std_v_1_pct = week_pct_average_volatility - week_pct_std_volatility
        if week_lower_std_v_1 < 0:
            week_lower_std_v_1 = 0.0
        if week_lower_std_v_1_pct < 0:
            week_lower_std_v_1_pct = 0.0
  
        st.metric(label=texts["std_deviation_1"], value=f"{week_lower_std_v_1:.5} - {week_upper_std_v_1:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{week_lower_std_v_1_pct:.2f}% - {week_upper_std_v_1_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["previous_week_volatility"]}: </span>'
            f'<span style="color: blue;">{week_volatility},</span><br>'
            f'<center><span style="color: green;">{week_pct_volatility}%</span>', 
            unsafe_allow_html=True)
        

    with col2:
        # 2 Std Deviation
        week_upper_std_v_2 = week_average_volatility + (week_std_volatility * 2)
        week_lower_std_v_2 = week_average_volatility - (week_std_volatility * 2)
        week_upper_std_v_2_pct = week_pct_average_volatility + (week_pct_std_volatility * 2)
        week_lower_std_v_2_pct = week_pct_average_volatility - (week_pct_std_volatility * 2)
        if week_lower_std_v_2 < 0:
            week_lower_std_v_2 = 0.0
        if week_lower_std_v_2_pct < 0:
            week_lower_std_v_2_pct = 0.0
        st.metric(label=texts["std_deviation_2"], value=f"{week_lower_std_v_2:.5} - {week_upper_std_v_2:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{week_lower_std_v_2_pct:.2f}% - {week_upper_std_v_2_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["average_volatility"]}: {week_average_volatility},</span><br>'f'<center><span style="color: green;">{week_pct_average_volatility}%</span>', unsafe_allow_html=True)

    with col3:
        # 3 Std Deviation
        week_upper_std_v_3 = week_average_volatility + (week_std_volatility * 3)
        week_lower_std_v_3 = week_average_volatility - (week_std_volatility * 3)
        week_upper_std_v_3_pct = week_pct_average_volatility + (week_pct_std_volatility * 3)
        week_lower_std_v_3_pct = week_pct_average_volatility - (week_pct_std_volatility * 3)
        if week_lower_std_v_3 < 0:
            week_lower_std_v_3 = 0.0
        if week_lower_std_v_3_pct < 0:
            week_lower_std_v_3_pct = 0.0
        st.metric(label=texts["std_deviation_3"], value=f"{week_lower_std_v_3:.5} - {week_upper_std_v_3:.5}")
        st.markdown(f'<span style="font-size: 24px; color: green;">{week_lower_std_v_3_pct:.2f}% - {week_upper_std_v_3_pct:.2f}%</span>', unsafe_allow_html=True)
        st.markdown(f'<span style="color: blue;">{texts["std_deviation_of_volatility"]} {week_std_volatility:.5},</span><br>'f'<center><span style="color: green;">{week_pct_std_volatility:.2f}%</span>', unsafe_allow_html=True)
        
    st.write(f"{texts['previous_week']}: ", data.index[-2])


    csv = data_wk.to_csv().encode('utf-8')
    st.download_button(
        label=texts["download_csv"],
        data=csv,
        file_name='daily_volatility.csv',
        mime='text/csv',)
    
    csv_pct = data_wk_pct.to_csv().encode('utf-8')
    st.download_button(
        label=texts["download_csv_pct"],
        data=csv_pct,
        file_name='daily_volatility.csv',
        mime='text/csv',)
