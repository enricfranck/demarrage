import json
import logging
import secrets
import smtplib
import ssl
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID

import emails
import requests
from emails.template import JinjaTemplate
from jose import jwt
from pydantic import EmailStr
from sqlalchemy import MetaData, Table
from unidecode import unidecode

from app import schemas
from app.core.config import settings
from app.db.session import engine


def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def create_secret():
    res = "".join(secrets.choice(string.ascii_letters + string.digits) for x in range(10))
    return res



def decode_text(text: str) -> str:
    str_ = text.replace(" ", "_")
    return unidecode(str_.replace("-", "_"))


def send_new_account(email_to: str, password: str) -> any:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.EMAILS_FROM_EMAIL
    sender_password = settings.PASSWORD_FROM_EMAIL

    message = f"""\
        FROM: "
        To: {email_to}
        Subject: "
        Nouveau compte:\n
        Username: {email_to}
        Password: {password}
        """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email_to, message)


def check_email_valide(email: EmailStr) -> str:
    response = requests.get("https://isitarealemail.com/api/email/validate",
                            params={"email": email})
    status = response.json()["status"]
    return status

def convert_date(date: str) -> str:
    month = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet",
            "Aout", "Séptembre", "Octobre", "Novembre","Décembre", ""]
    # 1995-10-20
    if not date :
        return ""
    try:
        days = date[8:10]
        year = date[0:4]
        month_ = int(date[5:7])
        return f"{days} {month[month_ - 1]} {year}"
    except Exception as e:
        print(e , date)
        return  ""

def clear_name(name: str, nbr: int = 50) -> str :
    if len(name) <= nbr:
        return name
    else:
        return name[0:nbr]+" ..."


def format_date(date_: datetime = ""):
    if date_ == "":
        date_= datetime.now()
    d2 = date_.astimezone()
    return format(d2.strftime("%Y-%m-%d %H:%M:%S"))


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)

