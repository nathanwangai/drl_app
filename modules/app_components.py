import numpy as np
import streamlit as st
# from modules.utils import load_df, retrieve_ref_doses

def demographic_input():
    with st.container(border=True):
        st.subheader('**Demographic Info**')

        gender = st.radio(
            'Select the patient\'s gender',
            ('Male', 'Female', 'Other'),
        )
        
        patient_type = st.radio(
            'Is the patient a child or adult?',
            ('Child', 'Adult'),
        ) 
        
        col1, col2 = st.columns([1, 2])
        with col1:
            age_unit = st.selectbox(
                'Units:',
                ('Years', 'Months')
            )
        with col2:
            age = st.number_input(f'Patient Age ({age_unit.lower()})', min_value=0, max_value=120)            
            if (age_unit == 'Months' and age is not None): age /= 12

        col3, col4 = st.columns([1,2])
        with col1:
            weight_unit = st.selectbox(
                'Units:',
                ('kgs', 'lbs')
            )
        with col2:
            weight = st.number_input(f'Patient Weight {weight_unit}', min_value=0.0, max_value=1000.0, value=None, placeholder='Optional')
            if (weight_unit == 'lbs' and weight is not None): weight /= 2.20462 

        return gender, patient_type, age, weight

def protocol_input(patient_type):
    with st.container(border=True):
        st.subheader('**Protocol Info**')
        body_region, indication = None, None

        if patient_type == 'Child':
            body_region = st.selectbox(
                'Select body region',
                ('Head', 'Chest', 'Abdomen', 'Chest-Abdomen-Pelvis')
            )
        elif st.checkbox('Report clinical indication'):
                indication = st.selectbox(
                    'Select clinical indication',
                    ('Chronic Sinusitis', 'Stroke', 
                     'Cervical spine trauma', 
                     'CACS', 'Lung cancer', 'Pulmonary embolism', 'Coronary CTA',
                     'Hepatocellular carcinoma', 'Colic/abdominal pain', 'Appendicitis')
                )
        else:
            body_region = st.selectbox(
                'Select body region',
                ('Head', 'Neck', 'Cervical spine', 'Chest', 'CTPA', 'Abdomen-pelvis', 'Chest-abdomen-pelvis')
            )

        contrast = st.checkbox('Using contrast?')
        contrast = 'Yes' if contrast else 'No'

        return body_region, indication, contrast

def system_parameters_input():
    with st.container(border=True):
        st.subheader('**System Parameters**')

        with st.columns(3)[0]: 
            num_phases = st.number_input('Number of Phases', min_value=1, max_value=10)

        ctdivol_arr = np.empty(num_phases)
        dlp_arr = np.empty(num_phases)

        col1, col2 = st.columns(2)
        for i in range(num_phases):
            with col1:
                ctdivol_arr[i] = st.number_input('CTDIvol (mGy)', step=0.1, min_value=0.0, format='%.1f', key=i)

            with col2:
                dlp_arr[i] = st.number_input('DLP (mGy·cm)', step=1, min_value=0, key=99-i)                                     

        return np.median(ctdivol_arr), np.sum(dlp_arr)

# def recommendation_report(country, patient_type, age, weight, body_region, indication, contrast, ctdivol, dlp):
#     if patient_type == 'Child':
#         pass
#     elif indication != None:
#         df = load_df(f'{country}_clinical_drls')
#         retrieve_ref_doses(df, 'Clinical Indication', indication)
#     else:
#         df = load_df(f'{country}_adult_drls')