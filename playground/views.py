from django.core.mail import EmailMessage, BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.http import JsonResponse
from .tasks import notify_customers


def send_email(request):
    notify_customers.delay("Hello")
    # try:
    #     # message = EmailMessage(
    #     #     "subject", "message", "info@storefront.com", ["johndoe@gmail.com"]
    #     # )
    #     # message.attach_file("playground/static/images/dog.jpeg")
    #     # message.send()
    #     message = BaseEmailMessage(
    #         template_name="emails/hello.html", context={"name": "John Doe"}
    #     )
    #     message.send(["janedoe@gmail.com"])
    # except BadHeaderError:
    #     pass
    return JsonResponse({"message": "Email sent"})
