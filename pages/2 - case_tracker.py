import numpy as np
import pandas as pd
import streamlit as st

df = pd.read_csv('database.csv')
# col1, col2 = st.columns([0.8, 0.2])

# for i in range(len(df)):
#     row = df.iloc[i]
#     with col1:
#         st.write(row)

st.data_editor(
    df,
    column_config = {
        'patient_type': st.column_config.Column(
            'Patient Type',
            disabled=True
        ),
        'body_region': st.column_config.Column(
            'Body Region',
            disabled=True
        )
    }, 
    num_rows='dynamic')