import numpy as np
import streamlit as st
from modules.utils import load_ref_helper, compare_doses

@st.cache_data
def load_ref(id1, id2, use_europe=True):
    return load_ref_helper(id1, id2, use_europe)

'''
- Select reference standard

Decision paths:
- 'Europe'
- 'United States' -> ('Without Contrast', 'With Contrast')
'''
def sidebar():
    with st.sidebar:
        st.header('Reference Menu')
        contrast_usage = None

        ref_country = st.sidebar.selectbox(
            'Select reference standard:',
            ('Europe', 'United States')
        )
        
        if (ref_country == 'United States'):
            contrast_usage = st.radio(
                'Select contrast usage:',
                ('Without contrast', 'With contrast')
            )
            st.markdown('''
                        - **Pediatric doses:** Kanal KM, Butler PF, Chatfield MB, et al. U.S. Diagnostic Reference Levels and Achievable Doses for 10 Pediatric CT Examinations. Radiology. 
                        2022;302(1):164-174. [doi:10.1148/radiol.2021211241](https://pubs.rsna.org/doi/10.1148/radiol.2021211241)
                        - **Pediatric and adult doses:** ACR–AAPM–SPR PRACTICE PARAMETER FOR DIAGNOSTIC REFERENCE LEVELS AND ACHIEVABLE DOSES IN MEDICAL X-RAY IMAGING. Published online 2022. Accessed September 10, 2023. 
                        https://www.acr.org/-/media/ACR/Files/Practice-Parameters/diag-ref-levels.pdf 
                        - **Clinical indication-based doses:** Bos D, Yu S, Luong J, et al. Diagnostic reference levels and median doses for common clinical indications of CT: findings from an international registry. Eur Radiol. 
                        2022;32(3):1971-1982. [doi:10.1007/s00330-021-08266-1](https://link.springer.com/article/10.1007/s00330-021-08266-1)
                        ''')
        else: # ref_country == 'Europe'
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

        # st.subheader('Dose Input Instructions')
        # st.info('''
        # 1. Do NOT input scout/localizer doses or doses related to bolus tracking or test bolus. 
        # 2. For multiple-run, multiple body parts CT, please input CTDIvol and DLP separately. 
        # 3. For multiphase CT (>1 acquisition), please input the maximum single CTDIvol (Ex: if CTDIvol are 4 and 6 mGy for two scan series, input 6 mGy. Do NOT add CTDIvol)
        # 4. For multiphase CT (>1 acquisition), please input the total DLP (Ex: if DLP are 300 and 600 mGy.cm for two scan series, input 900 mGy.cm)
        # ''')

    return ref_country, contrast_usage

'''
- Input demographic information according to European reference

Decision paths:
- 'Adult' -> Body Region
- 'Child' -> 'Head' -> Age
- 'Child' -> ('Chest', 'Abdomen') -> Weight
'''
def europe_demographics_expander():
    life_stage = None # 'Child' or 'Adult'
    adult_body_region = None # 'Head', 'Neck', 'Cervical spine', 'Chest', 'CTPA', 'Abdomen-pelvis', or 'Chest-abdomen-pelvis'
    child_body_region = None # 'Head', 'Chest', or 'Abdomen'
    age_class = None # '0-3 months', '3-12 months', '1-6 years', '>6 years'
    weight_class = None # '0-5 kg', '5-15 kg', '15-30 kg', '30-50 kg', '50-80 kg'
    include_indications = None # boolean
    df = None # pandas dataframe

    with st.expander('**Demographics**', expanded=True):
        life_stage = st.radio(
            'Select age group:',
            ('Child', 'Adult')
        )

        if (life_stage == 'Adult'): 
            df = load_ref(life_stage, 'regions')
            adult_body_region= st.selectbox(
                'Select body region:',
                (df['Region']) # adult DRL accessed by body region
            )
        else: # life_stage == "Child"
            child_body_region = st.radio( 
                'Select body region:',
                ('Head', 'Chest', 'Abdomen')
            )
            df = load_ref(life_stage, child_body_region)

            if (child_body_region=='Head'): 
                age_class = st.selectbox(
                    'Select age class: ',
                    (df['Age']) # child head DRL accessed by age
                )
            else: # child_body_region == 'Chest' or 'Abdomen'
                weight_class = st.selectbox(
                    'Select weight class: ',
                    (df['Weight']) # child chest or abdomen DRL accessed by weight
                )
        
        if (life_stage == 'Adult'): 
            include_indications = st.checkbox('Do you have clinical indications to include?')

    return (life_stage, 
            adult_body_region, child_body_region, 
            age_class, weight_class, 
            include_indications,
            df)

