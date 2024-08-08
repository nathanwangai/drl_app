import csv
import streamlit as st
from collections import Counter

weight_groups_europe = {
    '<5 kg': [0, 5],
    '5-15 kg': [5, 15],
    '15-30 kg': [15, 30],
    '30-50 kg': [30, 50],
    '50-80 kg': [50, 80],
    '>80 kg': [80, 999]
}

age_groups_europe = {
    '0-3 months': [0, 3/12],
    '3-12 months': [3/12, 1],
    '1-6 years': [1, 6],
    '>6 years': [6, 999]
}

age_groups_us_head = {
    '0-1 year': [0, 1],
    '1-2 years': [1, 2],
    '2-6 years': [2, 6],
    '6-18 years': [6, 18],
    '>18 years': [18, 999]
}

age_groups_us_other = {
    '0-1 year': [0, 1],
    '1-5 years': [1, 5],
    '5-10 years': [5, 10],
    '10-15 years': [10, 15],
    '15-18 years': [15, 18],
    '>18 years': [18, 999]
}

def num_to_category(num, categories):
    for key, value in categories.items():
        if value[0] <= num < value[1]: 
            return key

@st.cache_data
def load_drls():
    drls = []
    with open('../drls.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            drls.append(row)
    return drls

drls = load_drls()
        
def get_drl_doses(data, country):
    data = data.copy()
    for key in ['gender', 'ctdivol', 'dlp']: data.pop(key)
    data = {k: v for k, v in data.items() if v is not None}
    data['country'] = country

    if country == 'United States':
        data.pop('weight', None)

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

    return [row[-2:] for row in drls if Counter(data) == Counter(row[:-2])]
