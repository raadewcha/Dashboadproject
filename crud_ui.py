import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, ctx, dash
import pandas as pd
from database import (
    InflasiCRUD,
    NilaiTukarPetaniCRUD,
    NilaiImporCRUD,
    KedalamanKemiskinanCRUD,
    PendudukUmurSekolahCRUD,
)


def get_crud_layout():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "Manajemen Data",
                                        className="text-primary fw-bold mb-0 d-inline",
                                    ),
                                    dbc.Button(
                                        "Logout",
                                        id="btn-logout",
                                        color="danger",
                                        size="sm",
                                        className="float-end",
                                    ),
                                ],
                                className="mb-3",
                            ),
                            dbc.Alert(
                                id="crud-alert",
                                is_open=False,
                                duration=4000,
                                color="success",
                                dismissable=True,
                                className="mb-3",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Label(
                                                "Pilih Tabel Data", className="fw-bold"
                                            ),
                                            dcc.Dropdown(
                                                id="crud-table-selector",
                                                options=[
                                                    {
                                                        "label": "Inflasi",
                                                        "value": "inflasi",
                                                    },
                                                    {
                                                        "label": "Nilai Tukar Petani",
                                                        "value": "nilai_tukar_petani",
                                                    },
                                                    {
                                                        "label": "Nilai Impor",
                                                        "value": "nilai_impor",
                                                    },
                                                    {
                                                        "label": "Kedalaman Kemiskinan",
                                                        "value": "kedalaman_kemiskinan",
                                                    },
                                                    {
                                                        "label": "Penduduk Menurut Umur Sekolah",
                                                        "value": "penduduk_umur_sekolah",
                                                    },
                                                ],
                                                value="inflasi",
                                                clearable=False,
                                                className="mb-3",
                                            ),
                                            dbc.Button(
                                                "Tambah Data Baru",
                                                id="btn-add-new",
                                                color="success",
                                                className="w-100",
                                            ),
                                        ]
                                    )
                                ],
                                className="shadow-sm mb-4",
                            ),
                        ],
                        width=12,
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(id="crud-table-container"),
                        ],
                        width=12,
                    )
                ]
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                    dbc.ModalBody(id="modal-body"),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Batal",
                                id="btn-cancel",
                                color="secondary",
                                className="me-2",
                            ),
                            dbc.Button("Simpan", id="btn-save", color="primary"),
                        ]
                    ),
                ],
                id="crud-modal",
                size="xl",
                is_open=False,
                scrollable=True,
            ),
            dcc.Store(id="crud-store-edit-id"),
            dcc.Store(id="crud-store-action"),
            dcc.Store(id="crud-refresh-trigger", data=0),
        ],
        fluid=True,
        className="mt-4",
    )


