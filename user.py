import streamlit as st
import pandas as pd
from connector import get_data

st.title("👤 Pengaturan Akun")

def ShowData(data):
    raw = data
    df = pd.DataFrame(raw, columns=['Id', 'Tipe', 'Waktu', 'Nominal', 'Saldo'])
    df['Waktu'] = pd.to_datetime(df['Waktu'], unit='s')
    
    return df

def UserDetailForm():
    with st.container(border=True):
        st.subheader("Data Personal")
        st.write("#### Nama:")
        st.write("Haikal Ali")
        st.write("#### Email:")
        st.write("haikalali@student.telkomuniversity.ac.id")
        st.write("#### Nomor Telpon:")
        st.write("082213501842")
        st.write("#### PIN:")
        st.write("123456")

def HistoryTransaksi():
    with st.container(border=True):
        st.subheader("History Transaksi")
        
        data = ShowData(get_data())

        st.markdown(data.style.hide(axis="index").to_html(), unsafe_allow_html=True)

def PlotTransaksi():
    x = []
    y = []

    with st.container(border=True):
        st.subheader("Grafik Transaksi")
        data = get_data()

        for idx in range(len(data)):
            if data[idx][1] == "TABUNGAN":
                x.append(pd.to_datetime(data[idx][2], unit='s'))
                y.append(data[idx][3])

        df = pd.DataFrame(y, x)
        st.line_chart(df) 
            
def User():
    UserDetailForm()
    HistoryTransaksi()
    PlotTransaksi()

User()