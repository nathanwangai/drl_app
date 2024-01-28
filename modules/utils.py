import pandas as pd
import streamlit as st
import plotly.graph_objects as go

@st.cache_data
def load_df(fname):
    """
    Loads and caches a DataFrame from a CSV file in 'drls' directory.

    Parameters:
    fname (str): Name of the CSV file.

    Returns:
    pandas.DataFrame: Loaded DataFrame.
    """
    
    return pd.read_csv(f'drls/{fname}')

@st.cache_data
def retrieve_ref_doses(df, col_name, choice, contrast=False):
    """
    Retrieves and caches reference doses (CTDIvol and DLP) from a DataFrame based on a specified choice.

    Parameters:
    df (pandas.DataFrame): DataFrame containing dose information.
    col_name (str): Column name in DataFrame to match with 'choice'.
    choice (str): Value in 'col_name' column to filter the DataFrame.
    contrast (bool, optional): If True, retrieves contrast-enhanced doses. Defaults to False.

    Returns:
    tuple: A tuple (ctdivol, dlp) containing the CTDIvol and DLP values.
    """

    if contrast:
        ctdivol = df[df[col_name] == choice]['CTDIvol_contrast'].values[0]
        dlp = df[df[col_name] == choice]['DLP_contrast'].values[0]
    else:
        ctdivol = df[df[col_name] == choice]['CTDIvol'].values[0]
        dlp = df[df[col_name] == choice]['DLP'].values[0]
        
    if (ctdivol != '-'): ctdivol = float(ctdivol)
    if (dlp != '-'): dlp = float(dlp)

    return ctdivol, dlp

def compare_doses(ref_dose, dose, dose_type):
    """
    Compares a dose against a reference dose and displays an error if it's higher.

    Parameters:
    ref_dose (float or str): Reference dose value or '-' to indicate no comparison.
    dose (float): Dose value to compare.
    dose_type (str): Description of the dose type for display in the message.

    Returns:
    bool: True if dose is not greater than reference dose, False otherwise.
    """

    if (ref_dose != '-' and dose > ref_dose):
        val = (dose/ref_dose - 1) * 100
        st.error(f'Unfortunately, your {dose_type} is {val:.0f}% greater than the suggested DRL.')
        return False
    
    return True

def dose_gauge_plot(ref_dose, dose, dose_type):
    """
    Creates and saves a gauge plot comparing a dose to a reference dose.

    Parameters:
    ref_dose (float): Reference dose for comparison.
    dose (float): Dose value to display.
    dose_type (str): Type of dose ('CTDIvol' or 'DLP'), affects labels.

    Returns:
    None: Saves the plot as an image, does not return a value.
    The plot is saved in 'static' directory with the filename '{dose_type}_gauge.png'.
    """
    
    bar_color = 'green' if dose < ref_dose else 'red'
    dose_units = ' mGy' if dose_type == 'CTDIvol' else ' mGy⋅cm'

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+gauge",
        value = dose,
        number = {
            'suffix': dose_units,
            'font': {'size': 42, 'color': 'black'}
        },
        gauge = {
            'axis': {'range': [0, 10*ref_dose],
                     'tickfont': {'size': 32, 'color': 'black'},
                     'tickcolor': 'black',
                     'tickwidth': 5,
                     'ticklen': 15},
            'bar': {'color': bar_color},
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
                   font = {'size': 42, 'color': 'black'},
                   showarrow = False,
    )

    fig.update_layout(
        width = 600,
        height = 300,
        margin = dict(t=50, b=20, l=100, r=100)
    )

    fig.write_image(f'static/{dose_type}_gauge.png')