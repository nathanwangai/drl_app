import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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

def dose_gauge_plot(ref_dose, dose, dose_type):

    color = 'green' if dose < ref_dose else 'red'
    suffix = ' mGy' if dose_type == 'CTDIvol' else ' mGy⋅cm'

    fig = go.Figure()
    fig.add_trace(go.Indicator(
            mode = "number+gauge",
            value = dose,
            number = {
                'suffix': suffix,
                'font.size': 42
            },
            gauge = {
                'axis': {'range': [0, 10*ref_dose], 
                         'tickfont': {'size': 32},
                         'tickcolor': 'black'},
                'bar': {'color': color},
                'bordercolor' : 'white',
                'steps': [
                    {'range': [0, ref_dose], 'color': 'lightgreen'},
                    {'range': [ref_dose, 10*ref_dose], 'color': 'pink'}
                ]
            }
        )
    )

    fig.add_annotation(x=0.5, y=0.45, 
                   text = dose_type,
                   font = {'size': 42},
                   showarrow = False,
    )

    fig.update_layout(
        width = 600,
        height = 300,
        margin = dict(t=50, b=20, l=100, r=100)
    )

    fig.write_image(f'static/{dose_type}_gauge.png')

    return None
