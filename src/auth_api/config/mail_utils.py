"""Module responsible for sending emails"""
import logging
import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from auth import settings

LOGGER = logging.getLogger(__name__)


class MailUtils:
    """
    Mail Utils class
    """

    @classmethod
    def send_mail(cls,
                  subject,
                  message_text,
                  message_html,
                  to_mail_address=None,
                  cc_mail_address=None,
                  bcc_mail_address=None,
                  reply_to=None,
                  ):
        """
        Send an email with message_text or message_html content from from_email to to_mail_address
        :param subject:
        :param message_text:
        :param message_html:
        :param from_email:
        :param to_mail_address:
        :param cc_mail_address:
        :param bcc_mail_address:
        :param reply_to:
        :return:
        """

        from_email = settings.DEFAULT_FROM_EMAIL
        if to_mail_address is None and cc_mail_address is None and bcc_mail_address is None:
            LOGGER.warning("Tried to send an e-mail without destination addresses (either in to, cc or bcc)")
            return
        # We add the name of the instance within the mail
        subject_with_name = f"{subject}"
        msg = EmailMultiAlternatives(
            subject_with_name,
            message_text,
            from_email,
            to_mail_address,
            cc=cc_mail_address,
            bcc=bcc_mail_address,
            reply_to=reply_to,
        )
        if message_html is not None:
            msg.attach_alternative(message_html, "text/html")
        msg.send()
        LOGGER.info("Sent %s email to %s", subject, to_mail_address)

    @staticmethod
    def _get_html_template(template_path, template_data):
        """
        Return the HTML template rendered using template_data
        :param template_path: the template path as a string (root path: /restapi/templates)
        :param template_data: The template data as a JSON collection
        :return: the HTML template rendered
        """
        mail_template = get_template(template_path)
        return mail_template.render(template_data)

    @classmethod
    def send_user_awaiting_activation(cls, user, token):
        to_address = [user.email]
        subject = "Registration"
        plain_text = "You registered on our Portal, now you must activate your account."
        html_template = cls._get_html_template(
            template_path="mails/auth/user_await_activation.html",
            template_data={"token": token,
                           "frontend_url": os.environ.get("FRONTEND_URL"),
                           "user": user})
        cls.send_mail(subject=subject, message_text=plain_text, message_html=html_template,
                      to_mail_address=to_address)
