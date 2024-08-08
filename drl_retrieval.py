import sys
import streamlit as st

sys.path.append('C:/Users/natha/Desktop/ct_dose_check') # force Python to check this directory for imported modules
from modules.drl_utils import * # conversion dictionaries, drls, num_to_category(), get_drl_doses()
from collections import Counter
from modules.app_components import demographic_input, protocol_input, system_parameters_input

def get_drl_doses_test(data, country):
    data = data.copy()
    for key in ['gender', 'ctdivol', 'dlp']: data.pop(key)
    data = {k: v for k, v in data.items() if v is not None}
    data['country'] = country

    if data['country'] == 'United States':
        data.pop('weight', None)
        if 'indication' in data: data.pop('contrast') 

        if data['patient_type'] == 'Child':
            if data['body_region'] == 'Head':
                data['age'] = num_to_category(data['age'], age_groups_us_head)
            else:
                data['age'] = num_to_category(data['age'], age_groups_us_other)
        else:
            data.pop('age')

    else:
        data.pop('contrast')

        if data['patient_type'] == 'Child':
            if data['body_region'] == 'Head':
                data.pop('weight', None)
                data['age'] = num_to_category(data['age'], age_groups_europe)
            else:
                data.pop('age')
                if 'weight' in data: data['weight'] = num_to_category(data['weight'], weight_groups_europe)
        else:
            data.pop('weight', None)
            data.pop('age')

    st.write(data)
    data = data.values()
    matches = [row[-2:] for row in drls if Counter(data) == Counter(row[:-2])]

    if len(matches) > 0:
        ret = []
        for n in matches[0]:
            ret.append(float(n) if n != '-' else n)
        return ret
    return None

st.dataframe(drls)
col_1, col_2 = st.columns(2)
with col_1:
    gender, patient_type, age, weight = demographic_input()
    body_region, indication, contrast = protocol_input(patient_type)
    ctdivol, dlp = system_parameters_input()

with col_2:
    with st.container(border=True):
        st.subheader('**User Input**')
        col_names = ['gender', 'patient_type', 'age', 'weight', 'body_region', 'indication', 'contrast', 'ctdivol', 'dlp']
        input_data = (gender, patient_type, age, weight, body_region, indication, contrast, ctdivol, dlp)
        input_data = dict(zip(col_names, input_data))
        st.write(input_data)

    with st.container(border=True):
        st.subheader('**DRLs**')
        europe_drl = get_drl_doses_test(input_data, 'Europe')
        us_drl = get_drl_doses_test(input_data, 'United States')

        if europe_drl is not None:
            st.success(f'European CTDIvol, DLP: {europe_drl[0], europe_drl[1]}')
        else:
            st.error('European DRLs unavailable') 

        if us_drl is not None:
            st.success(f'United States CTDIvol, DLP: {us_drl[0], us_drl[1]}')
        else:
            st.error('United States DRLs unavailable')  