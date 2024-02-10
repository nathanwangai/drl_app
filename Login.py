import pandas as pd
import streamlit as st
import modules.database_utils as db

st.set_page_config(page_title='Login', page_icon='static/mgh_logo.png', layout='wide')

with st.columns([1,2.5,1])[1]:
    st.title('CT Dose Check')
    st.markdown('''
                Welcome to CT Dose Check: a free web application for radiation dose optimization! 
                Our tools can be accessed through the sidebar:

                - 🔍 **Dose Checker**
                : seamlessly check prescribed doses against national DRLs.
                - 📊 **Dose Tracker\***
                : analyze track record of doses to facilitate development of local DRLs. 

                **\****requires a user account. Please log in or register below.*
                ''')

    login_tab, register_tab, account_tab = st.tabs(['Login', 'Register', 'Account'])

    with login_tab:
        # log in form to authenticate user credentials with Firebase
        # upon successful login: stores user object, Google Cloud database path, and database dataframe in session state
        with st.form('Login'):
            st.header('Login')
            email = st.text_input(':email: Email', placeholder='user@gmail.com')
            password = st.text_input(':key: Password', placeholder='password', type='password')
            login = st.form_submit_button('Login')
        
        if login: 
            try:
                st.session_state['user'] = db.auth.sign_in_with_email_and_password(email, password)
                st.session_state['path'] = f'ct_dose_check_bucket/{email}/database.csv'
                st.session_state['database'] = db.read_from_gcs(st.session_state['path'])
                st.success(f'Successfully logged in as {email}!')
            except Exception as e: 
                st.error('Log in failed. Please check your credentials, register for an account, \
                         or reset your password in the Account tab.')

    with register_tab:
        # account registration form to create a new user (email/password) in Firebase
        # upon successful registration: creates blank database file in Google Cloud
        with st.form('Register'):
            st.header('Register')
            email = st.text_input(':email: Email', placeholder='user@gmail.com')
            password1 = st.text_input(':key: Password', placeholder='password', type='password')
            password2 = st.text_input(':key: Verify Password', placeholder='password', type='password')
            register = st.form_submit_button('Register') 

        if register and (password1 == password2):
            try: 
                db.auth.create_user_with_email_and_password(email, password1)
                df = pd.DataFrame(columns=['patient_type', 'body_region', 'specific', 'contrast', 'ctdivol', 'dlp'])
                db.write_to_gcs(df, f'ct_dose_check_bucket/{email}/database.csv')
                st.success(f'Successfully registered {email}! Please log in to continue.')
            except Exception as e:
                st.error('Account registration failed. Please ensure that the email is valid, \
                         the password is at least 6 characters, and the user does not already exist.')
        elif (password1 != password2):
            st.error('Passwords do not match. Please try again.')

    with account_tab:
        # password reset and account deletion forms
        with st.container(border=True):
            st.header('Account')
            email = st.text_input('Forgot Password', placeholder='user@gmail.com')
            
            if st.button('Send Reset Link'):
                try:
                    db.auth.send_password_reset_email(email)
                    st.success(f'Password reset email sent to {email}! Please also check your spam folder.')
                except Exception as e:
                    st.error('Password reset failed. Please ensure that the email is valid.')

            if 'user' in st.session_state:
                delete = st.text_input('Delete Account', placeholder='please type "DELETE" to confirm', 
                                    help='This action is permanent and you will lose access to all account data.')
                if st.button('Delete Account') and (delete == 'DELETE'):
                    try:
                        db.auth.delete_user_account(st.session_state['user']['idToken'])
                        db.delete_database_gcs(st.session_state['user']['email'])
                        st.session_state.pop('user')
                        st.session_state.pop('path')
                        st.session_state.pop('database')
                        st.rerun()
                    except Exception as e:
                        st.error('Account deletion failed.')
    
    st.markdown('''
                *Developed by [Nathan Wang](https://www.nathanwang-ai.com/) for the Massachusetts General Hospital Webster Center for Quality and Safety.*
                ''')

db.user_sidebar() # displays current user in sidebar with logout button