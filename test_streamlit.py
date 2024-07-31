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
    return None if not v in cause_list else None

def max_correction(df_intern):
    for idx,elements in enumerate(df_intern.iloc[:,10]):
        if  not elements.lower().startswith("00"):
            df_intern.iloc[idx,10]="009999.99"
    return df_intern

cause_list=["ACC1","ACC2","ACC3","ACC4","ACC5","ANI1","ARB1","ARB2","AUT1","CLI1","CLI2","COM1","COM2","DIS1","DIS2","DIS3","DIS4","DIS5","DIS6","DIS7","INC1","OPE1","OPE10","OPE11","OPE12","OPE13","OPE14","OPE16","OPE17","OPE18","OPE19","OPE2","OPE20","OPE21","OPE22","OPE23","OPE3","OPE4","OPE5","OPE6","OPE7","OPE8","OPE9","OTR2","VAN1","VAN2","VAN3"]


st.set_page_config(layout="wide")
st.title('Correción de archivo FALLA para carga de bases móviles')

uploaded_file = st.file_uploader("Seleccione el archivo FALLA*.txt",type='txt')

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
