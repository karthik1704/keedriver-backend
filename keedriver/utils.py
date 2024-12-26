from firebase_admin import messaging
from rest_framework import pagination
from rest_framework.response import Response

from accounts.models import FCMToken


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        next = None
        previous = None

        if self.page.has_next():
            next = self.page.next_page_number()
        if self.page.has_previous():
            previous = self.page.previous_page_number()
        return Response(
            {
                "next": next,
                "previous": previous,
                "count": self.page.paginator.count,
                "results": data,
            }
        )


def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    try:
        response = messaging.send(message)
        print("Successfully sent message:", response)
    except Exception as e:
        print("Error sending message:", e)


def send_push_notification_to_user(user, title, body):
    tokens = FCMToken.objects.filter(user=user).values_list("token", flat=True)
    for token in tokens:
        try:
            send_push_notification(token, title, body)
        except Exception as e:
            print(f"Error sending to token {token}: {e}")
