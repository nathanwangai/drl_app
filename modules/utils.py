import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#####
@st.cache_data
def retrieve_ref_doses(df, col_name, choice, contrast=False):
    if contrast:
        ctdivol = df[df[col_name] == choice]['CTDIvol_contrast'].values[0]
        dlp = df[df[col_name] == choice]['DLP_contrast'].values[0]
    else:
        ctdivol = df[df[col_name] == choice]['CTDIvol'].values[0]
        dlp = df[df[col_name] == choice]['DLP'].values[0]
        
    if (ctdivol != '-'): ctdivol = float(ctdivol)
    if (dlp != '-'): dlp = float(dlp)

    return ctdivol, dlp

@st.cache_data
def load_df(fname):
    return pd.read_csv(f'drls/{fname}')

def compare_doses(ref_dose, dose, dose_type):
    if (ref_dose != '-' and dose > ref_dose):
        val = (dose/ref_dose - 1) * 100
        st.error(f'Unfortunately, your {dose_type} is {val:.0f}% greater than the suggested DRL.')
        return False
    
    return True

#####

'''
- USAGE: loads a csv file containing DRL values
- id1: 'child' or 'adult'
- id2: 'head', 'chest', 'abdomen', 'regions', or 'indicators'
'''
def load_ref_helper(id1, id2, use_europe): 
    if use_europe:
        country = 'uk' if (id2 == 'regions') else 'europe'
        fpath = f'drl_references/europe/{country}_{id1.lower()}_{id2.lower()}.csv'
    else:
        fpath = f'drl_references/united_states/us_{id1.lower()}_{id2.lower()}.csv'

    return pd.read_csv(fpath)

def create_dose_bars(title, ref_dose, dose):
    '''
    - creates dose warning bar plot

    Args:
    - ref_dose: dose suggested by DRL
    - dose: theoretical examination dose

    Returns: nothing
    '''
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.barh(' ', ref_dose, color='green', alpha=0.15)
    ax.barh(' ', ref_dose*9, left=ref_dose, color='red', alpha=0.15)

    # hide borders and y-axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax.set_xticks(np.arange(6) * 2*ref_dose)
    ax.tick_params(axis='x', labelsize=24)
    ax.xaxis.set_tick_params(width=3, length=9)

    ax.axvline(x=dose, color='red', linestyle='--', lw=4)
    ax.set_title(title, fontsize=24)
    return st.pyplot(fig)

'''
- USAGE: returns False (meaning unsafe) if dose exceeds the DRL
- ref_dose: dose suggested by DRL
- dose: theoretical examination dose
- name: 'CTDIvol' or 'DLP'
'''
def compare_doses(ref_dose, dose, name):
    if (ref_dose != '-' and dose > ref_dose):
        val = (dose/ref_dose - 1) * 100
        st.error(f'Unfortunately, your {name} is {val:.0f}% greater than the suggested DRL.')
        return False
    
    return True