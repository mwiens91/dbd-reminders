"""Sends an email."""

import smtplib
from dbdreminders.constants import EMAIL_SMTP_HOST, EMAIL_SMTP_PORT


def send_email(
    user: str, password: str, recipients: list[str], subject: str, body: str
):
    """This uses pretty standard methods, so look online if you're confused."""
    message = (
        """From: %s\nTo: %s\nSubject: %s\n\n%s
    """
        % (
            user,
            ", ".join(recipients),
            subject,
            body,
        )
    ).encode("utf-8")

    server = smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.sendmail(user, recipients, message)
    server.close()
