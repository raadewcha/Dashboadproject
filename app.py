import os 
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")

def read_csv_robust(path):
    for enc in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        for sep in [",", ";", "\t"]:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, engine="python")
                if df.shape[1] >= 2:
                    return df
            except Exception:
                continue
    raise ValueError(f"Gagal membaca file: {path}")

def load_datasets():
    files = {
        "Inflasi": "Inflasi_Provinsi_Sumsel_Baru.csv",
        "Nilai Tukar Petani": "Perkembangan_Nilai_Tukar_Petani.csv",
        "Nilai Impor": "Nilai_Impor_Bulanan.csv",
        "Kedalaman Kemiskinan": "Indeks_Kedalaman_Kemiskinan.csv",
        "Penduduk Menurut Umur Sekolah": "Penduduk_Menurut_Umur_Sekolah.csv"  # tambahkan jika file ini ada
    }

    data = {}
    for key, fname in files.items():
        fpath = os.path.join(DATA_DIR, fname)
        if os.path.exists(fpath):
            df = read_csv_robust(fpath).dropna(how="all")
            data[key] = df
            print(f"[OK] {fname} dimuat -> {df.shape}")
        else:
            print(f"[MISS] Tidak ditemukan: {fname}")

    if "Penduduk Menurut Umur Sekolah" in data:
        df = data["Penduduk Menurut Umur Sekolah"].copy()
        df.columns = ["Kelompok Umur", "Tidak/Belum Pernah Sekolah", "Masih Sekolah", "Tidak Sekolah Lagi"]
        df = df.dropna(subset=["Kelompok Umur"])
        df = df[~df["Kelompok Umur"].str.contains("Persentase|NaN|2024", na=False)]
        df = df[df["Kelompok Umur"].str.contains(r"\d", na=False)]  # hanya baris dengan angka umur
        data["Penduduk Menurut Umur Sekolah"] = df.reset_index(drop=True)
        print("[CLEAN] Dataset 'Penduduk Menurut Umur Sekolah' telah dibersihkan")

    return data

datasets = load_datasets()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server

navbar = dbc.Navbar(
    dbc.Container([
        html.A([
            html.Img(src="https://www.bps.go.id/favicon.ico", height="45px"),
            dbc.NavbarBrand(
                "Dashboard Ekonomi Daerah - Provinsi Sumatera Selatan",
                className="ms-3",
                style={"fontWeight": "bold", "color": "white", "fontSize": "20px"}
            )
        ], href="#", style={"textDecoration": "none", "display": "flex", "alignItems": "center"}),
    ]),
    color="#003366",
    dark=True,
    sticky="top",
    className="shadow-sm"
)

sidebar = dbc.Card([
    html.H5("📊 Filter Data", className="text-primary fw-bold"),
    html.Hr(),
    html.Label("Pilih Indikator"),
    dcc.Dropdown(
        id="indikator",
        options=[{"label": k, "value": k} for k in datasets.keys()],
        value=list(datasets.keys())[0] if datasets else None,
        clearable=False,
        className="mb-3"
    ),
    html.Label("Pilih Periode"),
    dcc.Dropdown(
        id="periode",
        placeholder="Pilih periode (opsional)",
        clearable=True,
        className="mb-3"
    ),
    dbc.Button("⬇️ Unduh Data CSV", id="btn-download", color="primary", className="w-100 mb-3"),
    dcc.Download(id="download-data"),
    html.Hr(),
    html.Small("📌 Sumber data: Publikasi resmi BPS Provinsi Sumatera Selatan.",
               style={"color": "#555"})
], body=True, style={
    "height": "90vh",
    "backgroundColor": "#f9f9f9",
    "overflowY": "auto",
    "overflowX": "hidden",
    "padding": "15px"
})

def make_card(judul, id_value, id_sub):
    return dbc.Card(
        dbc.CardBody([
            html.H6(judul, className="text-primary fw-bold"),
            html.H3(id=id_value, children="-", className="fw-bold"),
            html.Small(id=id_sub, className="text-muted")
        ]),
        className="shadow-sm",
        style={"margin": "5px", "textAlign": "center"}
    )

