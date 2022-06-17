"""Sends an email."""

import smtplib
from dbdreminders.constants import EMAIL_SMTP_HOST, EMAIL_SMTP_PORT


def send_email(
    user: str, password: str, recipients: list[str], subject: str, body: str
):
    """This uses pretty standard methods, so look online if you're confused.

    Note that as of May 30, 2022, you must use an "App Password" if
    using Gmail. See
    https://support.google.com/accounts/answer/6010255?hl=en&visit_id=637896899107643254-869975220&p=less-secure-apps&rd=1#zippy=%2Cuse-an-app-password.
    """
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
