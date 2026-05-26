import logging
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status, throttling
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContactMessage
from .serializers import ContactSerializer

logger = logging.getLogger(__name__)


class ContactThrottle(throttling.AnonRateThrottle):
    rate = "3/min"  # Limit: 3 requests per minute per IP


def send_contact_emails_async(data):
    """
    Background worker function that handles SMTP connections asynchronously.
    Renders and delivers copies to both the portfolio owner (admin) and the client.
    """
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@localhost")
    admin_email = getattr(settings, "ADMIN_EMAIL", "bonheurndezenc@gmail.com")

    # 1. Dispatch Admin Notification Copy
    try:
        admin_subject = f"Portfolio Inquiry: {data['subject']}"
        admin_html = render_to_string("contact/email_notification.html", context=data)
        admin_plain = strip_tags(admin_html)

        send_mail(
            subject=admin_subject,
            message=admin_plain,
            from_email=from_email,
            recipient_list=[admin_email],
            html_message=admin_html,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Async SMTP delivery failed for Admin notification: {e}")

    # 2. Dispatch Client Receipt Copy
    try:
        client_subject = f"Inquiry Received: {data['subject']}"
        client_html = render_to_string(
            "contact/email_client_confirmation.html", context=data
        )
        client_plain = strip_tags(client_html)

        send_mail(
            subject=client_subject,
            message=client_plain,
            from_email=from_email,
            recipient_list=[data["email"]],
            html_message=client_html,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Async SMTP delivery failed for Client confirmation: {e}")


class ContactAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # 1. Save to Local Database for secure backup
            try:
                ContactMessage.objects.create(
                    name=data["name"],
                    email=data["email"],
                    subject=data["subject"],
                    message=data["message"],
                )
            except Exception as db_err:
                logger.error(f"Database save failed for contact message: {db_err}")
                # We continue to try sending the email even if DB fails
                # for maximum fault-tolerance.

            # 2. Trigger async background email delivery daemon
            try:
                email_thread = threading.Thread(
                    target=send_contact_emails_async, args=(data,), daemon=True
                )
                email_thread.start()
            except Exception as thread_err:
                logger.error(
                    "Failed to spawn background thread for email dispatch: "
                    f"{thread_err}"
                )

            return Response(
                {"message": "Message sent successfully!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
