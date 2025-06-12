import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

# ============================
# 環境設定
# ============================

#.envファイルからapiキーを読み込む
load_dotenv()

# OpenAIクライアントを作成
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

# ============================
# 関数定義
# ============================
def generate_answer(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"あなたは親切なアシスタントです。"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def summarize_answer(answer):
    summary_prompt = f"次の文章をわかりやすく3行以内に要約してください:\n\n{answer}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system","content":"あなたは優秀な要約作成の専門家です。"},
            {"role":"user","content":summary_prompt}
        ]
    )
    return response.choices[0].message.content

def extract_keywords(answer):
    keyword_prompt = f"次の文章から重要なキーワードを5~10個、日本語の「・」区切りで抽出してください:\n\n{answer}"
    response =client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"あなたは優秀な情報整理の専門家です。"},
            {"role": "user", "content": keyword_prompt}
        ]
    )
    return response.choices[0].message.content

def classify_category(keywords, categories_list):
    categories_str = "\n".join([f"{i+1}. {cat}" for i, cat in enumerate(categories_list)])

    category_prompt = (f"""次のキーワードから、以下のカテゴリ一覧の中から最も適切なカテゴリを1つ選んでください。
必ずカテゴリの番号（数字）のみ出力してください。カテゴリ名や説明は絶対に出力しないでください。
カテゴリ一覧にないカテゴリは絶対に出力しないでください。

カテゴリ一覧:
{categories_str}

キーワード:
{keywords}
""")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは優秀な分類の専門家です。"},
            {"role": "user", "content": category_prompt}
        ]
    )

    # 生の出力を画面に表示（デバッグ用）
    #st.subheader("GPTの生の出力（デバッグ用）")
    #st.write(response.choices[0].message.content)

    # 数字を正規表現で取り出す
    match = re.search(r'\d+', response.choices[0].message.content)
    if match:
        category_number = int(match.group())
        index = category_number - 1
        if 0 <= index < len(categories_list):
            return categories_list[index]
    return "分類失敗"

# ============================
# Streamlit アプリUI
# ============================


#　タイトル
st.title("Chatgpt 質問応答ツール")

#　ユーザー入力欄
question = st.text_input("質問を入力してください:")

categories_list = [
    "技術", "ビジネス", "健康", "教育", "エンタメ",
    "天気・気象", "ニュース", "生活"
]

# ============================
# メイン処理
# ============================

if st.button("回答を生成"):
    if question:
        with st.spinner("ChatGPTに問い合わせ中..."):
            # 各処理を順番に実行
            answer = generate_answer(question)
            with st.expander("ChatGPTの回答"):
                st.write(answer)

            summary =summarize_answer(answer)
            with st.expander("要約"):
                st.write(summary)

            keywords =extract_keywords(answer)
            with st.expander("キーワード"):

                # カンマ区切りの文字列をリストに変換
                keyword_list = [kw.strip() for kw in keywords.split("・")]

                # リスト表示
                for kw in keyword_list:
                    st.text(f"・ {kw}")

            category = classify_category(keywords, categories_list)
            with st.expander("カテゴリ"):
                st.write(category)
    else:
         # 質問が未入力の場合の警告
        st.warning("質問を入力してください。")