def register_crud_callbacks(app):
    @app.callback(
        Output("crud-table-container", "children"),
        [
            Input("crud-table-selector", "value"),
            Input("crud-refresh-trigger", "data"),
        ],
    )
    def update_table(table_name, refresh_trigger):
        df = pd.DataFrame()

        if table_name == "inflasi":
            df = InflasiCRUD.get_all()
        elif table_name == "nilai_tukar_petani":
            df = NilaiTukarPetaniCRUD.get_all()
        elif table_name == "nilai_impor":
            df = NilaiImporCRUD.get_all()
        elif table_name == "kedalaman_kemiskinan":
            df = KedalamanKemiskinanCRUD.get_all()
        elif table_name == "penduduk_umur_sekolah":
            df = PendudukUmurSekolahCRUD.get_all()

        if df.empty:
            return html.Div(
                "Belum ada data.", className="alert alert-warning text-center"
            )

        if "created_at" in df.columns:
            df = df.drop(columns=["created_at"])
        if "updated_at" in df.columns:
            df = df.drop(columns=["updated_at"])
        if "indikator_id" in df.columns:
            df = df.drop(columns=["indikator_id"])

        table_header = [
            html.Thead(
                html.Tr(
                    [html.Th(col) for col in df.columns]
                    + [html.Th("Aksi", style={"width": "150px"})]
                )
            )
        ]

        rows = []
        for idx, row in df.iterrows():
            row_cells = [html.Td(row[col]) for col in df.columns]
            row_cells.append(
                html.Td(
                    [
                        dbc.Button(
                            "✏️",
                            id={"type": "btn-edit", "index": row["id"]},
                            color="warning",
                            size="sm",
                            className="me-1",
                        ),
                        dbc.Button(
                            "🗑️",
                            id={"type": "btn-delete", "index": row["id"]},
                            color="danger",
                            size="sm",
                        ),
                    ]
                )
            )
            rows.append(html.Tr(row_cells))

        table_body = [html.Tbody(rows)]

        return dbc.Card(
            dbc.CardBody(
                [
                    html.H5(
                        f"Data {table_name.replace('_', ' ').title()}",
                        className="text-primary fw-bold mb-3",
                    ),
                    dbc.Table(
                        table_header + table_body,
                        bordered=True,
                        hover=True,
                        responsive=True,
                        striped=True,
                    ),
                ]
            ),
            className="shadow-sm",
        )

    @app.callback(
        [
            Output("crud-modal", "is_open"),
            Output("modal-title", "children"),
            Output("modal-body", "children"),
            Output("crud-store-edit-id", "data"),
            Output("crud-store-action", "data"),
        ],
        [
            Input("btn-add-new", "n_clicks"),
            Input({"type": "btn-edit", "index": ALL}, "n_clicks"),
            Input("btn-cancel", "n_clicks"),
        ],
        [State("crud-table-selector", "value")],
        prevent_initial_call=True,
    )
    def toggle_modal(add_clicks, edit_clicks, cancel_clicks, table_name):
        if not ctx.triggered:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        triggered = ctx.triggered_id

        if triggered is None:
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update,
            )

        if triggered == "btn-cancel":
            return False, "", "", None, None

        if triggered == "btn-add-new":
            if not add_clicks:
                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )
            form = generate_form(table_name, None)
            return True, "Tambah Data Baru", form, None, "add"

        if isinstance(triggered, dict) and triggered.get("type") == "btn-edit":
            if not edit_clicks or not any(edit_clicks):
                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            record_id = triggered["index"]
            data = None

            if table_name == "inflasi":
                result = InflasiCRUD.get_by_id(record_id)
                data = result[0] if result else None
            elif table_name == "nilai_tukar_petani":
                result = NilaiTukarPetaniCRUD.get_by_id(record_id)
                data = result[0] if result else None
            elif table_name == "nilai_impor":
                result = NilaiImporCRUD.get_by_id(record_id)
                data = result[0] if result else None
            elif table_name == "kedalaman_kemiskinan":
                result = KedalamanKemiskinanCRUD.get_by_id(record_id)
                data = result[0] if result else None
            elif table_name == "penduduk_umur_sekolah":
                result = PendudukUmurSekolahCRUD.get_by_id(record_id)
                data = result[0] if result else None

            if data:
                form = generate_form(table_name, data)
                return True, "Edit Data", form, record_id, "edit"

        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )

    @app.callback(
        [
            Output("crud-modal", "is_open", allow_duplicate=True),
            Output("crud-alert", "children"),
            Output("crud-alert", "is_open"),
            Output("crud-alert", "color"),
            Output("crud-refresh-trigger", "data"),
        ],
        Input("btn-save", "n_clicks"),
        [
            State("crud-table-selector", "value"),
            State("crud-store-edit-id", "data"),
            State("crud-store-action", "data"),
            State({"type": "form-field", "field": ALL}, "value"),
            State({"type": "form-field", "field": ALL}, "id"),
            State("crud-refresh-trigger", "data"),
        ],
        prevent_initial_call=True,
    )
    def save_data(
        save_clicks, table_name, edit_id, action, form_values, form_ids, refresh_trigger
    ):
        if not save_clicks:
            return dash.no_update, "", False, "success", dash.no_update

        data = {}
        for i, field_id in enumerate(form_ids):
            field_name = field_id["field"]
            data[field_name] = form_values[i]

        try:
            if action == "add":
                if table_name == "inflasi":
                    InflasiCRUD.create(data)
                elif table_name == "nilai_tukar_petani":
                    NilaiTukarPetaniCRUD.create(data)
                elif table_name == "nilai_impor":
                    NilaiImporCRUD.create(data)
                elif table_name == "kedalaman_kemiskinan":
                    KedalamanKemiskinanCRUD.create(data)
                elif table_name == "penduduk_umur_sekolah":
                    PendudukUmurSekolahCRUD.create(data)
                message = "Data berhasil ditambahkan!"

            elif action == "edit" and edit_id:
                if table_name == "inflasi":
                    InflasiCRUD.update(edit_id, data)
                elif table_name == "nilai_tukar_petani":
                    NilaiTukarPetaniCRUD.update(edit_id, data)
                elif table_name == "nilai_impor":
                    NilaiImporCRUD.update(edit_id, data)
                elif table_name == "kedalaman_kemiskinan":
                    KedalamanKemiskinanCRUD.update(edit_id, data)
                elif table_name == "penduduk_umur_sekolah":
                    PendudukUmurSekolahCRUD.update(edit_id, data)
                message = "Data berhasil diperbarui!"

            return False, message, True, "success", refresh_trigger + 1

        except Exception as e:
            return True, f"Error: {str(e)}", True, "danger", dash.no_update

    @app.callback(
        [
            Output("crud-refresh-trigger", "data", allow_duplicate=True),
            Output("crud-alert", "children", allow_duplicate=True),
            Output("crud-alert", "is_open", allow_duplicate=True),
            Output("crud-alert", "color", allow_duplicate=True),
        ],
        Input({"type": "btn-delete", "index": ALL}, "n_clicks"),
        [
            State("crud-table-selector", "value"),
            State("crud-refresh-trigger", "data"),
        ],
        prevent_initial_call=True,
    )
    def delete_record(delete_clicks, table_name, refresh_trigger):
        if not any(delete_clicks):
            return dash.no_update, "", False, "success"

        triggered = ctx.triggered_id
        if isinstance(triggered, dict) and triggered["type"] == "btn-delete":
            record_id = triggered["index"]

            try:
                if table_name == "inflasi":
                    InflasiCRUD.delete(record_id)
                elif table_name == "nilai_tukar_petani":
                    NilaiTukarPetaniCRUD.delete(record_id)
                elif table_name == "nilai_impor":
                    NilaiImporCRUD.delete(record_id)
                elif table_name == "kedalaman_kemiskinan":
                    KedalamanKemiskinanCRUD.delete(record_id)
                elif table_name == "penduduk_umur_sekolah":
                    PendudukUmurSekolahCRUD.delete(record_id)

                return refresh_trigger + 1, "Data berhasil dihapus!", True, "success"

            except Exception as e:
                return dash.no_update, f"Error: {str(e)}", True, "danger"

        return dash.no_update, "", False, "success"


