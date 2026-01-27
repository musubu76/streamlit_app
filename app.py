import streamlit as st
import pandas as pd
import plotly.express as px

st.title('大学卒業予定者の就職状況')

df = pd.read_csv('FEH_00400402_260126104754.csv', encoding='shift_jis')

df['value'] = pd.to_numeric(df['value'], errors='coerce')

# 全体(大学):130、全体(性別):100
df_basic = df[(df['cat01_code'] == 130) & (df['cat02_code'] == 100)]

st.header('1. 就職希望率と内定率の比較')

# 年度選択
year_list = df_basic['時間軸(10月)'].unique()
selected_year = st.sidebar.selectbox('1.年度を選択してください', year_list)

df_year = df_basic[df_basic['時間軸(10月)'] == selected_year]

# 就職希望率:100、就職内定率:120
wish_rate = df_year[df_year['tab_code'] == 100]['value'].values[0]
offer_rate = df_year[df_year['tab_code'] == 120]['value'].values[0]

# st.metric
col1, col2 = st.columns(2)
col1.metric('就職希望率', f'{wish_rate}%')
col2.metric('就職内定率', f'{offer_rate}%')

st.header('2. 区分別の時系列推移')

univ_options = {'全体(大学)': 130, '国公立大学': 140, '私立大学': 150}
sex_options = {'全体(性別)': 100, '男': 110, '女': 120}

with st.sidebar:
    st.header('2.グラフ条件設定')
    selected_univ = st.selectbox('学校区分を選択してください', list(univ_options.keys()))
    selected_sex = st.selectbox('性別を選択してください', list(sex_options.keys()))

u_code = univ_options[selected_univ]
s_code = sex_options[selected_sex]

# 就職希望率:100、就職内定率:120
df_plot = df[(df['cat01_code'] == u_code) & 
             (df['cat02_code'] == s_code) & 
             (df['tab_code'].isin([100, 120]))]

# st.tabs
tab1, tab2 = st.tabs(['推移グラフ','抽出データ'])

with tab1:
    fig = px.line(df_plot, 
                  x='時間軸(10月)', 
                  y='value', 
                  color='表章項目',
                  title=f'{selected_univ}・{selected_sex}の就職状況推移',
                  markers=True,
                  labels={'value':'割合(%)'})
    st.plotly_chart(fig)

with tab2:
    st.dataframe(df_plot[['時間軸(10月)', '表章項目', 'value']])