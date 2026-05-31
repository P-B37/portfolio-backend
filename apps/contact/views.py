import logging
import threading
import urllib.parse

import requests
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


def send_contact_notifications_async(data):
    """
    Background worker function that handles notifications asynchronously.
    1. Sends an instant WhatsApp alert to the portfolio owner (Priority).
    2. Dispatches email copies to the portfolio owner (admin) and the client.
    """
    # --- 1. PRIORITY: WhatsApp Notification via CallMeBot ---
    whatsapp_number = getattr(settings, "WHATSAPP_NUMBER", None)
    whatsapp_apikey = getattr(settings, "WHATSAPP_API_KEY", None)

    if whatsapp_number and whatsapp_apikey:
        try:
            whatsapp_message = (
                f"📩 *New Portfolio Contact Form Submission*\n\n"
                f"👤 *Name:* {data['name']}\n"
                f"✉️ *Email:* {data['email']}\n"
                f"📝 *Subject:* {data['subject']}\n\n"
                f"💬 *Message:*\n{data['message']}"
            )
            encoded_message = urllib.parse.quote(whatsapp_message)
            url = (
                f"https://api.callmebot.com/whatsapp.php"
                f"?phone={whatsapp_number}"
                f"&text={encoded_message}"
                f"&apikey={whatsapp_apikey}"
            )
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                logger.info("WhatsApp contact form notification sent successfully.")
            else:
                logger.error(
                    f"CallMeBot WhatsApp dispatch failed with code "
                    f"{response.status_code}: {response.text}"
                )
        except Exception as wa_err:
            logger.error(f"Failed to dispatch WhatsApp notification: {wa_err}")
    else:
        logger.warning(
            "WhatsApp notifications skipped: "
            "WHATSAPP_NUMBER or WHATSAPP_API_KEY not configured."
        )

    # --- 2. Email Notifications ---
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@localhost")
    admin_email = getattr(settings, "ADMIN_EMAIL", "bonheurndezenc@gmail.com")

    # A. Dispatch Admin Notification Copy
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

    # B. Dispatch Client Receipt Copy
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

            # 2. Trigger async background notifications daemon
            try:
                email_thread = threading.Thread(
                    target=send_contact_notifications_async, args=(data,), daemon=True
                )
                email_thread.start()
            except Exception as thread_err:
                logger.error(
                    "Failed to spawn background thread for notification dispatch: "
                    f"{thread_err}"
                )

            return Response(
                {"message": "Message sent successfully!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
