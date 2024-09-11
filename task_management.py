import streamlit as st
import pandas as pd
from google.cloud import storage
from io import StringIO


def manage_tasks():
    st.title('Task Turtle')

    # Google Cloud Storageのクライアントを作成
    client = storage.Client()

    with st.form("cloud_storage"):
        # バケット名の入力フォーム
        bucket_name = st.text_input("バケット名", value="dk_task_list")    
        file_name = st.text_input("ファイル名", value="task.csv")
        
        if st.form_submit_button("LOAD TASK"):
            try:
                # バケットオブジェクトを取得
                bucket = client.bucket(bucket_name)
                # Blobオブジェクトを取得
                blob = bucket.blob(file_name)
                            
                st.session_state.bucket = bucket
                st.session_state.blob = blob
                
                # CSVファイルをダウンロードし、pandasで読み込み
                csv_data = blob.download_as_text()
                df = pd.read_csv(StringIO(csv_data))
                
                # DataFrameをセッションに保存
                st.session_state.df = df
                st.success("ファイルが読み込まれました。")
            except Exception as e:
                st.error(f"エラー: {e}")

    with st.form("form"):
        rank = st.number_input("優先順位", value=1)
        task = st.text_input("タスク")
        
        # タスク追加ボタン
        if st.form_submit_button("ADD TASK"):
            new_task = pd.DataFrame({"優先順位": [rank], "タスク": [task]})
            st.session_state.df = pd.concat([st.session_state.df, new_task], ignore_index=True)

    # 現在のタスクリストを表示（dfが存在する場合のみ）
    if 'df' in st.session_state:
        st.write("現在のタスク:")
        st.write(st.session_state.df)
        
        # タスクの削除
        delete_task = st.multiselect("削除するタスク", st.session_state.df["タスク"].values)
        if st.button("DELETE TASK"):
            st.session_state.df = st.session_state.df[~st.session_state.df["タスク"].isin(delete_task)]  # isin()でリストの中に含まれているかどうかを判定 falseのものだけを取り出す
            st.success("タスクが削除されました。")
        
        if st.button("SAVE TASK"):
            # 編集した DataFrame を CSV ファイルとして保存
            with open('temp_edited.csv', 'w', newline='', encoding='utf-8') as f:
                st.session_state.df.to_csv(f, index=False)
            
            # 編集した DataFrame を Google Cloud Storage にアップロード
            # アップロード先の Blob オブジェクトを作成
            upload_blob = st.session_state.bucket.blob(file_name)
            # CSV ファイルをアップロード
            upload_blob.upload_from_filename('temp_edited.csv')
            st.success("ファイルが Google Cloud Storage にアップロードされました。")
     
    else:
        st.write("タスク リストが読み込まれていません。")



