import dash_bootstrap_components as dbc
from dash import html, dcc
from flask import session

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"


def get_login_layout():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H4(
                                            "Login Admin",
                                            className="text-center text-white mb-0",
                                        ),
                                        style={"backgroundColor": "#003366"},
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                id="login-alert-container",
                                                className="mb-3",
                                            ),
                                            dbc.Label("Username", className="fw-bold"),
                                            dbc.Input(
                                                id="login-username",
                                                type="text",
                                                placeholder="Masukkan username",
                                                className="mb-3",
                                            ),
                                            dbc.Label("Password", className="fw-bold"),
                                            dbc.Input(
                                                id="login-password",
                                                type="password",
                                                placeholder="Masukkan password",
                                                className="mb-3",
                                            ),
                                            dbc.Button(
                                                "Login",
                                                id="btn-login",
                                                color="primary",
                                                className="w-100",
                                            ),
                                        ]
                                    ),
                                ],
                                className="shadow-lg",
                            )
                        ],
                        width={"size": 4, "offset": 4},
                        className="mt-5",
                    )
                ]
            )
        ],
        fluid=True,
        style={"backgroundColor": "#eef2f5", "minHeight": "100vh"},
    )


def check_authentication():
    return session.get("authenticated", False)


def login_user(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["authenticated"] = True
        session["username"] = username
        return True
    return False


def logout_user():
    session.clear()
