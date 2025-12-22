from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField(min_length=10)

    # Senior Detail: Honey Pot (Optional field that should be empty)
    # If a bot fills this, we know it's spam.
    # We won't implement it complexly now, but we keep the structure clean.
