# ChatGPT 質問応答ツール

このアプリは ChatGPT API を利用して、ユーザーの質問に回答し、要約・キーワード抽出・カテゴリ分類を行うツールです。  
Streamlit を使用してWebアプリ化しています。

## 特徴

- ChatGPT による自動回答
- 回答の要約生成
- 重要なキーワードの抽出（リスト形式）
- 事前定義カテゴリへの分類
- UIはExpanderで整理表示

## 使用技術

- Python 3.x
- Streamlit
- OpenAI API
- dotenv

## 使い方

1. `.env` ファイルに OpenAI API キーを設定  
    ```
    OPENAI_API_KEY=sk-xxxxxxx
    ```

2. 必要なライブラリをインストール  
    ```bash
    pip install streamlit openai python-dotenv
    ```

3. アプリを起動  
    ```bash
    streamlit run app_generate_answer.py
    ```

## 注意

`.env` ファイルは GitHub に公開しないでください（APIキーは個人情報です）。