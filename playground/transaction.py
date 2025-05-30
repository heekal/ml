import streamlit as st
from datetime import datetime
from connector import init_db, get_balance, insert_data, get_zscore, get_last_nominal, get_last_trans
from anomaly import test_anomaly

def show_judul():
    st.title("💸 Transfer Rupiah")
    st.subheader("Transfer ke Penerima Baru")

def get_waktu():
    return int(datetime.now().timestamp())

def get_time_diff(waktu):
    last_trans_time = get_last_trans()
    return waktu - last_trans_time if last_trans_time else 0

def get_waktu_unix():
    now = datetime.now()
    unix = int(now.timestamp())
    return unix

def get_trans_diff(nominal):
    last = get_last_nominal()
    return nominal - last

@st.dialog("Verifikasi Transaksi")
def verifikasi(nominal, destination_account):
    st.write(f"Apakah Anda yakin ingin mengirim $ {nominal} ke rekening {destination_account}?")
    pin = st.text_input("Masukkan PIN Anda", type="password")
    
    # Get current timestamp for the new transaction
    current_waktu = get_waktu()
    
    # Get last transaction's timestamp
    last_trans_time = get_last_trans()
    
    # Calculate time since last transaction (in seconds)
    last = current_waktu - last_trans_time if last_trans_time else 0
    
    # Calculate z-score using current_waktu as cutoff
    zscore = get_zscore(current_waktu)
    
    # Check anomaly status
    is_anomaly = test_anomaly(last, nominal, last_trans_time, zscore)
    
    if is_anomaly == 0:
        if st.button("Kirim", type="primary"):
            insert_data('TABUNGAN', current_waktu, nominal)
            st.success("Transaksi berhasil dikirim.")
            st.rerun()
    else:
        st.warning("Transaksi ini kemungkinan anomali, apakah yakin untuk melanjutkan?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ya, Lanjutkan", type="secondary"):
                insert_data('TABUNGAN', current_waktu, nominal)
                st.success("Transaksi berhasil dikirim.")
                st.rerun()
        with col2:
            if st.button("Batal"):
                st.info("Transaksi dibatalkan.")
                st.rerun()

def show_rekening():
    st.write("Rekening Sumber")
    tabungan = get_balance()

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("#### TABUNGAN :material/check:")
            st.write("1103223071")
            st.badge(f"Saldo: $ {int(tabungan)}", color="green")

        with col3:
            st.image(r"res\mandiri-black.png", width=200)

def show_form():
    st.write("Rekening Tujuan")
    with st.form("transaction_form"):
        st.selectbox("🏛️ Nama Bank", ("Mandiri", "BCA", "BRI"))

        rekening_tujuan = st.text_input("Nomor Rekening Tujuan")
        nominal_transaksi = st.number_input("Nominal Transfer", min_value=0, step=1000)
        deskripsi = st.text_input("Keterangan (Opsional)")
        is_submitted = st.form_submit_button("Lanjutkan", type="primary")

        if is_submitted:
            if rekening_tujuan.isdigit():
                verifikasi(nominal_transaksi, rekening_tujuan)
            else:
                st.error('Data Rekening Tujuan Tidak Valid', icon='🚨')

def main():
    show_judul()
    show_rekening()
    show_form()

if __name__ == '__main__':
    init_db()
    main()
