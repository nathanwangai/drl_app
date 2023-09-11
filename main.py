import streamlit as st
import pandas as pd
from modules.app_components import sidebar, europe_demographics_expander, us_demographics_expander, system_parameters_expander, recommendations_expander, clinical_indications_expander
from modules.utils import create_dose_bars, retrieve_ref_doses

st.set_page_config(page_title='CT-Dose-Check', page_icon='static/mgh_logo.png', layout='wide')
st.header('CT-Dose-Check')
rec_df = pd.read_csv('drl_references/recommendations.csv') # ('Child', 'Adult') -> ('Head', 'Chest', 'Abdomen')
ref_country, contrast_usage = sidebar()

if 'disclaimer' not in st.session_state:
    st.session_state['disclaimer'] = False

if not st.session_state['disclaimer']: 
    st.info('''
            Most diagnostic reference levels (DRLs) are estimated for a specific cohort of patients undergoing typical
            CT protocols. Therefore, DRLs should not be used for individual patients or as dose limits. However, DRLs
            are essential for radiation dose optimization. Rather than the DRLs, users must use their facility’s
            median dose values (typical values), representative of their CT equipment and patient population, for
            checking individual patients. The current tool provides an example of optimizing CT radiation dose and
            protocols on a national or international level. For local or facility-based dose optimization, it is essential
            to use the median local/facility doses (Typical values).
            ''')
    st.session_state['disclaimer'] = st.button('Accept Disclaimer')
else:
    col1, col2 = st.columns(2, gap='small')
    with col1: # --------------- DATA INPUT COLUMN ---------------
        # global variables (plus 'ref_country' and 'contrast_usage')
        ref_ctdivol = None
        ref_dlp = None
        indication = None
        df = None
        adult_body_region = None
        child_body_region = None
        submit = False

        if ref_country == 'Europe': # --------------- european reference ---------------  
            life_stage, adult_body_region, child_body_region, age_class, weight_class, include_indications, df = europe_demographics_expander()

            if include_indications:
                indication, ret = clinical_indications_expander(adult_body_region)
                if isinstance(ret, pd.DataFrame): df = ret # clinical indications DRL have highest priority

            # attempt to access DRLs by variables in order of decreasing priority
            selection_var_array = [indication, adult_body_region, age_class, weight_class]
            for var in selection_var_array:
                if (var != None): 
                    ref_ctdivol, ref_dlp = retrieve_ref_doses(df, var, include_indications)
                    break

            ctdivol, dlp = system_parameters_expander(ref_ctdivol, ref_dlp)
            submit = st.button('Submit')

        else: # --------------- united states reference ---------------  
            life_stage, adult_body_region, child_body_region, age_class, include_indications, df = us_demographics_expander()
            
            if include_indications:
                indication, ret = clinical_indications_expander(adult_body_region, use_europe=False)
                if isinstance(ret, pd.DataFrame): df = ret 

            selection_var_array = [indication, adult_body_region, age_class]
            for var in selection_var_array:
                if (var != None): 
                    ref_ctdivol, ref_dlp = retrieve_ref_doses(df, var, indication!=None, contrast_usage)
                    break
            
            if (ref_ctdivol == '-' and ref_dlp == '-'):
                body_region = adult_body_region if adult_body_region != None else child_body_region
                include_indications = False
                st.info(f'Unfortunately, DRL values unavailable for {life_stage}, {body_region} {contrast_usage.lower()}.')
            else:
                ctdivol, dlp = system_parameters_expander(ref_ctdivol, ref_dlp)
                submit = st.button('Submit')

    with col2: # --------------- RECOMMENDATIONS COLUMN ---------------
        with st.expander('**Recommendations**', expanded=True):    
        
            # ----- dose bar plots -----
            innercol1, innercol2 = st.columns(2, gap='small')
            with innercol1:
                if (ref_ctdivol != '-'): 
                    create_dose_bars('CTDIvol (mGy)', ref_ctdivol, ctdivol)
                else:
                    st.info('Unfortunately, CTDIvol DRL values are unavailable for these inputs.')
            with innercol2: 
                if (ref_dlp != '-'): 
                    create_dose_bars('DLP (mGy·cm)', ref_dlp, dlp)
                else:
                    st.info('Unfortunately, DLP DRL values unavailable for these inputs.')
            # ----- end of dose bar plots -----

            if submit: 
                body_region = adult_body_region if adult_body_region != None else child_body_region
                
                recommendations_expander(ctdivol, dlp, 
                                ref_ctdivol, ref_dlp, 
                                life_stage, body_region, rec_df)