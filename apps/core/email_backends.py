import logging

from django.core.mail.backends.base import BaseEmailBackend
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


class SendGridAPIBackend(BaseEmailBackend):
    """
    Custom Django Email Backend that sends emails via the SendGrid Web API (HTTPS)
    instead of SMTP. This is useful for environments like Render Free Tier,
    which block outbound SMTP traffic on ports 25, 465, and 587.
    """

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        from django.conf import settings

        api_key = getattr(settings, "SENDGRID_API_KEY", None)
        if not api_key:
            logger.error("SENDGRID_API_KEY is not configured in settings.")
            return 0

        sg = SendGridAPIClient(api_key)
        sent_count = 0

        for message in email_messages:
            try:
                # Extract plain text content
                plain_body = message.body

                # Extract HTML content if present
                html_body = None
                if hasattr(message, "alternatives") and message.alternatives:
                    for content, mimetype in message.alternatives:
                        if mimetype == "text/html":
                            html_body = content
                            break

                if (
                    not html_body
                    and hasattr(message, "html_message")
                    and message.html_message
                ):
                    html_body = message.html_message

                # Construct SendGrid Mail object
                mail = Mail(
                    from_email=message.from_email,
                    to_emails=message.to,
                    subject=message.subject,
                    plain_text_content=plain_body or " ",
                    html_content=html_body,
                )

                # Send via HTTP POST request (port 443)
                response = sg.send(mail)

                if response.status_code in (200, 201, 202):
                    sent_count += 1
                else:
                    logger.error(
                        f"SendGrid API returned\
                        status code {response.status_code}: {response.body}"
                    )
            except Exception as e:
                logger.error(f"Failed to send email via SendGrid Web API: {e}")
                if not self.fail_silently:
                    raise

        return sent_count
