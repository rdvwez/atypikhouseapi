import os
import sys
import smtplib
import traceback
from typing import Union
from flask import request, url_for, render_template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

    # message = Mail(
    #     from_email='your-email@example.com',
    #     to_emails='recipient@example.com',
    #     subject='Test Email',
    #     html_content='<strong>This is a test email</strong>')

    # try:
    #     sg = SendGridAPIClient('YOUR_SENDGRID_API_KEY')
    #     response = sg.send(message)
    #     return f"Email sent successfully! Response: {response.status_code}"
    # except Exception as e:
    #     return f"Error sending email: {str(e)}"

def send_confirmation_account_mail(user_id:int, email:str, subject:str, url_suffix:str) -> Union[Exception, None]:
        # breakpoint()
        # print(os.environ.get('SMPT_SERVER'))
        link = request.url_root[0:-1] + url_for(url_suffix,user_id = user_id)
        text = f""""Hello!
            We thank you for creating your account on Atypik House,
            Please click the link to confirm your registration: {link}"""
        # html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'
        
        message = MIMEMultipart("alternative")
        message["From"] = os.environ.get('FROM_ADDR')
        message["To"] = email
        message["Subject"] = subject

        part1 = MIMEText(text, "plain")
        # part2 = MIMEText(html, "html")

        message.attach(part1)
        # message.attach(part2)
        # breakpoint()
        err=None
        try:
            # Connexion au serveur SMTP
            server = smtplib.SMTP(os.environ.get('SMPT_SERVER'), os.environ.get('SMTP_PORT'))
            
            server.starttls()
            server.login(os.environ.get('SMTP_LOGIN'), os.environ.get('SMTP_PASSWORD'))

            # Envoi du message
            server.sendmail(os.environ.get('FROM_ADDR'), email, message.as_string())
            # print("E-mail envoyé avec succès !")
            # breakpoint()

        except Exception as e:
            err = e
            print("Une erreur s'est produite lors de l'envoi de l'e-mail : ", email)
        except KeyboardInterrupt as er:
            # err = er
            err = traceback.print_exc(file=sys.stdout)
            # breakpoint()

        finally:
            # Fermeture de la connexion SMTP
            if 'server' in locals():
                server.quit()
        return err

def send_reservation_confirmation_mail(email:str, subject:str,amount:str):
    text = f""""Hello!
            your payment has been received, for an amount of {amount} €
            
            Enjoy your stay!"""
    
    message = MIMEMultipart("alternative")
    message["From"] = os.environ.get('FROM_ADDR')
    message["To"] = email
    message["Subject"] = subject

    mime_document = MIMEText(text, "plain")
    message.attach(mime_document)

    err=None
    try:
        server = smtplib.SMTP(os.environ.get('SMPT_SERVER'), os.environ.get('SMTP_PORT'))
        
        server.starttls()
        server.login(os.environ.get('SMTP_LOGIN'), os.environ.get('SMTP_PASSWORD'))

        server.sendmail(os.environ.get('FROM_ADDR'), email, message.as_string())

    except Exception as e:
        err = e
        print("Une erreur s'est produite lors de l'envoi de l'e-mail : ", email)
    except KeyboardInterrupt as er:
        err = traceback.print_exc(file=sys.stdout)
    finally:
        # Fermeture de la connexion SMTP
        if 'server' in locals():
            server.quit()
    if err:
        print("[Senf Email Error]: Une erreur s'est produite pendant l'envoie de le mail de confirmation")
        print(err)
    print("Le mail de confirmation d'achat a été envoyé avec succès à l'e-mail : ", email)
    return err
        