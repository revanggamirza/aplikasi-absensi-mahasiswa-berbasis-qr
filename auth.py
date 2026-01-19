import streamlit as st

# ==========================
# Inisialisasi Session
# ==========================
def init_auth():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None


# ==========================
# Halaman Login
# ==========================
def login_page():
    st.title("🔐 Login Admin")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        # LOGIN SIMPLE (SESUIAI PERMINTAAN DOSEN)
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username atau password salah")
