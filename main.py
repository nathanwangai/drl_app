import streamlit as st
from modules.utils import dose_gauge_plot
from modules.app_components import sidebar, europe_data_input, us_data_input, system_parameters_input, recommendations

st.set_page_config(page_title='CT-Dose-Check', page_icon='static/mgh_logo.png', layout='wide')
st.title('CT-Dose-Check')

if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if 'disclaimer_accepted' not in st.session_state:
    st.session_state['disclaimer_accepted'] = False

if not st.session_state['disclaimer_accepted']: 
    st.info('''
            Most diagnostic reference levels (DRLs) are estimated for a specific cohort of patients undergoing typical
            CT protocols. Therefore, DRLs should not be used for individual patients or as dose limits. However, DRLs
            are essential for radiation dose optimization. Rather than the DRLs, users must use their facility’s
            median dose values (typical values), representative of their CT equipment and patient population, for
            checking individual patients. The current tool provides an example of optimizing CT radiation dose and
            protocols on a national or international level. For local or facility-based dose optimization, it is essential
            to use the median local/facility doses (Typical values).
            ''')
    
    if st.button('Accept Disclaimer'): 
        st.session_state['disclaimer_accepted'] = True
        st.rerun()

else:
    ref_country = sidebar()

    col1, col2 = st.columns(2)
    with col1:
        if (ref_country == 'Europe'):
            ret = europe_data_input()
            st.write(ret)
            a, b = ret[0], ret[1]
            ref_ctdivol, ref_dlp = ret[-2], ret[-1]
            ctdivol, dlp = system_parameters_input(ref_ctdivol, ref_dlp)
        else:
            ret = us_data_input()
            st.write(ret)
            a, b = ret[0], ret[1]
            ref_ctdivol, ref_dlp = ret[-2], ret[-1]
            ret2 = system_parameters_input(ref_ctdivol, ref_dlp)
            ctdivol, dlp = ret2[0], ret2[1]

        submit = st.button('Get Recommendation')

        if submit: 
            st.session_state['var1'] = ref_ctdivol
            st.session_state['var2'] = ref_dlp
            st.session_state['var3'] = ctdivol
            st.session_state['var4'] = dlp
            st.session_state['var5'] = a
            st.session_state['var6'] = b
            st.session_state['submitted'] = True

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

                recommendations(st.session_state['var1'], st.session_state['var2'], st.session_state['var3'],
                                st.session_state['var4'], st.session_state['var5'], st.session_state['var6'])
                store = st.button('Store in database')

                if store:
                    st.session_state['submitted'] = False
                    st.rerun()