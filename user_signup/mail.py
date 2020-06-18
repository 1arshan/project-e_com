from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .token import account_activation_token


def sendmail(user, current_site):
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    name = user.first_name
    message = Mail(
        from_email='onearshanahmad@outlook.com',
        to_emails=user.email,
        subject='Activate Your Account',
        html_content='<h3> Hello ' + name.capitalize() + ',</h3>'
                    '<p>Please click on the link to confirm your registration,</p>'
                    'http://' + domain + '/'+'user_signup/verify_email/'+ uid + '/' + token
    )

    try:
        sg = SendGridAPIClient('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 ')
        response = sg.send(message)
    except Exception as e:
        print(e)

