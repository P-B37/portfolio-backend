from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, throttling
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.conf import settings
from .serializers import ContactSerializer
import logging

logger = logging.getLogger(__name__)


class ContactThrottle(throttling.AnonRateThrottle):
    rate = "3/min"  # Limit: 3 requests per minute per IP


class ContactAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # 1. Prepare the HTML Content
            # We pass the 'data' dict as context to the template
            html_message = render_to_string(
                "contact/email_notification.html", context=data
            )

            # 2. Prepare the Plain Text Content (Fallback)
            # Good for spam filters and old email clients
            plain_message = strip_tags(html_message)

            email_subject = f"Portfolio: {data['subject']}"

            try:
                send_mail(
                    subject=email_subject,
                    message=plain_message,  # <--- The plain text version goes here
                    from_email="bonheurndezenc@gmail.com",
                    recipient_list="bonheurndezenc@gmail.com",
                    html_message=html_message,  # <--- The HTML version goes here
                    fail_silently=False,
                )

                return Response({"message": "Message sent!"}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Email failed: {e}")
                return Response(
                    {"error": "Failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
