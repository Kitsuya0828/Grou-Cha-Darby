import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st
import streamlit.components.v1 as components
import bar_chart_race as bcr
from PIL import Image
from io import StringIO
from datetime import datetime
from collections import defaultdict
import japanize_matplotlib
import plotly.graph_objects as go

# ロゴ
logo_image = Image.open('logo.png')
st.image(logo_image)

# メイン画像
main_image = Image.open('mainimg.png')
st.image(main_image)

"""
# 遊び方

以下の手順で、誰でも簡単に**バーチャートレース（ぬるぬる動くグラフ）**を作ることができます。

1. LINEのトーク履歴をtxtファイル形式で保存する（所要時間：1分）＜方法は[コチラ]("https://appllio.com/line-talk-history-send-mail")＞
2. 保存したtxtファイルをアップロードする（所要時間：30秒）
3. お好みでカスタマイズして完成！（所要時間：30秒）

# さっそく遊んでみる
LINEトーク履歴（txtファイル）を選択してください
"""
uploaded_file = st.file_uploader("""※期間が1年以上になると動画処理が終わらない可能性があります""",type="txt",)
st.markdown("**（画面左上からサイドバーを開くと自由にカスタマイズできます）**")
"""
---
"""


#####サイドバー#####
st.sidebar.markdown("# ⚙️カスタマイズオプション")

st.sidebar.markdown("### 【データフレーム】")
df_category = st.sidebar.radio("データフレームの種類を選択してください", ('標準', '累積和','標準<markdown>', '累積和<markdown>'))

st.sidebar.markdown("### 【折れ線グラフ】")
line_title = st.sidebar.text_input('表示タイトル', 'グループチャット発言回数の推移')
line_category = st.sidebar.radio("折れ線グラフの種類を選択してください", ('累積和','標準'))

st.sidebar.markdown("### 【ヒートマップ】")
heat_title = st.sidebar.text_input('表示タイトル', 'グループチャット発言回数')
heat_colorscale = st.sidebar.radio("カラースケールを選択してください", ('Defalut','Blackbody','Bluered','Blues','Earth','Electric','Greens','Greys','Hot','Jet','Picnic','Portland','Rainbow','RdBu','Reds','Viridis','YlGnBu','YlOrRd'))
st.sidebar.markdown("### 【バーチャートレース】")
bcr_title = st.sidebar.text_input('表示タイトル', 'グループチャット発言回数ランキング')
n_bars = st.sidebar.slider('ランキング上位表示人数', min_value=1,max_value=20,value=2)
st.sidebar.write('↪',n_bars, '人')
from_date = str(st.sidebar.date_input('表示期間(開始)',value=datetime(2000,1,1)))
to_date = str(st.sidebar.date_input('表示期間（終了）',value=datetime(2100,12,31)))
steps_per_period = st.sidebar.slider('ピリオド毎のステップ数', min_value=1,max_value=50,value=10)
st.sidebar.write('↪',steps_per_period)
period_length = st.sidebar.slider('1ピリオドの長さ', min_value=100,max_value=1000,value=500)
st.sidebar.write('↪',period_length)
#####サイドバー#####


