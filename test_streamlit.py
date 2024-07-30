import streamlit as st
import numpy as np
import pandas as pd

@st.cache_data

def color_test2(x, color):
    return np.where(x.startswith("00"), f"color: {color};", 'color:blue;')

def convert_df(df):
    return df.to_csv(index=False, header=None).encode('latin1')
#df.to_csv(encoding='latin1',sep=',', index=False, header=None)

def color_alert_max_10000(v):
    props='color:red;'
    return props if not v.lower().startswith("00") else None

def color_causa(v):
    props='color:red;'
    #props="red"
    return props if not v in cause_list else None

def max_correction(df_intern):
    for idx,elements in enumerate(df_intern.iloc[:,10]):
        if  not elements.lower().startswith("00"):
            df_intern.iloc[idx,10]="009999.99"
    return df_intern

cause_list = ["DIS2", "OTR2", "VAN3"]


st.set_page_config(layout="wide")
st.title('Correción de archivo FALLAS para carga de bases móviles')

uploaded_file = st.file_uploader("Seleccione el archivo .txt de FALLAS",type='txt')

if uploaded_file is not None and uploaded_file.name.startswith("FALLA"):
    st.write("Archivo abierto:", uploaded_file.name)
    df = pd.read_csv(uploaded_file, dtype="object", encoding='latin1', header=None)
    s1 = df.style.map(color_causa,subset=pd.IndexSlice[:,[12]])\
        .map(color_alert_max_10000,subset=pd.IndexSlice[:,[10]])
    #s2 = df.style.apply(color_test2, color='green',subset=pd.IndexSlice[:,[12]])\
    #    .apply(color_alert_max_10000, subset=pd.IndexSlice[:,[10]])
    #s2 = df.style.applymap(color_alert_max_10000,subset=pd.IndexSlice[:,[10]])
    #s2 = df.style.map(color_alert_max_10000,subset=pd.IndexSlice[:,[10]])

    st.dataframe(s1)

    if st.button("Corregir"):
        
        df2=max_correction(df)
        s2 = df2.style.map(color_causa,subset=pd.IndexSlice[:,[12]])\
            .map(color_alert_max_10000,subset=pd.IndexSlice[:,[10]])
        
        st.dataframe(s2)
        csv=convert_df(df2)
        st.download_button(
            "Descargar",
            csv,
            uploaded_file.name,
            key='download-csv'
        )
