import os 
from typing import List
from requests import Response, post

class MailGunException(Exception):

    def __init__(self,message:str) -> None:
        super().__init__(message)

class Mailgun():

    def __init__(self) -> None:
        self.mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        self.mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        self.from_tile = "AtypikHouse"
        self.from_email = os.getenv("FROM_EMAIL")

    # @classmethod
    def send_email(self, email: List[str], subject: str, text:str, html: str) -> Response:
        if self.mailgun_api_key is None:
            raise MailGunException('Failed to load  mailgun API KEY')

        if self.mailgun_domain is None:
            raise MailGunException("Fail to load MailGun doamin ")

        reponse = post( 
            f"https://api.mailgun.net/v3/sandbox3b97d97e191b4cf8b3fb8786534f29fd.mailgun.org/messages",
            auth=("api", "7d719700f896d8ea2547efa2ecfeb8db-2de3d545-356a8ec5"),
            data={
                "from": f"{self.from_tile} <{self.from_email}>",
			    "to": email,
			    "subject": subject,
			    "text": text,
                "html" : html,
                "o:tracking": False
                },
        )
        if reponse.status_code != 200:
            raise MailGunException("Error in sending confirmation email, user registration failed.")
        
        return reponse