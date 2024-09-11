import streamlit as st
import gcsfs
import pandas as pd

try:
    # secrets.toml から認証情報を読み込む
    secrets = st.secrets["google_cloud"]

    # 認証情報を使ってファイルシステムを設定
    fs = gcsfs.GCSFileSystem(
        project=secrets["project_id"],
        token={
            "type": "service_account",
            "project_id": secrets["project_id"],
            "private_key_id": secrets["private_key_id"],
            "private_key": secrets["private_key"],
            "client_email": secrets["client_email"],
            "client_id": secrets["client_id"],
            "auth_uri": secrets["auth_uri"],
            "token_uri": secrets["token_uri"],
            "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": secrets["client_x509_cert_url"],
        }
    )

    # ファイルを読み込む
    with fs.open("dk_task_list/岡山県_33202170_202402.csv") as f:
        df = pd.read_csv(f)

    # データフレームを表示
    st.write(df)

except Exception as e:
    st.error(f"An error occurred: {e}")


