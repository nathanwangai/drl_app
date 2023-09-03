import streamlit as st

st.set_page_config(page_title='CT-Dose-Check', page_icon='static/mgh_logo.png', layout='wide')
st.header('About')
st.markdown('This application was developed at the Massachusetts General Hospital Webster Center for Quality and Safety')

col1, col2, col3 = st.columns(3, gap='small')
with col1: 
    st.info('''
            **Nathan Wang**\\
            Undergraduate @ Johns Hopkins University
            ''')
with col2: 
    st.info('''
            **Lina Karout, MD**\\
            Research fellow @ Massachusetts General Hospital
            ''')
with col3: 
    st.info('''
            **Mannudeep Kalra, MD**\\
            Director @ The Webster Center for Quality and Safety
            ''')