import numpy as np
import pandas as pd
import streamlit as st

st.title('Case Tracker')

path = 'gcs://data_bucket_ct_dose_check/nathan_test/database.csv'
df = pd.read_csv(path)


st.data_editor(
    df,
    column_config = {
        'patient_type': st.column_config.SelectboxColumn(
            'Patient Type',
            options = ['Adult', 'Child'],
            required = True
        ),
        'body_region': st.column_config.Column(
            'Body Region',
            disabled = True
        ),
        'selector': st.column_config.Column(
            'Selector',
            disabled = True
        ),
        'contrast': st.column_config.CheckboxColumn(
            'Contrast',
            required = True
        ),
        'ctdivol': st.column_config.NumberColumn(
            'CTDIvol (mGy)',
            required = True
        ),
        'dlp': st.column_config.NumberColumn(
            'DLP (mGy*cm)',
            required = True
        )
    }, 
    num_rows='dynamic')