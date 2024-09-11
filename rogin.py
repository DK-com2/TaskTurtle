import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from task_management import manage_tasks  # 新しく作成したファイルをインポート

# 'config.yaml' ファイルを読み込む
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# プレーンテキストのパスワードを一度ハッシュ化する
# Hasher.hash_passwords(config['credentials'])

# 認証機能を作成する
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# ログインを処理する
authenticator.login()

# 認証状態に応じた処理
if st.session_state['authentication_status']:
    # ログイン成功時の処理
    authenticator.logout()  # ログアウトボタンを表示
    st.write(f'Welcome *{st.session_state["name"]}*')  # ユーザー名を表示
    manage_tasks()  # タスク管理の関数を呼び出す

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')  # 認証失敗メッセージを表示

elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')  # 認証待ちメッセージを表示




