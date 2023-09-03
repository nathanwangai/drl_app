import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

'''
- USAGE: creates dose warning bar plot
- ref_dose: dose suggested by DRL
- dose: theoretical examination dose
'''
def create_dose_bars(title, ref_dose, dose):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.barh(' ', ref_dose, color='green', alpha=0.15)
    ax.barh(' ', ref_dose*2, left=ref_dose, color='red', alpha=0.15)

    # hide borders and y-axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax.set_xticks(np.arange(4) * ref_dose)
    ax.tick_params(axis='x', labelsize=24)
    ax.xaxis.set_tick_params(width=3, length=9)

    ax.axvline(x=dose, color='red', linestyle='--', lw=4)
    ax.set_title(title, fontsize=24)
    st.pyplot(fig)

'''
- USAGE: retrieves DRL values of CTDIvol and DLP
- df: dataframe for the DRL csv file
- key: variable to retrieve DRL (e.g. age or weight)
- contrast_usage: 'Without contrast' or 'With contrast'
'''
def retrieve_ref_doses(df, key, contrast_usage=None):
    col_name = df.columns[0]

    if (contrast_usage == 'With contrast'): 
        ctdi_type = 'CTDIvol_w_contrast'
        dlp_type = 'DLP_w_contrast'
    elif (contrast_usage == 'Without contrast'):
        ctdi_type = 'CTDIvol_wo_contrast'
        dlp_type = 'DLP_wo_contrast'
    else:
        ctdi_type = 'CTDIvol'
        dlp_type = 'DLP'
    
    ref_ctdivol = df[df[col_name] == key][ctdi_type].values[0]
    ref_dlp = df[df[col_name] == key][dlp_type].values[0]
    if (ref_ctdivol != '-'): ref_ctdivol = float(ref_ctdivol)
    if (ref_dlp != '-'): ref_dlp = float(ref_dlp)

    return ref_ctdivol, ref_dlp

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