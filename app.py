import streamlit as st
import sqlite3
import threading
import cv2
import qrcode

from datetime import datetime, date
from io import BytesIO

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from streamlit_autorefresh import st_autorefresh

# =========================
# MODULES
# =========================
from modules.auth import init_auth, login_page
from modules.db import (
    init_db,
    add_student,
    list_students,
    delete_student_and_attendance,
    npm_exists,
    add_attendance,
    list_attendance,
    already_marked_recent,
    already_marked_today,
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Absensi Mahasiswa", layout="wide")

# =========================
# AUTH (SATU GERBANG)
# =========================
init_auth()
if not st.session_state.logged_in:
    login_page()
    st.stop()

# =========================
# INIT DB
# =========================
init_db()

# =========================
# CSS
# =========================
def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a, #111827, #0b1220);
        }
        h1,h2,h3,h4,h5,h6,p,label,div {
            color: #e5e7eb !important;
        }
        .card {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.write(f"👤 Login sebagai **{st.session_state.username}**")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

# =========================
# QR GENERATOR
# =========================
def make_qr_png(payload: str) -> bytes:
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# =========================
# TABS
# =========================
tab0, tab1, tab2, tab3 = st.tabs(
    ["🏠 Dashboard", "➕ Mahasiswa", "📷 Scan QR", "📊 Rekap"]
)

# ======================================================
# DASHBOARD
# ======================================================
# ======================================================
# DASHBOARD (RINGKAS & LENGKAP)
# ======================================================
with tab0:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Dashboard Absensi")

    today = date.today()
    hari = today.strftime("%A")
    tanggal = today.strftime("%d %B %Y")

    st.caption(f"📅 **{hari}**, {tanggal}")

    # ======================
    # DATA RINGKAS
    # ======================
    students = list_students()
    total_students = len(students)

    rows_today = [
        r for r in list_attendance(limit=500)
        if r[0].startswith(today.isoformat())
    ]

    in_today = len([r for r in rows_today if r[3] == "IN"])
    out_today = len([r for r in rows_today if r[3] == "OUT"])

    c1, c2, c3 = st.columns(3)
    c1.metric("👨‍🎓 Total Mahasiswa", total_students)
    c2.metric("🟢 IN Hari Ini", in_today)
    c3.metric("🔴 OUT Hari Ini", out_today)

    st.divider()

    # ======================
    # GRAFIK IN vs OUT
    # ======================
    st.subheader("📊 Perbandingan IN & OUT (Hari Ini)")
    if in_today or out_today:
        st.bar_chart(
            {
                "Jumlah": {
                    "IN": in_today,
                    "OUT": out_today
                }
            }
        )
    else:
        st.info("Belum ada absensi hari ini")

    st.divider()

    # ======================
    # GRAFIK 7 HARI TERAKHIR
    # ======================
    st.subheader("📈 Absensi 7 Hari Terakhir")

    daily_count = {}
    all_rows = list_attendance(limit=1000)

    for r in all_rows:
        d = r[0][:10]
        daily_count[d] = daily_count.get(d, 0) + 1

    if daily_count:
        st.line_chart(daily_count)
    else:
        st.info("Belum ada data grafik")

    st.divider()

    # ======================
    # AKTIVITAS TERAKHIR
    # ======================
    st.subheader("🕒 Aktivitas Terakhir")

    last_rows = list_attendance(limit=5)
    if last_rows:
        for r in last_rows:
            icon = "🟢" if r[3] == "IN" else "🔴"
            st.write(
                f"{icon} **{r[1]} – {r[2]}** | {r[3]} | {r[0]}"
            )
    else:
        st.info("Belum ada aktivitas absensi")

    st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# MAHASISWA
# ======================================================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Tambah Mahasiswa")

    npm = st.text_input("NPM")
    nama = st.text_input("Nama")
    kelas = st.text_input("Kelas (opsional)")

    if st.button("Simpan"):
        if npm and nama:
            try:
                add_student(npm.strip(), nama.strip(), kelas.strip() if kelas else None)
                st.success("Mahasiswa berhasil ditambahkan")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("NPM sudah terdaftar")
        else:
            st.warning("NPM dan Nama wajib diisi")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Daftar Mahasiswa")

    students = list_students()
    if students:
        for s in students:
            st.write(f"{s[0]} | {s[1]} | {s[2]}")
            st.download_button(
                "⬇️ QR Code",
                make_qr_png(s[0]),
                file_name=f"{s[0]}.png",
                key=f"qr_{s[0]}",
            )
    else:
        st.info("Belum ada mahasiswa")

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# SCAN QR (FIX TOTAL)
# ======================================================
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📷 Scan QR Absensi")

    att_type = st.selectbox("Jenis Absensi", ["IN", "OUT"])

    class QRScanner(VideoTransformerBase):
        def __init__(self):
            self.detector = cv2.QRCodeDetector()
            self.lock = threading.Lock()
            self.last_status = None
            self.last_seen_id = None
            self.last_seen_time = None

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")

            # ==== WAJIB: GRAYSCALE (LEBIH AKURAT)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            data, points, _ = self.detector.detectAndDecode(gray)

            # DEBUG RAW (WAJIB ADA)
            cv2.putText(
                img,
                f"RAW: {data}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

            if not data:
                return img

            now = datetime.now()

            # ==== ANTI SPAM 1.5 DETIK
            if self.last_seen_id == data and self.last_seen_time:
                if (now - self.last_seen_time).total_seconds() < 1.5:
                    return img

            self.last_seen_id = data
            self.last_seen_time = now

            if not npm_exists(data):
                self.last_status = "❌ NPM tidak terdaftar"
                return img

            if already_marked_today(data, att_type):
                self.last_status = "⚠️ Sudah absen hari ini"
                return img

            add_attendance(data, att_type, None, None)
            self.last_status = f"✅ {data} absen {att_type}"

            return img

    ctx = webrtc_streamer(
        key=f"qr_scanner_{att_type}",
        video_processor_factory=QRScanner,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if ctx and ctx.video_processor and ctx.video_processor.last_status:
        st.success(ctx.video_processor.last_status)

    if ctx and ctx.state and ctx.state.playing:
        st_autorefresh(interval=500, key="qr_refresh")

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# REKAP
# ======================================================
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Rekap Absensi")

    rows = list_attendance(limit=200)
    if rows:
        st.dataframe(
            [{
                "Waktu": r[0],
                "NPM": r[1],
                "Nama": r[2],
                "Tipe": r[3]
            } for r in rows],
            use_container_width=True
        )
    else:
        st.info("Belum ada data")

    st.markdown('</div>', unsafe_allow_html=True)
