import pandas as pd
import plotly.express as px

def absensi_per_tanggal(data):
    df = pd.DataFrame(
        data,
        columns=["id", "nama", "nim", "tanggal", "waktu"]
    )
    count = df.groupby("tanggal").size().reset_index(name="jumlah")
    fig = px.bar(
        count,
        x="tanggal",
        y="jumlah",
        title="Jumlah Absensi per Tanggal"
    )
    return fig
