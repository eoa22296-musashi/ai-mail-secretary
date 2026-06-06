import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.title("AIメール秘書")

mail_text = st.text_area(
    "メール本文を入力してください",
    height=250
)

if st.button("解析する"):

    if not mail_text:
        st.warning("メール本文を入力してください")
        st.stop()

    prompt = f"""
以下のメールを解析してください。

【出力形式】

summary=要約

category=分類

reply=返信案
{mail_text}
"""

    with st.spinner("AI解析中..."):

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

st.subheader("要約")
st.info(result.split("category=")[0].replace("summary=", "").strip())

st.subheader("分類")
st.info(
    result.split("category=")[1]
    .split("reply=")[0]
    .strip()
)

st.subheader("返信案")
st.success(
    result.split("reply=")[1]
    .strip()
)