if uploaded_file is not None:  # ファイルがアップロードされた場合

    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    tmp_names = defaultdict(int)   # グループメンバーの名前を格納するリスト
    stringio_list = []
    # グループの人数をカウント
    for i,data in enumerate(stringio):
        data_list = list(map(str,data.split()))  # txtファイルの各行のデータをリスト化
        stringio_list.append(data_list)
        if i < 2:   #2行目までのタイトルと保存日時はスキップ
            continue
        if len(data_list) <= 2:  # 空白行&日付行はスキップ
            continue
        name = data_list[1]
        if not data_list[0][0].isdigit() or name in ['Group','You','☎']:  # システムメッセージ等を除外する
            continue
        tmp_names[name] += 1    # メンバーリストに追加
    names = [key for key in tmp_names.keys() if tmp_names[key] >= 5]  # 発言回数5回以上のメンバーだけ残す
    chat_count = []    # 日付ごとの発言カウントを格納するリスト
    daily_data = []    # 1日のデータを格納するリスト
    for i,data_list in enumerate(stringio_list):

        if i < 2:   #2行目までのタイトルと保存日時はスキップ
            continue

        if len(data_list) < 1:    # 空白行はスキップ
            continue
        
        if len(data_list[0])>=10 and data_list[0][4]=='/' and data_list[0][7]=='/':  # 日付の行
            if daily_data:
                if daily_data[0] <= to_date:    # 表示期間以内
                    chat_count.append(daily_data)     # 日付の行が来たタイミングで先日の発言回数をchat_countリストに追加
                else:    # 表示期間外
                    break

            date = data_list[0].replace('/','-')[:10]   # 2020/01/01 ---> 2020-01-01　（日付表示を変更）
            if from_date <= date:  # 表示期間内
                daily_data = [date]+[0]*(len(names))     # その日のデータを格納するリストを用意  ['2020-01-01',0,0,0,...]
                continue
            else:
                daily_data = None
        
        if len(data_list) >= 3:
            name = data_list[1]
            if name in names and daily_data:   # 発言表示の行の場合
                daily_data[names.index(name)+1] += 1    # 発言者ごとの発言数をインクリメントする
    if daily_data and daily_data[0] <= to_date:
        chat_count.append(daily_data)
    chat_count = np.array(chat_count)  # 発言カウントリストをnumpy配列に変換
    original_df = pd.DataFrame(chat_count)
    original_df.columns = ['日付'] + names  # 列インデックスに氏名を指定
    original_df = original_df.set_index('日付')  # 行インデックスに日付を指定
    original_df = original_df.astype(dict(zip(names,['int64']*len(names))))  # カウントした発言数を整数(int64)型に変換
    chat_count[:,1:len(names)+1] = np.cumsum(np.array(chat_count[:,1:len(names)+1],dtype=int),axis=0)  # 日付以外の列に関して、縦方向に累積和を取る
    df = pd.DataFrame(chat_count)
    df.columns = ['日付'] + names  # 列インデックスに氏名を指定
    df = df.set_index('日付')  # 行インデックスに日付を指定
    df = df.astype(dict(zip(names,['int64']*len(names))))  # カウントした発言数を整数(int64)型に変換
    
    # データフレーム
    st.write(f'## データフレーム（{df_category}）')
    if df_category == '標準':
        st.write(original_df)
    elif df_category == '累積和':
        st.write(df)
    elif df_category == '標準<markdown>':
        st.markdown(original_df.to_markdown())
    else:
        st.markdown(df.to_markdown())
    
    # 折れ線グラフ
    st.write(f'## 折れ線グラフ（{line_category}）')
    pd.options.plotting.backend = "plotly"
    if line_category == "標準":
        fig_line = original_df.plot(title=line_title, template="simple_white",
                    labels=dict(index="日付", value="回数", variable="メンバー"))
    else:
        fig_line = df.plot(title=line_title, template="simple_white",
                    labels=dict(index="日付", value="回数", variable="メンバー"))
    st.write(fig_line)

    # ヒートマップ
    st.write('## ヒートマップ')
    if heat_colorscale == 'Defalut':
        heat_colorscale = None
    fig_heat = go.Figure(data=go.Heatmap(
        z=original_df,
        x=names,
        y=list(df.index),
        colorbar=dict(title='回数'),
        colorscale=heat_colorscale,
        hoverongaps = True)
    )
    fig_heat.update_xaxes(title="メンバー")
    fig_heat.update_yaxes(title="日付")
    fig_heat.update_layout(title=heat_title)
    st.write(fig_heat)

    # バーチャートレース
    st.write('## バーチャートレース')
    html = bcr.bar_chart_race(df,title=bcr_title,n_bars=n_bars,figsize=(4,3),steps_per_period=steps_per_period,period_length=period_length)
    components.html(html._repr_html_(),width=10000,height=7500)

# 注意事項
st.markdown("※本サービスは、アップロードされたLINEトーク履歴（個人情報を含む）を使用して処理を行います。アップロードされた情報は保存されることなく処理が終了した時点で破棄されますが、心配な方は利用を控えてください。")
