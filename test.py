import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection
import io

def manage_tasks():
    st.title('Task Turtle')

    # Create connection object and retrieve file contents.
    conn = st.connection('gcs', type=FilesConnection)

    # Read file from GCS
    file_content = conn.read("dk_task_list/task.csv", input_format="csv", ttl=600)

    # Try different encodings
    encodings = ['utf-8', 'cp932', 'iso-2022-jp']
    for encoding in encodings:
        try:
            df = pd.read_csv(io.StringIO(file_content), encoding=encoding)
            st.write("DataFrame loaded successfully with encoding:", encoding)
            st.write(df)
            return
        except UnicodeDecodeError:
            st.write(f"Failed to read with encoding: {encoding}")

manage_tasks()


