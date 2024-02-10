import streamlit as st
import modules.database_utils as db

st.set_page_config(page_title='Dose Tracker', page_icon='static/mgh_logo.png', layout='wide')

with st.columns([1,2.5,1])[1]:
    st.title('📊 Dose Tracker')

    if 'user' in st.session_state:
            path = st.session_state['path']

            if 'database' not in st.session_state:
                st.session_state['database'] = db.read_from_gcs(path)
            database = st.session_state['database']

            database = st.data_editor(
                database,
                column_config = {
                    'patient_type': st.column_config.SelectboxColumn(
                        'Patient Type',
                        options = ['Adult', 'Child'],
                        required = True
                    ),
                    'body_region': st.column_config.Column(
                        'Body Region',
                        disabled = True
                    ),
                    'selector': st.column_config.Column(
                        'Selector',
                        disabled = True
                    ),
                    'contrast': st.column_config.CheckboxColumn(
                        'Contrast',
                        required = True
                    ),
                    'ctdivol': st.column_config.NumberColumn(
                        'CTDIvol (mGy)',
                        required = True
                    ),
                    'dlp': st.column_config.NumberColumn(
                        'DLP (mGy*cm)',
                        required = True
                    )
                }, 
                num_rows='dynamic')

            if st.button('Save Changes'):
                database.to_csv(path, index=False)
                st.toast('Changes saved successfully!')
    else:
        st.info('''
                **Dose Tracker** compiles data inputted in **Dose Checker** for building local DRLs.
                Please log in to access this feature.
                ''')

    db.user_sidebar()
    