def generate_form(table_name, data=None):
    fields = []

    if table_name == "inflasi":
        fields = [
            ("tahun", "Tahun", "number", data.get("tahun") if data else 2024),
            ("kota", "Kota", "text", data.get("kota") if data else ""),
            ("januari", "Januari", "number", data.get("januari") if data else 0),
            ("februari", "Februari", "number", data.get("februari") if data else 0),
            ("maret", "Maret", "number", data.get("maret") if data else 0),
            ("april", "April", "number", data.get("april") if data else 0),
            ("mei", "Mei", "number", data.get("mei") if data else 0),
            ("juni", "Juni", "number", data.get("juni") if data else 0),
            ("juli", "Juli", "number", data.get("juli") if data else 0),
            ("agustus", "Agustus", "number", data.get("agustus") if data else 0),
            ("september", "September", "number", data.get("september") if data else 0),
            ("oktober", "Oktober", "number", data.get("oktober") if data else 0),
            ("november", "November", "number", data.get("november") if data else 0),
            ("desember", "Desember", "number", data.get("desember") if data else 0),
        ]

    elif table_name == "nilai_tukar_petani":
        fields = [
            ("tahun", "Tahun", "number", data.get("tahun") if data else 2025),
            (
                "jenis_ntp",
                "Jenis NTP",
                "text",
                data.get("jenis_ntp") if data else "NTP",
            ),
            ("januari", "Januari", "number", data.get("januari") if data else 0),
            ("februari", "Februari", "number", data.get("februari") if data else 0),
            ("maret", "Maret", "number", data.get("maret") if data else 0),
            ("april", "April", "number", data.get("april") if data else 0),
            ("mei", "Mei", "number", data.get("mei") if data else 0),
            ("juni", "Juni", "number", data.get("juni") if data else 0),
            ("juli", "Juli", "number", data.get("juli") if data else 0),
            ("agustus", "Agustus", "number", data.get("agustus") if data else 0),
            ("september", "September", "number", data.get("september") if data else 0),
            ("oktober", "Oktober", "number", data.get("oktober") if data else 0),
            ("november", "November", "number", data.get("november") if data else 0),
            ("desember", "Desember", "number", data.get("desember") if data else 0),
        ]

    elif table_name == "nilai_impor":
        fields = [
            ("tahun", "Tahun", "number", data.get("tahun") if data else 2024),
            ("bulan", "Bulan", "text", data.get("bulan") if data else ""),
            ("nilai", "Nilai (US$)", "number", data.get("nilai") if data else 0),
        ]

    elif table_name == "kedalaman_kemiskinan":
        fields = [
            ("tahun", "Tahun", "number", data.get("tahun") if data else 2025),
            (
                "kabupaten_kota",
                "Kabupaten/Kota",
                "text",
                data.get("kabupaten_kota") if data else "",
            ),
            ("indeks", "Indeks", "number", data.get("indeks") if data else 0),
        ]

    elif table_name == "penduduk_umur_sekolah":
        fields = [
            ("tahun", "Tahun", "number", data.get("tahun") if data else 2024),
            (
                "kelompok_umur",
                "Kelompok Umur",
                "text",
                data.get("kelompok_umur") if data else "",
            ),
            (
                "tidak_belum_sekolah",
                "Tidak/Belum Sekolah (%)",
                "number",
                data.get("tidak_belum_sekolah") if data else 0,
            ),
            (
                "masih_sekolah",
                "Masih Sekolah (%)",
                "number",
                data.get("masih_sekolah") if data else 0,
            ),
            (
                "tidak_sekolah_lagi",
                "Tidak Sekolah Lagi (%)",
                "number",
                data.get("tidak_sekolah_lagi") if data else 0,
            ),
        ]

    form_fields = []
    for field_id, label, field_type, value in fields:
        form_fields.append(
            dbc.Row(
                [
                    dbc.Label(label, width=3, className="fw-bold"),
                    dbc.Col(
                        dbc.Input(
                            id={"type": "form-field", "field": field_id},
                            type=field_type,
                            value=value,
                            step="0.01" if field_type == "number" else None,
                            className="mb-2",
                        ),
                        width=9,
                    ),
                ],
                className="mb-2",
            )
        )

    return html.Div(form_fields)