cards = dbc.Row([
    dbc.Col(make_card("Nilai Terakhir", "val-terakhir", "sub-terakhir")),
    dbc.Col(make_card("Perubahan (m-1)", "val-diff", "sub-diff")),
    dbc.Col(make_card("Rata-rata", "val-mean", "sub-mean")),
    dbc.Col(make_card("Nilai Maksimum", "val-max", "sub-max")),
], className="mb-4")

app.layout = dbc.Container([
    navbar,
    html.Br(),
    dbc.Row([
        dbc.Col(sidebar, width=3),
        dbc.Col([
            html.Div([
                html.H4("📈 Visualisasi Data Ekonomi Sumatera Selatan",
                        style={"color": "#003366", "fontWeight": "bold"}),
                html.P("Dashboard interaktif untuk menampilkan tren indikator ekonomi daerah secara visual dan informatif.",
                       style={"color": "#555"})
            ]),
            html.Hr(),
            cards,
            dcc.Graph(id="grafik-utama", style={"height": "500px"}),
            html.Div(id="table-container", style={"marginTop": "20px"})
        ], width=9)
    ])
], fluid=True, style={"backgroundColor": "#eef2f5"})

@app.callback(
    [Output("periode", "options"), Output("periode", "value")],
    Input("indikator", "value")
)
def update_periode(indikator):
    if indikator not in datasets:
        return [], None
    df = datasets[indikator]
    if df.empty:
        return [], None
    col0 = df.columns[0]
    options = [{"label": str(v), "value": str(v)} for v in df[col0].astype(str).unique()]
    return options, None

@app.callback(
    [Output("grafik-utama", "figure"),
     Output("val-terakhir", "children"),
     Output("sub-terakhir", "children"),
     Output("val-diff", "children"),
     Output("sub-diff", "children"),
     Output("val-mean", "children"),
     Output("sub-mean", "children"),
     Output("val-max", "children"),
     Output("sub-max", "children"),
     Output("table-container", "children")],
    [Input("indikator", "value"), Input("periode", "value")]
)
def update_dashboard(indikator, periode):
    if indikator not in datasets:
        return px.scatter(), "-", "", "-", "", "-", "", "-", "", html.Div("Tidak ada data")

    df = datasets[indikator].copy().dropna(how="all")
    if df.shape[1] < 2:
        return px.scatter(), "-", "", "-", "", "-", "", "-", "", html.Div("Data tidak valid")

    x_col, y_col = df.columns[0], df.columns[1]
    df[y_col] = df[y_col].astype(str).str.replace("%", "").str.replace(",", ".")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=[y_col])
    df[x_col] = df[x_col].astype(str).str.strip()

    df = df.sort_values(by=x_col, ascending=True)
    fig = px.line(df, x=x_col, y=y_col, markers=True, line_shape='spline',
                  title=f"Tren {indikator} di Provinsi Sumatera Selatan",
                  color_discrete_sequence=["#003366"])
    fig.update_layout(template="plotly_white", title_x=0.5,
                      title_font=dict(size=20, color="#003366"))

    if df.empty:
        return fig, "-", "", "-", "", "-", "", "-", "", html.Div("Data kosong")

    last_val = df[y_col].iloc[-1]
    last_label = df[x_col].iloc[-1]
    prev_val = df[y_col].iloc[-2] if len(df) > 1 else None
    diff = last_val - prev_val if prev_val is not None else 0
    mean_val = df[y_col].mean()
    max_val = df[y_col].max()

    table = dbc.Table.from_dataframe(df.tail(10), striped=True, bordered=True, hover=True, responsive=True)

    return (
        fig,
        f"{last_val:.2f}", f"Periode: {last_label}",
        f"{diff:+.2f}" if prev_val is not None else "-", f"Sebelumnya: {prev_val:.2f}" if prev_val else "-",
        f"{mean_val:.2f}", "Rata-rata periode",
        f"{max_val:.2f}", "Nilai maksimum",
        html.Div([
            html.H5("📋 Tabel 10 Baris Terakhir", className="text-primary fw-bold"),
            table
        ])
    )

@app.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    State("indikator", "value"),
    prevent_initial_call=True
)
def download_csv(n_clicks, indikator):
    if indikator not in datasets:
        return None
    df = datasets[indikator]
    return dcc.send_data_frame(df.to_csv, f"{indikator}_Sumsel.csv", index=False)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
