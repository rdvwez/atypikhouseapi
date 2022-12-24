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

        if self.mailgun_domain in None:
            raise MailGunException("Fail to load MailGun doamin ")

        reponse = post( 
            f"http://api.mailgun.net/v3/{self.mailgun_domain}/messages",
            auth=("api", self.mailgun_api_key),
            data={
                "from": f"{self.from_tile} <{self.from_email}>",
			    "to": email,
			    "subject": subject,
			    "text": text,
                "html" : html
                },
        )
        
        if reponse.status_code != 200:
            raise MailGunException("Error in sending confirmation email, user registration failed.")
        
        return reponse