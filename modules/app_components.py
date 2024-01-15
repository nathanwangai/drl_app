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
        
        if st.toggle('View References'):
            if (ref_country == 'United States'):
                st.markdown('''
                            - **Pediatric doses:** Kanal KM, Butler PF, Chatfield MB, et al. U.S. Diagnostic Reference Levels and Achievable Doses for 10 Pediatric CT Examinations. Radiology. 
                            2022;302(1):164-174. [doi:10.1148/radiol.2021211241](https://pubs.rsna.org/doi/10.1148/radiol.2021211241)
                            - **Pediatric and adult doses:** ACR–AAPM–SPR PRACTICE PARAMETER FOR DIAGNOSTIC REFERENCE LEVELS AND ACHIEVABLE DOSES IN MEDICAL X-RAY IMAGING. Published online 2022. Accessed September 10, 2023. 
                            https://www.acr.org/-/media/ACR/Files/Practice-Parameters/diag-ref-levels.pdf 
                            - **Clinical indication-based doses:** Bos D, Yu S, Luong J, et al. Diagnostic reference levels and median doses for common clinical indications of CT: findings from an international registry. Eur Radiol. 
                            2022;32(3):1971-1982. [doi:10.1007/s00330-021-08266-1](https://link.springer.com/article/10.1007/s00330-021-08266-1)
                            ''')
            else:
                st.markdown('''
                            - **Pediatric doses:** Directorate-General for Energy (European Commission). Technical Recommendations for Monitoring Individuals for Occupational Intakes of Radionuclides. Publications Office of the European Union; 2018. Accessed September 11, 2023. 
                            https://data.europa.eu/doi/10.2833/393101
                            - **Adult doses (UK):** National Diagnostic Reference Levels (NDRLs) from 13 October 2022. GOV.UK. Accessed September 10, 2023. 
                            https://www.gov.uk/government/publications/diagnostic-radiology-national-diagnostic-reference-levels-ndrls/ndrl
                            - **Clinical indication-based doses:** 
                                - Directorate-General for Energy (European Commission), Damilakis J, Frija G, et al. European Study on Clinical Diagnostic Reference Levels for X-Ray Medical Imaging: EUCLID. Publications Office of the European Union; 2021. Accessed September 10, 2023. 
                                https://data.europa.eu/doi/10.2833/452154 
                                - Diagnostic reference levels and median doses for common clinical indications of CT: findings from an international registry. Eur Radiol. 
                                2022;32(3):1971-1982. [doi:10.1007/s00330-021-08266-1](https://link.springer.com/article/10.1007/s00330-021-08266-1)
                        ''')

    return ref_country

def europe_data_input():
    with st.container(border=True):
        st.subheader('**Data Input**')

        patient_type = st.radio(
            'Is the patient a child or adult?',
            ('Child', 'Adult')
        )

        if (patient_type == 'Child'):
            df = load_df('europe_pediatric_drls.csv')
            region = st.radio(
                'Select body region:',
                df['Region'].unique()
            )

            df = df[df['Region'] == region]
            choice = st.selectbox(
                'Select the patient\'s age or weight group: ',
                df['Age/Weight']
            )
            ctdivol, dlp = retrieve_ref_doses(df, 'Age/Weight', choice)

            return patient_type, region, choice, ctdivol, dlp

        elif st.checkbox('Include clinical indications?'): 
            df = load_df('europe_clinical_drls.csv')
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
            df = load_df('uk_adult_drls.csv')
            region = st.radio(
                'Select body region: ',
                df['Region'].unique()
            )
            ctdivol, dlp = retrieve_ref_doses(df, 'Region', region)

            return patient_type, region, ctdivol, dlp
    
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
            ctdivol_disable = True
            dlp_disable = True
            max_ctdivol = None
            max_dlp = None
            
            if (ctdivol != '-'): 
                ctdivol_disable = False
                max_ctdivol = 10*ctdivol
            if (dlp != '-'): 
                dlp_disable = False
                max_dlp = (10/num_phases)*dlp

        ctdivol_arr = np.empty(num_phases)
        dlp_arr = np.empty(num_phases)
        col1, col2 = st.columns(2)
        for i in range(num_phases):
            with col1:
                ctdivol_arr[i] = st.number_input('CTDIvol (mGy)', step=0.1, 
                                                 min_value=0.0, max_value=max_ctdivol, 
                                                 format='%.1f', key=i, disabled=ctdivol_disable)
            
            with col2:
                dlp_arr[i] = st.number_input('DLP (mGy·cm)', step=1.0, 
                                             min_value=0.0, max_value=max_dlp, 
                                             format='%.0f', key=99-i, disabled=dlp_disable)                                            

    return np.median(ctdivol_arr), np.sum(dlp_arr)

def recommendations(ref_ctdivol, ref_dlp, ctdivol, dlp, patient_type, region):
    df = load_df('recommendations.csv')
    ctdivol_safe = compare_doses(ref_ctdivol, ctdivol, 'CTDIvol')
    dlp_safe = compare_doses(ref_dlp, dlp, 'DLP')

    if not (ctdivol_safe and dlp_safe):        
        # st.write(f'{patient_type} {region}')
        df = df[df['Category'] == f'{patient_type} {region}']

        if (not df.empty):
            st.info(df['Recommendation'].values[0])
        else: 
            st.info('Unfortunately, there are no specific recommendations available for these inputs. However, please attempt to reduce dose.')
    else:
        st.success('Congratulations! Your doses are below the suggested DRLs.')