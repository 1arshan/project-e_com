from celery import shared_task
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from medhistory.secrets import EmailToken


@shared_task
def send_parallel_mail(subject, content, to_email):
    message = Mail(
        from_email=EmailToken.from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    try:

        sg = SendGridAPIClient(EmailToken.sendgrid_token)
        response = sg.send(message)
        #print("mail send")
    except Exception as e:
        #print("mail not send")
        print(e)


