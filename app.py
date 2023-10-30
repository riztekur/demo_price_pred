import streamlit as st
import pandas as pd
import pickle

def create_time_feature(df):
    df['date'] = pd.to_datetime(df['date'])
    df['dayofmonth'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df.drop(columns=['date'], inplace=True)
    return df

df = pd.read_csv('df_prep.csv')
model = pickle.load(open('model.sav','rb'))

with st.form('input_form'):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        country = st.selectbox('Country', options=df['country'].unique())
    with col2:
        area = st.selectbox('Area', options=df['area'].unique())
    with col3:
        size = st.selectbox('Size', options=df['size'].unique())
    with col4:
        date = st.date_input('Date')

    submitted = st.form_submit_button("Predict")

if submitted:
    x = pd.DataFrame(
        [[country,area,size,date]],
        columns=['country','area','size','date']
    )

    x['country'] = pd.Categorical(x['country'], categories=df['country'].unique())
    x['area'] = pd.Categorical(x['area'], categories=df['area'].unique())
    x['size'] = pd.Categorical(x['size'], categories=df['size'].unique())

    st.dataframe(x, use_container_width=True, hide_index=True)

    x = create_time_feature(x)

    pred = model.predict(x)[0]
    st.metric("Price", f'Rp{pred:,.2f}')