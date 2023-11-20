import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('prep_data.csv', parse_dates=['date'])
result = pd.read_csv('result.csv', parse_dates=['date'])

df['date'] = df['date'].dt.date
result['date'] = result['date'].dt.date

col1, col2, col3, col4 = st.columns(4)
with col1:
    country = st.selectbox('Country', options=result['country'].unique())
with col2:
    area = st.selectbox('Area', options=result[result['country']==country]['area'].unique())
with col3:
    size = st.selectbox('Size', options=result[(result['country']==country) & (result['area']==area)]['size'].unique())
with col4:
    date = st.date_input('Date')

res1, res2 = st.columns(2)
with res1:
    st.subheader("Result")
with res2:
    to_usd = st.toggle('Show in USD')

currency = {
    "INDONESIA" : "IDR",
    "CHINA" : "CNY",
    "INDIA" : "INR",
    "ECUADOR" : "USD",
    "THAILAND" : "THB",
    "VIETNAM" : "VND"
}

if to_usd:
    price = 'price_usd'
    sign = "USD"
else:
    price = 'price_origin'
    sign = currency[country]
pred = result.loc[
    (result['country'] == country) 
    & (result['area'] == area)
    & (result['size'] == size)
    & (result['date'] == date), [price]].values[0][0]

st.subheader(f'{sign} {pred:,.2f}')