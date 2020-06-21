from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from user_signup.token import account_activation_token
from medhistory.secrets import EmailToken
import asyncio


async def sendmail(*args):
    message = Mail(
        from_email=EmailToken.from_email,
        to_emails=args[2],
        subject=args[0],
        html_content=args[1]
    )

    try:

        sg = SendGridAPIClient(EmailToken.sendgrid_token)
        response = sg.send(message)
        print("mail send")
    except Exception as e:
        print("mail not send")
        print(e)



async def MailVerification(user, current_site):
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    name = user.first_name
    receiver_email = user.email
    subject = 'Activate Your Account'
    html_content = str('<h3> Hello ' + name.capitalize() + ',</h3>'
                '<p>Please click on the link to confirm your registration,</p>'
                'http://' + domain + '/' + 'user_signup/verify_email/' + uid + '/' + token)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(sendmail(subject, html_content, receiver_email))
    loop.close()

