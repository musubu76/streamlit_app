import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.title('大学卒業予定者の就職状況')

df = pd.read_csv('FEH_00400402_260126104754.csv', encoding='shift_jis')

df['value'] = pd.to_numeric(df['value'], errors='coerce')

# 全体(大学):130、全体(性別):100
df_basic = df[(df['cat01_code'] == 130) & (df['cat02_code'] == 100)]

st.header('1. 就職希望率と内定率の比較')

# 年度選択
year_list = df_basic['時間軸(10月)'].unique()
selected_year = st.sidebar.selectbox('年度を選択してください', year_list)

df_year = df_basic[df_basic['時間軸(10月)'] == selected_year]

# 就職希望率:100、就職内定率:120
wish_rate = df_year[df_year['tab_code'] == 100]['value'].values[0]
offer_rate = df_year[df_year['tab_code'] == 120]['value'].values[0]

col1, col2 = st.columns(2)
col1.metric('就職希望率', f'{wish_rate}%')
col2.metric('就職内定率', f'{offer_rate}%')