import gcsfs
import pyrebase
import pandas as pd
import streamlit as st

auth = pyrebase.initialize_app(st.secrets.firebase_auth_config).auth()
fs = gcsfs.GCSFileSystem(token=dict(st.secrets['gcs_config']))

def write_to_gcs(df, path):
    with fs.open(path, 'w') as f:
        df.to_csv(f, index=False)

def read_from_gcs(path):
    with fs.open(path) as f:
        return pd.read_csv(f)
    
def delete_database_gcs(email):
    path = f'ct_dose_check_bucket/{email}/database.csv'

    if fs.exists(path):
        fs.rm(path)

def user_sidebar():
    with st.sidebar:
        if 'user' in st.session_state:
            st.info(f'Currently logged in as: {st.session_state["user"]["email"]}')

            if st.button('Log Out'):
                st.session_state.pop('user')
                st.session_state.pop('path')
                st.session_state.pop('database')
                st.toast('Successfully logged out!')
                st.rerun()
        else:
            st.info('Currently logged in as Guest')