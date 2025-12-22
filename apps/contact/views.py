from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, throttle
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer
import logging

logger = logging.getLogger(__name__)


class ContactThrottle(throttle.AnonRateThrottle):
    rate = "3/min"  # Limit: 3 requests per minute per IP


class ContactAPIView(APIView):
    throttle_classes = [ContactThrottle]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # Construct the email
            # We send the email TO ourselves, FROM the user's data
            email_subject = f"Portfolio Contact: {data['subject']}"
            email_body = f"""
            You have received a new message from your portfolio.

            Name: {data['name']}
            Email: {data['email']}

            Message:
            {data['message']}
            """

            try:
                # 'fail_silently=False' lets us catch the error if SMTP fails
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],  # We will add this setting
                    fail_silently=False,
                )

                return Response(
                    {"message": "Message sent successfully!"}, status=status.HTTP_200_OK
                )

            except Exception as e:
                # Log the error for debugging, but return a generic error to user
                logger.error(f"Email sending failed: {str(e)}")
                return Response(
                    {"error": "Failed to send message. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
