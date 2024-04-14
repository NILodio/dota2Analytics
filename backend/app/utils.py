import logging
import pickle
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import emails  # type: ignore
import numpy as np
import pandas as pd
from jinja2 import Template
from jose import JWTError, jwt
from sklearn.preprocessing import PolynomialFeatures

from app.core.config import settings


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except JWTError:
        return None


def get_numerical_columns(df):
    numeric_types = ["int16", "int32", "int64", "float16", "float32", "float64"]
    return df.select_dtypes(include=numeric_types).columns.to_list()


def apply_log_transformation(df_original):
    df = df_original.copy()
    for column in df.columns.to_list():
        df[column] = df[column].map(lambda value: np.log(value) if value > 0 else 0)
    return df


def standard_scale_dataset(df, scaler_path):
    numerical_columns = get_numerical_columns(df)
    scaler = load_model(scaler_path)
    df_numeric = df[numerical_columns]
    df_scaled = scaler.transform(df_numeric.to_numpy())
    df_scaled = pd.DataFrame(df_scaled, columns=df_numeric.columns.to_list())
    return df_scaled


def extract_polynomial_features(df, degree=2, test_size=0.3):
    polynomial = PolynomialFeatures(
        degree=degree, include_bias=False, interaction_only=False
    )
    features_polynomial = polynomial.fit_transform(df)
    return pd.DataFrame(features_polynomial)


def load_model(path):
    return pickle.load(open(path, "rb"))


def make_prediction(df, model_path, scaler_path):
    df = apply_log_transformation(df)
    df_scaled = standard_scale_dataset(df, scaler_path)
    complex_df = extract_polynomial_features(df_scaled, degree=2)
    model = load_model(model_path)
    y_pred = model.predict(complex_df)
    return y_pred
