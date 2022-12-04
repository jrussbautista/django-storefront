from django.core.mail import EmailMessage, BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.http import JsonResponse


def send_email(request):
    try:
        # message = EmailMessage(
        #     "subject", "message", "info@storefront.com", ["johndoe@gmail.com"]
        # )
        # message.attach_file("playground/static/images/dog.jpeg")
        # message.send()
        message = BaseEmailMessage(
            template_name="emails/hello.html", context={"name": "John Doe"}
        )
        message.send(["janedoe@gmail.com"])
    except BadHeaderError:
        pass
    return JsonResponse({"message": "Email sent"})
 