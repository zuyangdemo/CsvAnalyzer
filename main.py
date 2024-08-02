import os

import streamlit as st
import pandas as pd
from utils import parse_cvs


def create_chart(input_data, input_type):
    df_data = pd.DataFrame(input_data['data'], columns=input_data['columns'])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if input_type == "bar":
        st.bar_chart(df_data)
    elif input_type == "line":
        st.line_chart(df_data)
    elif input_type == "scatter":
        st.scatter_chart(df_data)


st.title("CSV 数据高级分析工具💡")

with st.sidebar:
    openapi_api_key = st.text_input(label="请输入你的OPENAI API 密钥: ",
                                    type="password",
                                    value=os.getenv("OPENAI_API_KEY"))
    st.markdown("[获取OPENAI API KEY](https://openai.xiniushu.com/docs/guides/speech-to-text)")

csv_file = st.file_uploader(label="请上传你的CSV文件：", type="csv")
if csv_file is not None:
    st.session_state['df'] = pd.read_csv(csv_file)
    with st.expander(label="查看原始数据"):
        st.dataframe(st.session_state['df'])

query = st.text_area(label="请输入你的问题， 答案包括文字， 柱状图，折线图和散点图")

button = st.button(label="开始分析数据")

if button:
    if not openapi_api_key:
        st.info("请输入密钥")
        st.stop()

    if not query:
        st.info("你还没有问问题呢")
        st.stop()

    if "df" not in st.session_state:
        st.info("请上传需要分析的CSV文件")
        st.stop()

    with st.spinner("AI正在思考中，请稍后..."):
        response = parse_cvs(openai_api_key=openapi_api_key,
                             df=st.session_state['df'],
                             query=query)
        if "answer" in response:
            st.write(response["answer"])
        elif "table" in response:
            st.table(pd.DataFrame(response["table"]["data"],
                                  columns=response["table"]["columns"]))
        elif "bar" in response:
            create_chart(response["bar"], input_type="bar")
        elif "line" in response:
            create_chart(response["line"], input_type="line")
        elif "scatter" in response:
            create_chart(response["scatter"], input_type="scatter")
