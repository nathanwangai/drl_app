import streamlit as st
import modules.database_utils as db
from modules.utils import dose_gauge_plot
from modules.app_components import sidebar, europe_data_input, us_data_input, system_parameters_input, recommendations

# -----| Initialize Session Variables |-----
if 'disclaimer_accepted' not in st.session_state:
    st.session_state['disclaimer_accepted'] = False

if 'ret' not in st.session_state:
    st.session_state['ret'] = None

if 'doses' not in st.session_state:
    st.session_state['doses'] = None

if 'user' in st.session_state:
    path = st.session_state['path']
    database = st.session_state['database']
# ----- ----- ----- ----- -----

st.set_page_config(page_title='Dose Checker', page_icon='static/mgh_logo.png', layout='wide')

with st.columns([1,6,1])[1]:
    st.title('CT Dose Check')

    if not st.session_state['disclaimer_accepted']: 
        st.info('''
                Most diagnostic reference levels (DRLs) are estimated for a specific cohort of patients undergoing typical
                CT protocols. Therefore, DRLs should not be used for individual patients or as dose limits. However, DRLs 
                are essential for radiation dose optimization. Rather than the DRLs, users must use their facility’s median 
                dose values (typical values), representative of their CT equipment and patient population, for checking 
                individual patients. The current tool provides an example of optimizing CT radiation dose and protocols on 
                a national or international level. For local or facility-based dose optimization, it is essential to use the 
                median local/facility doses (Typical values).
                ''')
        
        if st.button('I Understand'): 
            st.session_state['disclaimer_accepted'] = True
            st.rerun()

if st.session_state['disclaimer_accepted']:
    ref_country = sidebar()

    col1, col2 = st.columns([1, 3, 3, 1])[1:3]
    with col1:
        ret = europe_data_input() if (ref_country == 'Europe') else us_data_input()
        a, b = ret[0], ret[1]
        ref_ctdivol, ref_dlp = ret[-2], ret[-1]
        ctdivol, dlp = system_parameters_input(ref_ctdivol, ref_dlp)

        # detect if changes have been made since last submit
        if ret != st.session_state['ret']:
            st.session_state['submitted'] = False

        if (ctdivol, dlp) != st.session_state['doses']:
            st.session_state['submitted'] = False

        if  st.button('Get Recommendation'):
            st.session_state['ret'] = ret
            st.session_state['doses'] = (ctdivol, dlp)
            st.session_state['submitted'] = True
            st.session_state['stored'] = False

    if st.session_state['submitted']:
        with col2: 
            with st.container(border=True):
                st.subheader('**Recommendation**')
                
                inner_col1, inner_col2 = st.columns(2)
                with inner_col1:
                    if (ref_ctdivol != '-'):
                        dose_gauge_plot(ref_ctdivol, ctdivol, 'CTDIvol')
                        st.image('static/CTDIvol_gauge.png')
                    else:
                        st.info('CTDIvol DRL values are unavailable.')
                with inner_col2:
                    if (ref_dlp != '-'):
                        dose_gauge_plot(ref_dlp, dlp, 'DLP')
                        st.image('static/DLP_gauge.png')
                    else: 
                        st.info('DLP DRL values are unavailable.')

                recommendations(ref_ctdivol, ref_dlp, ctdivol, dlp, a, b)

                if 'user' in st.session_state:
                    if st.button('Store in database'):
                        st.toast(ret[:-2] + st.session_state['doses'])
                        database.loc[len(database)] = ret[:-2] + st.session_state['doses']
                        db.write_to_gcs(database, path)

st.write('')

db.user_sidebar()