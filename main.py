import streamlit as st
from connector import init_db, get_balance

def show_widget():
    tabungan = get_balance()

    with st.container(border=True):
        left, right = st.columns(2)

        with left:
            st.badge("TABUNGAN :material/check:", color="blue")
            st.write("1103223071")
            st.write(f"$ {int(tabungan)}")

        with right:
            st.image("res\mandiri-black.png")

def show_emoney():
    with st.container(border=True):
        left, right = st.columns(2)

        with left:
            st.badge("E-MONEY :material/star:", color="orange")
            st.write("082223223071")
            st.write("$ 100")

        with right:
            st.image("res\mandiri-emoney.png")

def show_fav():
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            border1 = st.container(border=True)
            border1.image(r"res\qris-icon.png", caption="QRIS")
        
        with col2:
            border2 = st.container(border=True)
            border2.image(r"res\topup-icon.png", caption="Top Up")

        with col3:
            border3 = st.container(border=True)
            border3.image(r"res\bayar-icon.png", caption="Bayar")
        
        with col4:
            border4 = st.container(border=True)
            border4.image(r"res\invest-icon.png", caption="Investasi")

        with col5:
            border5 = st.container(border=True)
            border5.image(r"res\transfer-icon.png", caption="Transfer")

        with col6:
            border6 = st.container(border=True)
            border6.image(r"res\setortarik-icon.png", caption="Setor Tarik")


def dashboard():
    st.title("Selamat Datang, Haikal!")

    col1, col2 = st.columns(2)
    
    with col1:
        show_widget()

    with col2:
        show_emoney()

    st.write("#####")
    st.subheader("Favourite :material/star:")

    show_fav()

def main():
    pages = {
        "Home" : [
            st.Page(dashboard, title="Dashboard 📊"),
            st.Page("transaction.py", title="Transfer Rupiah 💸")
        ],
        "Pengaturan" : [
            st.Page("user.py", title="Akun 👤")
        ]
    }

    pg = st.navigation(pages)
    pg.run()

if __name__ == '__main__':
    init_db()
    main()
