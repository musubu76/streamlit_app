import streamlit as st
import pandas as pd
import plotly.express as px

st.title('大学卒業予定者の就職状況')

# st.expander
with st.expander('概要・目的'):
    st.write('概要:1996年から2025年までの大学卒業予定者における就職状況を可視化した分析ツールです。')
    st.write('目的:年度ごとの比較や、時系列での変化を分析することで、約30年間の就職状況への理解を深めます。')

df = pd.read_csv('FEH_00400402_260126104754.csv', encoding='shift_jis')

df['value'] = pd.to_numeric(df['value'], errors='coerce')

st.header('1. 年度別比較')

# st.expander
with st.expander('操作方法'):
    st.write('左側にある「1.年度設定」から、年度を選択してください。')

# 全体(大学):130、全体(性別):100
df_basic = df[(df['cat01_code'] == 130) & (df['cat02_code'] == 100)]

# 年度選択
st.sidebar.header('1.年度設定')
year_list = df_basic['時間軸(10月)'].unique()
selected_year = st.sidebar.selectbox('年度を選択してください', year_list)

df_year = df_basic[df_basic['時間軸(10月)'] == selected_year]

# 就職希望率:100、就職内定率:120
wish_rate = df_year[df_year['tab_code'] == 100]['value'].values[0]
offer_rate = df_year[df_year['tab_code'] == 120]['value'].values[0]

st.write(f'### {selected_year} 就職希望率vs内定率 (全体)')

# st.metric
col1, col2 = st.columns(2)
col1.metric('就職希望率', f'{wish_rate}%')
col2.metric('就職内定率', f'{offer_rate}%')

# 就職希望率:100、就職内定率:120、国公立:140、私立:150
st.write(f'### {selected_year} 国公立vs私立 (内定率の比較)')
df_compare = df[(df['時間軸(10月)'] == selected_year) & 
                (df['cat02_code'] == 100) & 
                (df['tab_code'] == 120) & 
                (df['cat01_code'].isin([140, 150]))]

fig_bar = px.bar(df_compare, 
                 x='学校区分', 
                 y='value', 
                 color='学校区分',
                 text_auto=True,
                 labels={'value':'内定率(%)'})
st.plotly_chart(fig_bar)

st.header('2. 区分別の時系列推移')

# st.expander
with st.expander('操作方法'):
    st.write('左側にある「2.グラフ条件設定」から、学校区分と性別を選択してください。')
    st.write('グラフの右にある「表象項目」から、表示する指標を変更できます。')
    st.write('「抽出データ」からCSVファイルをダウンロードすることができます。')

univ_options = {'全体(大学)': 130, '国公立大学': 140, '私立大学': 150}
sex_options = {'全体(性別)': 100, '男': 110, '女': 120}

st.sidebar.header('2.グラフ条件設定')
selected_univ = st.sidebar.selectbox('学校区分を選択してください', list(univ_options.keys()))
selected_sex = st.sidebar.selectbox('性別を選択してください', list(sex_options.keys()))

u_code = univ_options[selected_univ]
s_code = sex_options[selected_sex]

# 就職希望率:100、就職内定率:120
df_plot = df[(df['cat01_code'] == u_code) & 
             (df['cat02_code'] == s_code) & 
             (df['tab_code'].isin([100, 120]))]

# st.tabs
tab1, tab2 = st.tabs(['推移グラフ','抽出データ'])

with tab1:
    # 推移グラフ
    fig = px.line(df_plot, 
                  x='時間軸(10月)', 
                  y='value', 
                  color='表章項目',
                  title=f'{selected_univ}・{selected_sex}の就職状況推移',
                  markers=True,
                  labels={'value':'割合(%)'})
    st.plotly_chart(fig)

with tab2:
    # 抽出データ
    st.dataframe(df_plot[['時間軸(10月)', '表章項目', 'value']])

    # st.download_button
    csv = df_plot.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="抽出データをCSVとしてダウンロード",
        data=csv,
        file_name=f'{selected_univ}_{selected_sex}.csv',
        mime='text/csv'
    )