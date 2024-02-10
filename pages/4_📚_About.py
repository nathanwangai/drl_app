import streamlit as st
from modules.database_utils import user_sidebar

st.set_page_config(page_title='About', page_icon='static/mgh_logo.png', layout='wide')

with st.columns([1,4,1])[1]:
    st.title('About')
    st.markdown('''
                The mission of the [Webster Center for Quality and Safety](https://www.massgeneral.org/imaging/research/webster-center) encompasses all aspects of quality and safety in radiology \
                in addition to developing and promoting imaging methods that ensure the lowest achievable level of patient exposure to radiation.
                
                This web application aims to advance dose optimization in CT imaging by providing software tools to facilitate standardization of imaging protocols.

                This web application was developed using the Streamlit library in Python. 
                Firebase is used for user authentication and Google Cloud Storage for saving dose data.
                The code for this project can be accessed on [Github](https://github.com/nathanwangai/ct_dose_check).
                ''')   

    col1, col2, col3 = st.columns(3)
    with col1: 
        st.image('static/nathan.jpg', use_column_width=True)
        st.info('''
                **Nathan Wang** \\
                Senior @ Johns Hopkins University

                \\
                *Contributions* \\
                Programming the application in Python
                ''')
    with col2: 
        st.image('static/lina.png', use_column_width=True)
        st.info('''
                **Lina Karout, MD** \\
                Research fellow @ Massachusetts General Hospital

                *Contributions* \\
                Application design and project justification
                ''')
    with col3: 
        st.image('static/mannudeep.png', use_column_width=True)
        st.info('''
                **Mannudeep Kalra, MD**\\
                Director @ The Webster Center for Quality and Safety

                *Contributions* \\
                Creating the dose optimization recommendations \\
                Application design
                ''')
        
user_sidebar()