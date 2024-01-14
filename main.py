import streamlit as st
from modules.utils import create_dose_bars

st.set_page_config(page_title='CT-Dose-Check', page_icon='static/mgh_logo.png', layout='wide')
st.title('CT-Dose-Check')

from modules.app_components import sidebar, europe_data_input, us_data_input, system_parameters_input, recommendations

ref_country = sidebar()

col1, col2 = st.columns(2, gap='small')
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

    submit = st.button('Submit')

with col2: 
    with st.container(border=True):
        st.subheader('**Recommendations**')
        
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            if (ref_ctdivol != '-'):
                create_dose_bars('CTDIvol (mGy)', ref_ctdivol, ctdivol)
            else:
                st.info('CTDIvol DRL values are unavailable.')
        with inner_col2:
            if (ref_dlp != '-'):
                create_dose_bars('DLP', ref_dlp, dlp)
            else: 
                st.info('DLP DRL values are unavailable.')

        if (submit): 
            recommendations(ref_ctdivol, ref_dlp, ctdivol, dlp, a, b)


# if 'disclaimer' not in st.session_state:
#     st.session_state['disclaimer'] = False

# if not st.session_state['disclaimer']: 
#     st.info('''
#             Most diagnostic reference levels (DRLs) are estimated for a specific cohort of patients undergoing typical
#             CT protocols. Therefore, DRLs should not be used for individual patients or as dose limits. However, DRLs
#             are essential for radiation dose optimization. Rather than the DRLs, users must use their facility’s
#             median dose values (typical values), representative of their CT equipment and patient population, for
#             checking individual patients. The current tool provides an example of optimizing CT radiation dose and
#             protocols on a national or international level. For local or facility-based dose optimization, it is essential
#             to use the median local/facility doses (Typical values).
#             ''')
#     st.session_state['disclaimer'] = st.button('Accept Disclaimer')
# else: