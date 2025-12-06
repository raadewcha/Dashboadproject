import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx, no_update
import dash_bootstrap_components as dbc
from database import (
    InflasiCRUD,
    NilaiTukarPetaniCRUD,
    NilaiImporCRUD,
    KedalamanKemiskinanCRUD,
    PendudukUmurSekolahCRUD,
)
from crud_ui import get_crud_layout, register_crud_callbacks
from auth import get_login_layout, check_authentication, login_user, logout_user


def transform_inflasi_data():
    df = InflasiCRUD.get_all()
    if df.empty:
        return pd.DataFrame()
    df_melted = df.melt(
        id_vars=["id", "kota", "tahun"],
        value_vars=[
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
        ],
        var_name="Bulan",
        value_name="Inflasi",
    )
    df_melted = df_melted.dropna(subset=["Inflasi"])
    return df_melted[["Bulan", "Inflasi"]]


def transform_ntp_data():
    df = NilaiTukarPetaniCRUD.get_all()
    if df.empty:
        return pd.DataFrame()
    df_melted = df.melt(
        id_vars=["id", "jenis_ntp", "tahun"],
        value_vars=[
            "januari",
            "februari",
            "maret",
            "april",
            "mei",
            "juni",
            "juli",
            "agustus",
            "september",
            "oktober",
            "november",
            "desember",
        ],
        var_name="Bulan",
        value_name="Nilai",
    )
    df_melted = df_melted.dropna(subset=["Nilai"])
    return df_melted[["Bulan", "Nilai"]]


def transform_impor_data():
    df = NilaiImporCRUD.get_all()
    if df.empty:
        return pd.DataFrame()
    return df[["bulan", "nilai"]].rename(
        columns={"bulan": "Bulan", "nilai": "Nilai Impor"}
    )


def transform_kemiskinan_data():
    df = KedalamanKemiskinanCRUD.get_all()
    if df.empty:
        return pd.DataFrame()
    return df[["kabupaten_kota", "indeks"]].rename(
        columns={"kabupaten_kota": "Kabupaten/Kota", "indeks": "Indeks"}
    )


def transform_penduduk_data():
    df = PendudukUmurSekolahCRUD.get_all()
    if df.empty:
        return pd.DataFrame()
    return df[
        ["kelompok_umur", "tidak_belum_sekolah", "masih_sekolah", "tidak_sekolah_lagi"]
    ].rename(
        columns={
            "kelompok_umur": "Kelompok Umur",
            "tidak_belum_sekolah": "Tidak/Belum Pernah Sekolah",
            "masih_sekolah": "Masih Sekolah",
            "tidak_sekolah_lagi": "Tidak Sekolah Lagi",
        }
    )


def load_datasets():
    data = {}
    try:
        df_inflasi = transform_inflasi_data()
        if not df_inflasi.empty:
            data["Inflasi"] = df_inflasi
            print(f"[OK] Inflasi dimuat dari database -> {df_inflasi.shape}")
    except Exception as e:
        print(f"[ERROR] Inflasi: {e}")

    try:
        df_ntp = transform_ntp_data()
        if not df_ntp.empty:
            data["Nilai Tukar Petani"] = df_ntp
            print(f"[OK] Nilai Tukar Petani dimuat dari database -> {df_ntp.shape}")
    except Exception as e:
        print(f"[ERROR] Nilai Tukar Petani: {e}")

    try:
        df_impor = transform_impor_data()
        if not df_impor.empty:
            data["Nilai Impor"] = df_impor
            print(f"[OK] Nilai Impor dimuat dari database -> {df_impor.shape}")
    except Exception as e:
        print(f"[ERROR] Nilai Impor: {e}")

    try:
        df_kemiskinan = transform_kemiskinan_data()
        if not df_kemiskinan.empty:
            data["Kedalaman Kemiskinan"] = df_kemiskinan
            print(
                f"[OK] Kedalaman Kemiskinan dimuat dari database -> {df_kemiskinan.shape}"
            )
    except Exception as e:
        print(f"[ERROR] Kedalaman Kemiskinan: {e}")

    try:
        df_penduduk = transform_penduduk_data()
        if not df_penduduk.empty:
            data["Penduduk Menurut Umur Sekolah"] = df_penduduk
            print(
                f"[OK] Penduduk Menurut Umur Sekolah dimuat dari database -> {df_penduduk.shape}"
            )
    except Exception as e:
        print(f"[ERROR] Penduduk Menurut Umur Sekolah: {e}")

    return data


datasets = load_datasets()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server
server.secret_key = "dashboard-ekonomi-sumsel-2024-secret-key"

from crud_routes import register_crud_routes

register_crud_routes(server)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                [
                    html.Img(src="/assets/logo.png", height="45px"),
                    dbc.NavbarBrand(
                        "Dashboard Ekonomi Daerah - Provinsi Sumatera Selatan",
                        className="ms-3",
                        style={
                            "fontWeight": "bold",
                            "color": "white",
                            "fontSize": "20px",
                        },
                    ),
                ],
                href="/",
                style={
                    "textDecoration": "none",
                    "display": "flex",
                    "alignItems": "center",
                },
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                "📊 Dashboard",
                                id="nav-dashboard",
                                href="/",
                                className="text-white fw-bold",
                                active="exact",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "Manajemen Data",
                                id="nav-crud",
                                href="/crud",
                                className="text-white fw-bold",
                                active="exact",
                            )
                        ),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="#003366",
    dark=True,
    sticky="top",
    className="shadow-sm",
)

sidebar = dbc.Card(
    [
        html.H5("📊 Filter Data", className="text-primary fw-bold"),
        html.Hr(),
        html.Label("Pilih Indikator"),
        dcc.Dropdown(
            id="indikator",
            options=[{"label": k, "value": k} for k in datasets.keys()],
            value=list(datasets.keys())[0] if datasets else None,
            clearable=False,
            className="mb-3",
        ),
        html.Label("Pilih Kabupaten/Kota"),
        dcc.Dropdown(
            id="kabupaten",
            placeholder="Semua Kabupaten/Kota",
            clearable=True,
            className="mb-3",
        ),
        html.Label("Pilih Periode"),
        dcc.Dropdown(
            id="periode",
            placeholder="Pilih periode (opsional)",
            clearable=True,
            className="mb-3",
        ),
        dbc.Button(
            "⬇️ Unduh Data CSV",
            id="btn-download",
            color="primary",
            className="w-100 mb-3",
        ),
        dcc.Download(id="download-data"),
        html.Hr(),
        html.Small(
            "📌 Sumber data: Publikasi resmi BPS Provinsi Sumatera Selatan.",
            style={"color": "#555"},
        ),
    ],
    body=True,
    style={
        "height": "90vh",
        "backgroundColor": "#f9f9f9",
        "overflowY": "auto",
        "overflowX": "hidden",
        "padding": "15px",
    },
)


def make_card(judul, id_value, id_sub):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(judul, className="text-primary fw-bold"),
                html.H3(id=id_value, children="-", className="fw-bold"),
                html.Small(id=id_sub, className="text-muted"),
            ]
        ),
        className="shadow-sm",
        style={"margin": "5px", "textAlign": "center"},
    )


cards = dbc.Row(
    [
        dbc.Col(make_card("Nilai Terakhir", "val-terakhir", "sub-terakhir")),
        dbc.Col(make_card("Perubahan (m-1)", "val-diff", "sub-diff")),
        dbc.Col(make_card("Rata-rata", "val-mean", "sub-mean")),
        dbc.Col(make_card("Nilai Maksimum", "val-max", "sub-max")),
    ],
    className="mb-4",
)

dashboard_layout = dbc.Row(
    [
        dbc.Col(sidebar, width=3),
        dbc.Col(
            [
                html.Div(
                    [
                        html.H4(
                            "📈 Visualisasi Data Ekonomi Sumatera Selatan",
                            style={"color": "#003366", "fontWeight": "bold"},
                        ),
                        html.P(
                            "Dashboard interaktif untuk menampilkan tren indikator ekonomi daerah secara visual dan informatif.",
                            style={"color": "#555"},
                        ),
                    ]
                ),
                html.Hr(),
                cards,
                dcc.Graph(id="grafik-utama", style={"height": "500px"}),
                html.Div(id="table-container", style={"marginTop": "20px"}),
            ],
            width=9,
        ),
    ]
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Br(),
        html.Div(id="page-content"),
    ],
    fluid=True,
    style={"backgroundColor": "#eef2f5"},
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/crud":
        if check_authentication():
            return get_crud_layout()
        return get_login_layout()
    elif pathname == "/login":
        return get_login_layout()
    return dashboard_layout


@app.callback(
    [
        Output("url", "pathname", allow_duplicate=True),
        Output("login-alert-container", "children"),
    ],
    Input("btn-login", "n_clicks"),
    [
        State("login-username", "value"),
        State("login-password", "value"),
        State("url", "pathname"),
    ],
    prevent_initial_call=True,
)
def handle_login(n_clicks, username, password, current_path):
    if not n_clicks:
        return no_update, no_update

    if not username or not password:
        return no_update, dbc.Alert(
            "❌ Username dan password harus diisi!",
            color="warning",
            dismissable=True,
        )

    if login_user(username, password):
        return "/crud", no_update
    else:
        return no_update, dbc.Alert(
            "❌ Username atau password salah!",
            color="danger",
            dismissable=True,
        )


register_crud_callbacks(app)


app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            fetch('/logout', {method: 'POST'})
                .then(() => window.location.href = '/');
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("btn-logout", "n_clicks"),
    Input("btn-logout", "n_clicks"),
    prevent_initial_call=True,
)


@app.callback(
    [
        Output("kabupaten", "options"),
        Output("kabupaten", "value"),
        Output("periode", "options"),
        Output("periode", "value"),
    ],
    Input("indikator", "value"),
)
def update_filters(indikator):
    if indikator not in datasets:
        return [], None, [], None
    df = datasets[indikator]
    if df.empty:
        return [], None, [], None

    # Update kabupaten options
    kabupaten_options = []
    if indikator == "Inflasi":
        df_full = InflasiCRUD.get_all()
        if not df_full.empty and "kota" in df_full.columns:
            kabupaten_options = [
                {"label": k, "value": k} for k in sorted(df_full["kota"].unique())
            ]
    elif indikator == "Kedalaman Kemiskinan":
        df_full = KedalamanKemiskinanCRUD.get_all()
        if not df_full.empty and "kabupaten_kota" in df_full.columns:
            kabupaten_options = [
                {"label": k, "value": k}
                for k in sorted(df_full["kabupaten_kota"].unique())
            ]

    # Update periode options
    col0 = df.columns[0]
    periode_options = [
        {"label": str(v), "value": str(v)} for v in df[col0].astype(str).unique()
    ]

    return kabupaten_options, None, periode_options, None


@app.callback(
    [
        Output("grafik-utama", "figure"),
        Output("val-terakhir", "children"),
        Output("sub-terakhir", "children"),
        Output("val-diff", "children"),
        Output("sub-diff", "children"),
        Output("val-mean", "children"),
        Output("sub-mean", "children"),
        Output("val-max", "children"),
        Output("sub-max", "children"),
        Output("table-container", "children"),
    ],
    [
        Input("indikator", "value"),
        Input("kabupaten", "value"),
        Input("periode", "value"),
    ],
)
def update_dashboard(indikator, kabupaten, periode):
    if indikator not in datasets:
        return (
            px.scatter(),
            "-",
            "",
            "-",
            "",
            "-",
            "",
            "-",
            "",
            html.Div("Tidak ada data"),
        )

    # Apply kabupaten filter if applicable
    if kabupaten:
        if indikator == "Inflasi":
            df_full = InflasiCRUD.get_all()
            if not df_full.empty and "kota" in df_full.columns:
                df_full = df_full[df_full["kota"] == kabupaten]
                df_melted = df_full.melt(
                    id_vars=["id", "kota", "tahun"],
                    value_vars=[
                        "januari",
                        "februari",
                        "maret",
                        "april",
                        "mei",
                        "juni",
                        "juli",
                        "agustus",
                        "september",
                        "oktober",
                        "november",
                        "desember",
                    ],
                    var_name="Bulan",
                    value_name="Inflasi",
                )
                df = df_melted.dropna(subset=["Inflasi"])[["Bulan", "Inflasi"]]
            else:
                df = datasets[indikator].copy()
        elif indikator == "Kedalaman Kemiskinan":
            df_full = KedalamanKemiskinanCRUD.get_all()
            if not df_full.empty and "kabupaten_kota" in df_full.columns:
                df_full = df_full[df_full["kabupaten_kota"] == kabupaten]
                df = df_full[["kabupaten_kota", "indeks"]].rename(
                    columns={"kabupaten_kota": "Kabupaten/Kota", "indeks": "Indeks"}
                )
            else:
                df = datasets[indikator].copy()
        else:
            df = datasets[indikator].copy()
    else:
        df = datasets[indikator].copy()

    df = df.dropna(how="all")
    if df.shape[1] < 2:
        return (
            px.scatter(),
            "-",
            "",
            "-",
            "",
            "-",
            "",
            "-",
            "",
            html.Div("Data tidak valid"),
        )

    x_col, y_col = df.columns[0], df.columns[1]
    df[y_col] = df[y_col].astype(str).str.replace("%", "").str.replace(",", ".")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")
    df = df.dropna(subset=[y_col])
    df[x_col] = df[x_col].astype(str).str.strip()

    df = df.sort_values(by=x_col, ascending=True)
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        markers=True,
        line_shape="spline",
        title=f"Tren {indikator} di Provinsi Sumatera Selatan",
        color_discrete_sequence=["#003366"],
    )
    fig.update_layout(
        template="plotly_white", title_x=0.5, title_font=dict(size=20, color="#003366")
    )

    if df.empty:
        return fig, "-", "", "-", "", "-", "", "-", "", html.Div("Data kosong")

    last_val = df[y_col].iloc[-1]
    last_label = df[x_col].iloc[-1]
    prev_val = df[y_col].iloc[-2] if len(df) > 1 else None
    diff = last_val - prev_val if prev_val is not None else 0
    mean_val = df[y_col].mean()
    max_val = df[y_col].max()

    table = dbc.Table.from_dataframe(
        df.tail(10), striped=True, bordered=True, hover=True, responsive=True
    )

    return (
        fig,
        f"{last_val:.2f}",
        f"Periode: {last_label}",
        f"{diff:+.2f}" if prev_val is not None else "-",
        f"Sebelumnya: {prev_val:.2f}" if prev_val else "-",
        f"{mean_val:.2f}",
        "Rata-rata periode",
        f"{max_val:.2f}",
        "Nilai maksimum",
        html.Div(
            [
                html.H5("📋 Tabel 10 Baris Terakhir", className="text-primary fw-bold"),
                table,
            ]
        ),
    )


@app.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    State("indikator", "value"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, indikator):
    if indikator not in datasets:
        return None
    df = datasets[indikator]
    return dcc.send_data_frame(df.to_csv, f"{indikator}_Sumsel.csv", index=False)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