'''
- Input demographic information according to US reference

Decision paths:
- 
'''
def us_demographics_expander():
    life_stage = None # 'Child' or 'Adult'
    adult_body_region = None # 'Head', 'Neck', 'Cervical spine', 'Chest', 'CTPA', 'Abdomen-pelvis', or 'Chest-abdomen-pelvis'
    child_body_region = None # 'Head', 'Chest', 'Abdomen', or 'Chest-abdomen-pelvis'
    age_class = None # 0-1 year, 1-5 years, 5-10 years, 10-15 years, 15-18 years ('Head': 0-1 year, 1-2 years, 2-6 years, 6-18 years)
    include_indications = None # boolean
    df = None # pandas dataframe
    
    with st.expander('**Demographics**', expanded=True):
        life_stage = st.radio(
                'Select age group:',
                ('Child', 'Adult')
            ) 
    
        if (life_stage == 'Child'): 
            child_body_region = st.radio( 
                'Select body region:',
                ('Head', 'Chest', 'Abdomen', 'Chest-Abdomen-Pelvis')
            )
            df = load_ref(life_stage, child_body_region, use_europe=False)

            age_class = st.selectbox(
                'Select age class: ',
                (df['Age']) # child DRL accessed by age
            )
        else: # life_stage == 'Adult'
            df = load_ref(life_stage, 'regions', use_europe=False)
            adult_body_region = st.selectbox(
                'Select body region:',
                (df['Region'])  # adult DRL accessed by body region
            )
            include_indications = st.checkbox('Do you have clinical indications to include?')

        return life_stage, adult_body_region, child_body_region, age_class, include_indications, df

'''
- Input clinical indications

Decision paths:
- 'Adult' -> ('Head', 'Neck', 'Chest', 'Abdomen') -> Clinical indications
- 'Adult' -> (All other) -> No clinical indications
'''
def clinical_indications_expander(adult_body_region, use_europe=True):
    with st.expander('**Clinical Indications**', expanded=True):
        df = load_ref('adult', 'indicators', use_europe)
        indication_options = df[df['Region']==adult_body_region]['Indication']

        if (indication_options.size > 0):
            indication = st.radio(
                'Select clinical indication: ',
                (indication_options)
            )

            return indication, df
        else:
            st.info('DRLs are only available for a limited number of clinical indications.')
            return None, None

'''
- Input CTDIvol and DLP
'''
def system_parameters_expander(ref_ctdivol, ref_dlp):
    with st.expander('**CT Doses**', expanded=True):
        max_ctdivol = float(10*ref_ctdivol) if ref_ctdivol != '-' else None
        max_dlp = float(10*ref_dlp) if ref_dlp != '-' else None
        
        col1, _, _ = st.columns(3)
        with col1: 
            num_phases = st.number_input('Number of Phases', min_value=1, max_value=10)
            ctdivol_arr = np.empty(num_phases)
            dlp_arr = np.empty(num_phases)

        innercol1, innercol2 = st.columns(2)
        for i in range(num_phases):
            with innercol1:
                ctdivol_arr[i] = st.number_input('CTDIvol (mGy)', step=0.1, min_value=0.0, max_value=max_ctdivol, format='%.1f', key=i)
            
            with innercol2:
                dlp_arr[i] = st.number_input('DLP (mGy·cm)', step=1.0,  min_value=0.0, max_value=max_dlp, format='%.0f', key=99-i)

    return np.median(ctdivol_arr), np.sum(dlp_arr)
'''
- View recommendations

Decision paths:
- (>=1 dose exceeds 'DRL') and ('body_region' in 'rec_df) -> Detailed recommendation
- (>=1 dose exceeds 'DRL') -> ('body_region' not in 'rec_df') -> Generic recommendation
- Both doses below 'DRL' -> Congratulations message
'''
def recommendations_expander(ctdivol, dlp, 
                             ref_ctdivol, ref_dlp, 
                             life_stage, body_region, rec_df):
    
    ctdivol_safe = compare_doses(ref_ctdivol, ctdivol, 'CTDIvol')
    dlp_safe = compare_doses(ref_dlp, dlp, 'DLP')
    
    if not(ctdivol_safe and dlp_safe):
        valid_body_regions = ['Head', 'Chest', 'Abdomen']

        if body_region in valid_body_regions: 
            key = f'{life_stage} {body_region}'
            rec = rec_df.loc[rec_df['Category']==key, 'Recommendation'].values[0]
            st.info(rec)

        else: 
            st.info('Unfortunately, there are no specific recommendations available for these inputs.')
    else:
        st.success('Congratulations! Your doses are below the suggested DRLs.')