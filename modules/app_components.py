import numpy as np
import streamlit as st
from modules.utils import retrieve_ref_doses, load_df, compare_doses

def sidebar():
    with st.sidebar:
        st.header('Reference Menu')
        ref_country = st.sidebar.selectbox(
            'Select reference standard:',
            ('Europe', 'United States')
        )

    return ref_country

def europe_data_input():
    """
    Returns:
    tuple: patient_type, body_region, selector, contrast usage, ctdivol, dlp
    """
    with st.container(border=True):
        st.subheader('**Data Input**')

        patient_type = st.radio(
            'Is the patient a child or adult?',
            ('Child', 'Adult')
        )

    # __________European Pediatric DRLs__________
        if (patient_type == 'Child'):
            df = load_df('europe_pediatric_drls.csv')
            body_region = st.radio(
                'Select body region:',
                df['Region'].unique()
            )

            df = df[df['Region'] == body_region]
            size_group = st.selectbox(
                'Select the patient\'s age or weight group: ',
                df['Age/Weight']
            )
            ctdivol, dlp = retrieve_ref_doses(df, 'Age/Weight', size_group)

            return patient_type, body_region, size_group, False, ctdivol, dlp
    # __________European Pediatric DRLs__________

    # -----| European Adult Clinical-Based DRLs |-----
        elif st.checkbox('Include clinical indications?'): 
            df = load_df('europe_clinical_drls.csv')
            body_region = st.radio(
                'Select body region: ',
                df['Region'].unique()
            )
            
            df = df[df['Region'] == body_region]
            indication = st.selectbox(
                'Select clinical indication: ',
                df['Clinical Indication']
            )
            ctdivol, dlp = retrieve_ref_doses(df, 'Clinical Indication', indication)

            return patient_type, body_region, indication, False, ctdivol, dlp
    # ----- ----- ----- ----- -----

    # -----| United Kingdom Adult DRLs |-----
        else:
            df = load_df('uk_adult_drls.csv')
            body_region = st.radio(
                'Select body region: ',
                df['Region'].unique()
            )
            ctdivol, dlp = retrieve_ref_doses(df, 'Region', body_region)

            return patient_type, body_region, 'None', False, ctdivol, dlp
    # ----- ----- ----- ----- -----
        
def us_data_input():
    with st.container(border=True):
        st.subheader('**Data Input**')

        patient_type = st.radio(
            'Is the patient a child or adult?',
            ('Child', 'Adult')
        )

        if (patient_type == 'Child'):
            df = load_df('us_pediatric_drls.csv')
            region = st.radio(
                'Select body region:',
                df['Region'].unique()
            )

            df = df[df['Region'] == region]
            age_or_weight = st.selectbox(
                'Select the patient\'s age or weight group: ',
                df['Age/Weight']
            )

            if (region == 'Head'): 
                contrast = st.checkbox('Check if using contrast', value=False, disabled=True)
            elif (region == 'Chest-Abdomen-Pelvis' or (region == 'Abdomen' and age_or_weight=='0-1 year')):
                contrast = st.checkbox('Check if using contrast', value=True, disabled=True)
            else:
                contrast = st.checkbox('Check if using contrast')

            ctdivol, dlp = retrieve_ref_doses(df, 'Age/Weight', age_or_weight, contrast)

            return patient_type, region, age_or_weight, ctdivol, dlp

        elif st.checkbox('Include clinical indications?'): 
            df = load_df('us_clinical_drls.csv')
            region = st.radio(
                'Select body region: ',
                df['Region'].unique()
            )
            
            df = df[df['Region'] == region]
            indication = st.selectbox(
                'Select clinical indication: ',
                df['Clinical Indication']
            )
            ctdivol, dlp = retrieve_ref_doses(df, 'Clinical Indication', indication)

            return patient_type, indication, ctdivol, dlp
        
        else:
            df = load_df('us_adult_drls.csv')
            region = st.radio(
                'Select body region: ',
                df['Region'].unique()
            )

            if (region in ['Head', 'Cervical spine']):
                contrast = st.checkbox('Check if using contrast', value=False, disabled=True)
            elif (region in ['Neck', 'CTPA', 'Chest-abdomen-pelvis']):
                contrast = st.checkbox('Check if using contrast', value=True, disabled=True)
            else:
                contrast = st.checkbox('Check if using contrast')

            ctdivol, dlp = retrieve_ref_doses(df, 'Region', region, contrast)

            return patient_type, region, ctdivol, dlp
            
def system_parameters_input(ctdivol, dlp):
    with st.container(border=True):
        st.subheader('**System Parameters**')
        
        with st.columns(3)[0]:
            num_phases = st.number_input('Number of Phases', min_value=1, max_value=10)
            disable_ctdivol = (ctdivol == '-')
            disable_dlp = (dlp == '-')
            max_ctdivol = 10*ctdivol if not disable_ctdivol else None
            max_dlp = (10/num_phases)*dlp if not disable_dlp else None

        ctdivol_arr = np.empty(num_phases)
        dlp_arr = np.empty(num_phases)
        col1, col2 = st.columns(2)
        for i in range(num_phases):
            with col1:
                ctdivol_arr[i] = st.number_input('CTDIvol (mGy)', step=0.1, 
                                                 min_value=0.0, max_value=max_ctdivol, 
                                                 format='%.1f', key=i, disabled=disable_ctdivol)
            
            with col2:
                dlp_arr[i] = st.number_input('DLP (mGy·cm)', step=1.0, 
                                             min_value=0.0, max_value=max_dlp, 
                                             format='%.0f', key=99-i, disabled=disable_dlp)                                         

    return np.median(ctdivol_arr), np.sum(dlp_arr)

def recommendations(ref_ctdivol, ref_dlp, ctdivol, dlp, patient_type, region):
    df = load_df('recommendations.csv')
    ctdivol_safe = compare_doses(ref_ctdivol, ctdivol, 'CTDIvol')
    dlp_safe = compare_doses(ref_dlp, dlp, 'DLP')

    if not (ctdivol_safe and dlp_safe):        
        df = df[df['Category'] == f'{patient_type} {region}']

        if (not df.empty):
            st.info(df['Recommendation'].values[0])
        else: 
            st.info('Unfortunately, there are no specific recommendations available for these inputs.')
    else:
        st.success('Congratulations! Your doses are below the suggested DRLs.')